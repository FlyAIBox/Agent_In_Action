"""
深度研究助手 (Deep Research Assistant) - LangGraph 智能代理系统

这个模块实现了一个基于 LangGraph 的深度研究助手，具备以下核心功能：

1. 分析师团队生成：
   - 根据研究主题自动生成多位AI分析师
   - 支持人类反馈进行分析师调整
   - 每位分析师负责特定的研究视角

2. 并行访谈系统：
   - 分析师与专家进行多轮深度访谈
   - 支持网络搜索和百科检索
   - 智能提问和回答生成

3. 报告生成：
   - 自动整合多个分析师的研究成果
   - 生成结构化的研究报告
   - 包含引言、主体内容、结论和引用

4. 工作流架构：
   - 使用 Map-Reduce 模式并行处理
   - 支持人机协同（Human-in-the-loop）
   - 完整的状态管理和检查点机制
"""

import os
import getpass
from typing import List, Annotated, Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
import operator

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import get_buffer_string
from langchain_openai import ChatOpenAI

# 导入搜索工具
from langchain_community.tools.tavily_search import TavilySearchResults

# 导入百度百科加载器（从同级目录导入）
from baike_loader import BaiduBaikeLoader

# LangGraph 相关导入
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Send
from langgraph.graph import MessagesState

import configuration

## 数据模型定义

class Analyst(BaseModel):
    """分析师数据模型"""
    affiliation: str = Field(description="分析师的主要隶属机构或组织")
    name: str = Field(description="分析师姓名")
    role: str = Field(description="分析师在研究主题中的具体角色定位")
    description: str = Field(description="分析师的关注焦点、关切点和动机的详细描述")

    @property
    def persona(self) -> str:
        """生成分析师人设描述"""
        return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"


class Perspectives(BaseModel):
    """分析师集合数据模型"""
    analysts: List[Analyst] = Field(description="包含所有分析师角色和隶属机构的综合列表")


class GenerateAnalystsState(TypedDict):
    """分析师生成状态管理"""
    topic: str  # 研究主题
    max_analysts: int  # 分析师数量上限
    human_analyst_feedback: str  # 人类反馈信息
    analysts: List[Analyst]  # 生成的分析师列表


class SearchQuery(BaseModel):
    """搜索查询数据模型"""
    search_query: str = Field(None, description="用于检索的搜索查询语句")


class InterviewState(MessagesState):
    """访谈状态管理类"""
    max_num_turns: int  # 对话轮次上限
    context: Annotated[list, operator.add]  # 检索到的源文档列表
    analyst: Analyst  # 当前进行访谈的分析师对象
    interview: str  # 完整的访谈记录文本
    sections: list  # 访谈摘要小节列表


class ResearchGraphState(TypedDict):
    """研究图状态管理类"""
    topic: str  # 研究主题
    max_analysts: int  # 分析师数量上限
    human_analyst_feedback: str  # 人类反馈信息
    analysts: List[Analyst]  # 分析师列表
    sections: Annotated[list, operator.add]  # 报告小节列表
    introduction: str  # 最终报告的引言部分
    content: str  # 最终报告的主体内容
    conclusion: str  # 最终报告的结论部分
    final_report: str  # 完整的最终报告


## 提示词模板

analyst_instructions = """你需要创建一组 AI 分析师人设。请严格遵循以下指引：

1. 先审阅研究主题：
{topic}

2. 查看（可选的）编辑反馈，它将指导分析师的人设创建：

{human_analyst_feedback}

3. 基于上述文档与/或反馈，识别最值得关注的主题。

4. 选出前 {max_analysts} 个主题。

5. 为每个主题分配一位分析师。"""

question_instructions = """你是一名分析师，需要通过访谈专家来了解一个具体主题。

你的目标是提炼与该主题相关的「有趣且具体」的洞见。

1. 有趣（Interesting）：让人感到意外或非显而易见的观点。

2. 具体（Specific）：避免泛泛而谈，包含专家提供的具体案例或细节。

以下是你的关注主题与目标设定：{goals}

请先用符合你人设的名字进行自我介绍，然后提出你的第一个问题。

持续追问，逐步深入，逐步完善你对该主题的理解。

当你认为信息已充分，请以这句话结束访谈：「非常感谢您的帮助!」

请始终保持与你的人设与目标一致的说话方式。"""

