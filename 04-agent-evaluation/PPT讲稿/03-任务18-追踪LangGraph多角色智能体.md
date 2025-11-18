# 任务18：追踪LangGraph多角色智能体

**时长：** 40分钟  
**难度：** ⭐⭐⭐⭐☆  
**交付成果：** 多角色智能体监控方案

---

## 第一部分：LangGraph基础概念 (10分钟)

### 🎯 什么是LangGraph？

**LangGraph = LangChain + Graph（图）结构**

```
传统LLM应用：
输入 → LLM → 输出
（单次调用，线性流程）

LangGraph应用：
        ┌─→ 节点A ─→ 节点B ─┐
输入 ─→ ┤                  ├─→ 输出
        └─→ 节点C ─→ 节点D ─┘
（多节点，图形工作流，可循环）
```

### 🏗️ 核心概念

#### 1. StateGraph（状态图）
```python
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

# 定义状态结构
class State(TypedDict):
    messages: list  # 对话历史
    user_info: dict  # 用户信息
    context: str    # 上下文

# 创建状态图
graph = StateGraph(State)
```

**作用：** 管理整个工作流的状态

#### 2. Node（节点）
```python
def node_function(state: State):
    """节点函数：接收状态，返回更新"""
    # 处理逻辑
    new_data = process(state)
    # 返回状态更新
    return {"context": new_data}

# 添加节点
graph.add_node("my_node", node_function)
```

**作用：** 执行具体的业务逻辑

#### 3. Edge（边）
```python
# 无条件边：总是执行
graph.add_edge("node_a", "node_b")

# 条件边：根据函数返回值选择下一个节点
graph.add_conditional_edges(
    "classifier",
    route_function,  # 返回下一个节点名称
    {
        "safe": "process_safe",
        "unsafe": "handle_unsafe"
    }
)
```

**作用：** 定义节点之间的流转关系

---

### 📊 LangGraph vs LangChain

| 特性 | LangChain | LangGraph |
|:---|:---|:---|
| **结构** | 线性链 | 图结构 |
| **流程** | 顺序执行 | 可分支、循环 |
| **状态** | 隐式传递 | 显式管理 |
| **复杂度** | 简单场景 | 复杂工作流 |
| **典型应用** | 简单问答、RAG | 多步推理、Agent |

---

## 第二部分：LangGraph集成Langfuse (10分钟)

### 🚀 三种集成方式

#### 方式1：使用CallbackHandler

```python
from langfuse.langchain import CallbackHandler
from langgraph.graph import StateGraph

langfuse_handler = CallbackHandler()

# 编译图
graph = state_graph.compile()

# 执行时添加callbacks
result = graph.invoke(
    initial_state,
    config={"callbacks": [langfuse_handler]}
)
```

**特点：** 简单，适合快速集成

#### 方式2：使用@observe装饰器

```python
from langfuse import observe

@observe()
def my_node(state):
    """被追踪的节点函数"""
    # 节点逻辑
    return updated_state

# 添加被装饰的节点
graph.add_node("my_node", my_node)
```

**特点：** 精细控制，可自定义span

#### 方式3：预配置图对象（Server模式）

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# 编译时就配置callback
graph = state_graph.compile().with_config(
    {"callbacks": [langfuse_handler]}
)

# 之后的所有invoke都会自动追踪
result = graph.invoke(initial_state)
```

**特点：** 适合生产环境，无需重复配置

---

## 第三部分：实战案例 - 邮件处理智能体 (15分钟)

### 🎯 业务场景

**背景：** 为蝙蝠侠的管家Alfred构建智能邮件助手

**需求：**
1. 读取邮件
2. 识别垃圾邮件
3. 合法邮件生成回复草稿
4. 通知主人

### 🏗️ 系统架构

```
┌─────────────────────────────────────┐
│         邮件处理工作流              │
├─────────────────────────────────────┤
│                                     │
│   START                             │
│     ↓                               │
│   读取邮件                          │
│     ↓                               │
│   分类邮件 ←─ LLM判断               │
│     ├─────┬─────┐                  │
│     ↓     ↓     ↓                  │
│   垃圾  正常   紧急                 │
│     ↓     ↓     ↓                  │
│   标记  起草  优先                  │
│     ↓     ↓     ↓                  │
│   通知主人 ←─────┘                  │
│     ↓                               │
│   END                               │
│                                     │
└─────────────────────────────────────┘
```

### 📝 代码实现

#### 步骤1：定义状态结构

```python
from typing import TypedDict, Optional, List, Dict, Any