search_instructions = SystemMessage(content="""你将获得一段分析师与专家之间的对话。

你的目标是基于这段对话，为Web搜索生成一条结构良好的查询语句。

首先，通读整段对话。

特别关注分析师最后提出的问题。

将这个最终问题转化为结构良好的 Web 搜索查询。""")

answer_instructions = """你是一位被分析师访谈的专家。

以下是分析师的关注领域：{goals}。

你的目标是回答访谈者提出的问题。

回答问题时，请仅使用以下上下文：

{context}

回答须遵循如下要求：

1. 只使用上下文中提供的信息。

2. 不要引入上下文之外的信息，也不要做未在上下文明确说明的假设。

3. 上下文在每段文档顶部包含来源信息。

4. 在涉及具体论断时，请在相应内容旁标注引用来源编号。例如，针对来源 1 使用 [1]。

5. 在答案结尾处按顺序列出引用来源，如：[1] Source 1, [2] Source 2 等。

6. 若来源形如：<Document source="assistant/docs/llama3_1.pdf" page="7"/>，则在引用列表中只写：

[1] assistant/docs/llama3_1.pdf, page 7

并且不要再重复加中括号，也不要附加 Document source 前缀。"""

section_writer_instructions = """你是一名资深技术写作者。

你的任务是基于一组来源文档，撰写一段简洁、易读的报告小节。

1. 先分析来源文档内容：
- 每个文档的名称在文档开头，以 <Document 标签呈现。

2. 使用 Markdown 制作小节结构：
- 用 ## 作为小节标题
- 用 ### 作为小节内的小标题

3. 按结构撰写：
 a. 标题（## 头）
 b. 摘要（### 头）
 c. 参考来源（### 头）

4. 标题需要贴合分析师的关注点并具有吸引力：
{focus}

5. 关于摘要部分：
- 先给出与分析师关注点相关的背景/上下文
- 强调访谈中获得的新颖、有趣或令人意外的洞见
- 使用到来源文档时，按使用顺序创建编号
- 不要提及访谈者或专家的名字
- 控制在约 400 字以内
- 在报告正文中使用数字引用（如 [1]、[2]），基于来源文档信息
- **重要：生成的小节内容必须全部使用中文，所有内容都必须是中文输出**

6. 在参考来源部分：
- 列出报告中使用到的全部来源
- 给出完整链接或具体文档路径
- 每个来源单独一行；在行尾加两个空格以产生 Markdown 换行
- 参考格式：

### Sources
[1] 链接或文档名
[2] 链接或文档名

7. 合并重复来源。例如以下是不正确的：

[3] https://ai.meta.com/blog/meta-llama-3-1/
[4] https://ai.meta.com/blog/meta-llama-3-1/

应去重为：

[3] https://ai.meta.com/blog/meta-llama-3-1/

8. 最终检查：
- 确保报告结构符合要求
- 标题前不要有任何前言
- 检查是否遵循了全部规范"""

report_writer_instructions = """你是一名技术写作者，正在为如下主题撰写报告：

{topic}

你拥有一支分析师团队。每位分析师完成了两件事：

1. 围绕一个具体子主题，访谈了一位专家。
2. 将发现写成一份备忘录（memo）。

你的任务：

1. 你将收到分析师们的备忘录集合。
2. 仔细思考每份备忘录的洞见。
3. 将它们整合为简洁的总体总结，串联起所有备忘录的中心观点。
4. 把每份备忘录的关键信息归纳成一个连贯的单一叙述。

**重要要求：生成的报告必须全部使用中文，所有内容都必须是中文输出，包括标题、正文、术语解释等。对于特殊的英文术语，可以在中文后面加上英文标注。**

报告格式要求：

1. 使用 Markdown 格式。
2. 报告不要有任何前言。
3. 不使用任何小标题。
4. 报告以一个标题开头：## Insights
5. 报告中不要提及任何分析师的名字。
6. 保留备忘录中的引用标注（如 [1]、[2]）。
7. 汇总最终来源列表，并以 `## Sources` 作为小节标题。
8. 按顺序列出来源且不要重复。

[1] Source 1
[2] Source 2

以下是分析师提供的备忘录，请基于此撰写报告：

{context}"""

intro_conclusion_instructions = """你是一名技术写作者，正在完成主题为 {topic} 的报告。

你将获得报告的全部小节。

你的任务是撰写简洁而有说服力的引言或结论。

由用户告知写引言还是结论。

两者均不需要任何前言。

目标约 100 字：
- 引言：精炼预览各小节要点
- 结论：精炼回顾各小节要点

使用 Markdown 格式。

**重要要求：生成的报告必须全部使用中文，所有内容都必须是中文输出，包括标题、正文、术语解释等。对于特殊的英文术语，可以在中文后面加上英文标注。**

引言要求：创建一个有吸引力的标题，并用 # 作为标题头。

引言小节标题使用：## 引言

结论小节标题使用：## 结论

撰写时可参考以下小节内容：{formatted_str_sections}"""


## 初始化模型和工具

# 初始化聊天模型
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 初始化搜索工具
tavily_search = TavilySearchResults(max_results=3)


## 节点函数定义

def create_analysts(state: GenerateAnalystsState):
    """创建分析师人设"""
    topic = state['topic']
    max_analysts = state['max_analysts']
    human_analyst_feedback = state.get('human_analyst_feedback', '')

    structured_llm = llm.with_structured_output(Perspectives)
    system_message = analyst_instructions.format(
        topic=topic,
        human_analyst_feedback=human_analyst_feedback,
        max_analysts=max_analysts
    )

    analysts = structured_llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content="生成分析师集合。")
    ])

    return {"analysts": analysts.analysts}


def human_feedback(state: GenerateAnalystsState):
    """人机协同中断点节点"""
    pass


def should_continue(state: GenerateAnalystsState):
    """条件路由函数：决定工作流的下一步执行"""
    human_analyst_feedback = state.get('human_analyst_feedback', None)
    if human_analyst_feedback:
        return "create_analysts"
    return END


def generate_question(state: InterviewState):
    """生成访谈问题"""
    analyst = state["analyst"]
    messages = state["messages"]

    system_message = question_instructions.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)

    return {"messages": [question]}


def search_web(state: InterviewState):
    """通过Web搜索检索相关文档"""
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state['messages'])

    search_docs = tavily_search.invoke(search_query.search_query)

    formatted_search_docs = "\n\n---\n\n".join([
        f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
        for doc in search_docs
    ])

    return {"context": [formatted_search_docs]}


def search_baike(state: InterviewState):
    """通过百科（百度百科）检索相关文档"""
    structured_llm = llm.with_structured_output(SearchQuery)
    search_query = structured_llm.invoke([search_instructions] + state['messages'])

    search_docs = BaiduBaikeLoader(
        query=search_query.search_query,
        load_max_docs=2
    ).load()

    formatted_search_docs = "\n\n---\n\n".join([
        f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
        for doc in search_docs
    ])

    return {"context": [formatted_search_docs]}


def generate_answer(state: InterviewState):
    """生成专家回答"""
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    system_message = answer_instructions.format(
        goals=analyst.persona,
        context=context
    )

    answer = llm.invoke([SystemMessage(content=system_message)] + messages)
    answer.name = "expert"

    return {"messages": [answer]}


def save_interview(state: InterviewState):
    """保存访谈内容"""
    messages = state["messages"]
    interview = get_buffer_string(messages)
    return {"interview": interview}