class EmailState(TypedDict):
    """邮件处理状态"""
    email: Dict[str, Any]           # 原始邮件
    is_spam: Optional[bool]         # 是否垃圾邮件
    spam_reason: Optional[str]      # 垃圾邮件原因
    email_category: Optional[str]   # 邮件分类
    draft_response: Optional[str]   # 回复草稿
    messages: List[Dict[str, Any]]  # LLM对话历史
```

#### 步骤2：定义节点函数

```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o", temperature=0)

def read_email(state: EmailState):
    """入口节点：读取邮件"""
    email = state["email"]
    print(f"📧 处理来自 {email['sender']} 的邮件")
    print(f"📋 主题: {email['subject']}")
    return {}  # 不修改状态

def classify_email(state: EmailState):
    """分类节点：使用LLM判断邮件类型"""
    email = state["email"]
    
    # 构造提示词
    prompt = f"""
请分析以下邮件，判断是垃圾邮件（SPAM）还是正常邮件（HAM）。

发件人：{email['sender']}
主题：{email['subject']}
正文：{email['body']}

只返回一个单词：SPAM 或 HAM
"""
    
    # 调用LLM
    response = model.invoke([{"role": "user", "content": prompt}])
    response_text = response.content.lower()
    
    # 判断结果
    is_spam = "spam" in response_text and "ham" not in response_text
    
    return {
        "is_spam": is_spam,
        "messages": state.get("messages", []) + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response.content}
        ]
    }

def handle_spam(state: EmailState):
    """处理垃圾邮件"""
    print("🚮 邮件已标记为垃圾邮件")
    return {}

def drafting_response(state: EmailState):
    """起草回复"""
    email = state["email"]
    
    prompt = f"""
请以Alfred管家的口吻，为以下邮件起草回复。

发件人：{email['sender']}
主题：{email['subject']}
正文：{email['body']}

回复要求：礼貌、专业、简洁
"""
    
    response = model.invoke([{"role": "user", "content": prompt}])
    
    return {
        "draft_response": response.content,
        "messages": state.get("messages", []) + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response.content}
        ]
    }