def route_messages(state: InterviewState, name: str = "expert"):
    """消息路由函数：决定访谈流程的下一步"""
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)

    num_responses = len([
        m for m in messages
        if isinstance(m, AIMessage) and m.name == name
    ])

    if num_responses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]
    if "非常感谢您的帮助!" in last_question.content:
        return 'save_interview'

    return "ask_question"


def write_section(state: InterviewState):
    """生成报告小节"""
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    system_message = section_writer_instructions.format(focus=analyst.description)
    section = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=f"使用这些来源撰写你的小节: {context}")
    ])

    return {"sections": [section.content]}


def initiate_all_interviews(state: ResearchGraphState):
    """启动所有并行访谈的Map步骤"""
    human_analyst_feedback = state.get('human_analyst_feedback')
    if human_analyst_feedback:
        return "create_analysts"
    else:
        topic = state["topic"]
        return [
            Send("conduct_interview", {
                "analyst": analyst,
                "messages": [HumanMessage(
                    content=f"所以你说你在写一篇关于{topic}的文章?"
                )]
            })
            for analyst in state["analysts"]
        ]


def write_report(state: ResearchGraphState):
    """生成最终报告主体内容（Reduce步骤）"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    system_message = report_writer_instructions.format(
        topic=topic,
        context=formatted_str_sections
    )

    report = llm.invoke([
        SystemMessage(content=system_message),
        HumanMessage(content=f"基于这些备忘录撰写一份报告。")
    ])

    return {"content": report.content}


def write_introduction(state: ResearchGraphState):
    """生成报告引言"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    instructions = intro_conclusion_instructions.format(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )

    intro = llm.invoke([
        instructions,
        HumanMessage(content=f"撰写报告引言")
    ])

    return {"introduction": intro.content}


def write_conclusion(state: ResearchGraphState):
    """生成报告结论"""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    instructions = intro_conclusion_instructions.format(
        topic=topic,
        formatted_str_sections=formatted_str_sections
    )

    conclusion = llm.invoke([
        instructions,
        HumanMessage(content=f"撰写报告结论")
    ])

    return {"conclusion": conclusion.content}


def finalize_report(state: ResearchGraphState):
    """最终报告生成函数（Reduce步骤的最终阶段）"""
    content = state["content"]

    if content.startswith("## Insights"):
        content = content.strip("## Insights")

    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = (
        state["introduction"] +
        "\n\n---\n\n" +
        content +
        "\n\n---\n\n" +
        state["conclusion"]
    )

    if sources is not None:
        final_report += "\n\n## Sources\n" + sources

    return {"final_report": final_report}


## 构建访谈子图

interview_builder = StateGraph(InterviewState)

# 添加各个功能节点
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_baike", search_baike)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

# 定义工作流连接关系
interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_baike")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_baike", "answer_question")

interview_builder.add_conditional_edges(
    "answer_question",
    route_messages,
    ['ask_question', 'save_interview']
)

interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

# 编译访谈工作流
interview_memory = MemorySaver()
interview_graph = interview_builder.compile(checkpointer=interview_memory).with_config(
    run_name="Conduct Interviews"
)


## 构建完整的研究图

builder = StateGraph(ResearchGraphState, config_schema=configuration.Configuration)

# 添加所有功能节点
builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("conduct_interview", interview_graph)
builder.add_node("write_report", write_report)
builder.add_node("write_introduction", write_introduction)
builder.add_node("write_conclusion", write_conclusion)
builder.add_node("finalize_report", finalize_report)

# 定义工作流连接关系
builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")

builder.add_conditional_edges(
    "human_feedback",
    initiate_all_interviews,
    ["create_analysts", "conduct_interview"]
)

builder.add_edge("conduct_interview", "write_report")
builder.add_edge("conduct_interview", "write_introduction")
builder.add_edge("conduct_interview", "write_conclusion")

builder.add_edge(
    ["write_conclusion", "write_report", "write_introduction"],
    "finalize_report"
)
builder.add_edge("finalize_report", END)

# 编译完整的研究图工作流
memory = MemorySaver()
graph = builder.compile(
    interrupt_before=['human_feedback'],
    checkpointer=memory
)