def notify_mr_wayne(state: EmailState):
    """通知主人"""
    email = state["email"]
    print("="*50)
    print(f"Sir, you've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print("\nDraft response:")
    print("-"*50)
    print(state["draft_response"])
    print("="*50)
    return {}
```

#### 步骤3：构建图结构

```python
from langgraph.graph import StateGraph, START, END

# 创建状态图
email_graph = StateGraph(EmailState)

# 添加节点
email_graph.add_node("read_email", read_email)
email_graph.add_node("classify_email", classify_email)
email_graph.add_node("handle_spam", handle_spam)
email_graph.add_node("drafting_response", drafting_response)
email_graph.add_node("notify_mr_wayne", notify_mr_wayne)

# 定义路由逻辑
def route_email(state: EmailState) -> str:
    """根据分类结果选择下一步"""
    if state["is_spam"]:
        return "spam"
    else:
        return "legitimate"

# 添加边
email_graph.add_edge(START, "read_email")
email_graph.add_edge("read_email", "classify_email")

# 添加条件边
email_graph.add_conditional_edges(
    "classify_email",
    route_email,
    {
        "spam": "handle_spam",
        "legitimate": "drafting_response"
    }
)

# 添加结束边
email_graph.add_edge("handle_spam", END)
email_graph.add_edge("drafting_response", "notify_mr_wayne")
email_graph.add_edge("notify_mr_wayne", END)

# 编译图
compiled_graph = email_graph.compile()
```

#### 步骤4：执行并追踪

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# 准备测试邮件
legitimate_email = {
    "sender": "京东客服",
    "subject": "关于你的订单发票",
    "body": "尊敬的韦恩先生，你的发票已开具..."
}

spam_email = {
    "sender": "某数字货币项目",
    "subject": "限时暴涨100倍！",
    "body": "立即加入，稳赚不赔..."
}

# 处理正常邮件
print("处理正常邮件：")
result1 = compiled_graph.invoke(
    {
        "email": legitimate_email,
        "is_spam": None,
        "draft_response": None,
        "messages": []
    },
    config={"callbacks": [langfuse_handler]}
)

print("\n处理垃圾邮件：")
result2 = compiled_graph.invoke(
    {
        "email": spam_email,
        "is_spam": None,
        "draft_response": None,
        "messages": []
    },
    config={"callbacks": [langfuse_handler]}
)
```

### 📊 在Langfuse中的追踪结构

```
Trace: email-processing
├── Span: read_email
│   ├── input: {email: {...}}
│   └── latency: 0.001s
├── Span: classify_email
│   ├── Span: ChatOpenAI (Generation)
│   │   ├── model: gpt-4o
│   │   ├── tokens: 150
│   │   ├── cost: $0.0008
│   │   └── output: "HAM"
│   └── latency: 1.2s
├── Span: drafting_response
│   ├── Span: ChatOpenAI (Generation)
│   │   ├── model: gpt-4o
│   │   ├── tokens: 300
│   │   ├── cost: $0.0015
│   │   └── output: "Dear..."
│   └── latency: 2.3s
└── Span: notify_mr_wayne
    └── latency: 0.001s

Total Cost: $0.0023
Total Latency: 3.5s
```

---

## 第四部分：高级功能 - 多智能体协作 (5分钟)

### 🤝 场景：主Agent调用子Agent

```python
from langfuse import get_client

langfuse = get_client()

# 生成共享的trace_id
shared_trace_id = langfuse.create_trace_id()

# 子Agent封装为工具
@tool
def research_agent(question: str):
    """研究Agent：深度研究问题"""
    with langfuse.start_as_current_span(
        name="sub-research-agent",
        trace_context={"trace_id": shared_trace_id}
    ) as span:
        span.update_trace(input=question)
        
        # 调用子Agent的图
        result = sub_agent.invoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"callbacks": [langfuse_handler]}
        )
        
        span.update_trace(output=result)
        return result

# 主Agent使用工具
main_agent = create_react_agent(
    model=ChatOpenAI(model="gpt-4o"),
    tools=[research_agent]  # 子Agent作为工具
)

# 执行主Agent
with langfuse.start_as_current_span(
    name="main-agent",
    trace_context={"trace_id": shared_trace_id}
) as span:
    span.update_trace(input="什么是Langfuse？")
    
    result = main_agent.invoke(
        {"messages": [{"role": "user", "content": "什么是Langfuse？"}]},
        config={"callbacks": [langfuse_handler]}
    )
    
    span.update_trace(output=result)
```

**Langfuse中的嵌套追踪：**
```
Trace (shared_trace_id)
├── Span: main-agent
│   ├── ReAct思考：需要调用研究工具
│   ├── Tool Call: research_agent
│   │   └── Span: sub-research-agent
│   │       ├── 子图节点1
│   │       ├── 子图节点2
│   │       └── 子图节点3
│   └── 最终回答
```

---

## 💡 关键要点总结

### LangGraph特点
```
✅ 图结构工作流
✅ 显式状态管理
✅ 支持分支和循环
✅ 适合复杂Agent
```

### Langfuse集成
```
✅ CallbackHandler集成
✅ @observe装饰器
✅ 预配置图对象
✅ 多智能体追踪
```

### 追踪价值
```
📊 可视化工作流
🐛 调试复杂逻辑
💰 成本精确分析
⏱️ 性能瓶颈定位
```

---

## 🎯 实战练习

### 练习1：简单LangGraph
创建一个3节点的LangGraph并追踪。

### 练习2：条件分支
实现带条件分支的工作流。

### 练习3：性能优化
分析邮件处理智能体的性能瓶颈。

### 练习4：多智能体
构建主Agent调用子Agent的系统。

---

**下一节：任务19 - 构建LLM安全监控系统**


