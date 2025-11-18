# 任务17：Langfuse集成实战 - 追踪OpenAI和LangChain调用

**时长：** 30分钟  
**难度：** ⭐⭐⭐☆☆  
**交付成果：** 基础集成代码和追踪方案

---

## 第一部分：OpenAI SDK集成 (15分钟)

### 🎯 集成目标

**只需改一行代码，就能获得完整的可观测性！**

```python
# 原来的导入方式
# from openai import OpenAI

# 新的导入方式（自动集成Langfuse）
from langfuse.openai import openai
```

### 🚀 快速开始

#### 步骤1：安装依赖

```bash
pip install langfuse==3.3.0 openai==1.107.0
```

#### 步骤2：配置环境变量

```python
import os
import getpass

# OpenAI配置
os.environ["OPENAI_API_KEY"] = getpass.getpass("OPENAI_API_KEY: ")
os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1"  # 可选

# Langfuse配置
os.environ["LANGFUSE_PUBLIC_KEY"] = getpass.getpass("LANGFUSE_PUBLIC_KEY: ")
os.environ["LANGFUSE_SECRET_KEY"] = getpass.getpass("LANGFUSE_SECRET_KEY: ")
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"
```

#### 步骤3：使用集成后的OpenAI客户端

```python
from langfuse.openai import openai

# 完全兼容原生OpenAI SDK的所有功能
completion = openai.chat.completions.create(
    # 📝 Langfuse特有参数：给这次调用起个名字
    name="calculator-demo",
    
    # 🤖 标准OpenAI参数
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一个精确的计算器"},
        {"role": "user", "content": "1 + 1 = "}
    ],
    temperature=0,
    
    # 🏷️ Langfuse元数据：自定义标签和分类
    metadata={
        "task_type": "calculator",
        "difficulty": "easy",
        "user_id": "demo_user"
    }
)

print(f"计算结果: {completion.choices[0].message.content}")
```

**输出：**
```
计算结果: 2
```

### 📊 在Langfuse中查看

访问 https://cloud.langfuse.com/traces

**你将看到：**
1. **Trace信息**
   - name: "calculator-demo"
   - user_id: "demo_user"
   - 执行时间和延迟

2. **Generation详情**
   - model: "gpt-4o"
   - input tokens: ~25
   - output tokens: ~1
   - cost: ~$0.0001

3. **自定义元数据**
   - task_type: "calculator"
   - difficulty: "easy"

---

### 🖼️ 图像分析示例

```python
# 多模态调用同样适用
completion = openai.chat.completions.create(
    name="image-analysis-demo",
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "你是一个图像分析AI，描述图像的主要内容。"
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "这张图片描绘了什么？"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ],
    metadata={
        "task_type": "image_analysis",
        "image_source": "user_upload"
    }
)

print(f"分析结果: {completion.choices[0].message.content}")
```

---

### 🌊 流式输出追踪

```python
# 流式输出也能完整追踪
print("AI回复：", end="")

completion = openai.chat.completions.create(
    name="streaming-joke-demo",
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是一位幽默的喜剧演员"},
        {"role": "user", "content": "讲一个关于程序员的笑话"}
    ],
    stream=True,  # 开启流式输出
    metadata={"streaming": True}
)

for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

print("\n✅ 完成!")
```

**Langfuse会自动：**
- 收集所有流式片段
- 计算总token数
- 记录完整的输出内容

---

### ⚡ 异步调用追踪

```python
from langfuse.openai import AsyncOpenAI
import asyncio

async_client = AsyncOpenAI()

async def async_calculation():
    completion = await async_client.chat.completions.create(
        name="async-calculator-demo",
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是计算器"},
            {"role": "user", "content": "100 + 200 = "}
        ],
        temperature=0,
        metadata={"concurrency": "high"}
    )
    return completion.choices[0].message.content

# 运行异步函数
result = await async_calculation()
print(f"异步计算结果: {result}")
```

---

### 🔧 函数调用（Function Calling）

```python
from pydantic import BaseModel
from typing import List
import json

# 定义函数返回值结构
class SolutionSteps(BaseModel):
    title: str
    steps: List[str]

# 使用函数调用
response = openai.chat.completions.create(
    name="function-calling-demo",
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "如何做番茄炒蛋？"}
    ],
    functions=[
        {
            "name": "get_recipe_steps",
            "description": "返回菜谱的制作步骤",
            "parameters": SolutionSteps.model_json_schema()
        }
    ],
    function_call={"name": "get_recipe_steps"}
)

# 解析函数调用结果
function_args = json.loads(
    response.choices[0].message.function_call.arguments
)
print(f"菜谱：{function_args['title']}")
for i, step in enumerate(function_args['steps'], 1):
    print(f"{i}. {step}")
```

**Langfuse中的函数调用追踪：**
- 记录函数定义
- 记录函数参数
- 记录函数返回值
- 标记为特殊的Generation类型

---

### 🏷️ 高级功能：自定义元数据

```python
completion = openai.chat.completions.create(
    name="advanced-metadata-demo",
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "你是助手"},
        {"role": "user", "content": "你好"}
    ],
    metadata={
        # Langfuse特殊字段
        "langfuse_session_id": "session_123",  # 会话ID
        "langfuse_user_id": "user_456",        # 用户ID
        "langfuse_tags": ["greeting", "test"], # 标签列表
        
        # 自定义字段
        "environment": "production",
        "version": "v1.0.0",
        "feature": "chat"
    }
)
```

**在Langfuse中的好处：**
- 按session/user聚合分析
- 按tags过滤和搜索
- 按自定义字段分组统计

---

### 📋 将多次调用归并到同一个Trace

```python
from langfuse import observe
from langfuse.openai import openai

@observe()  # 装饰器创建顶层trace
def multi_step_task(country: str):
    # 第一步：查询首都
    capital_response = openai.chat.completions.create(
        name="get-capital",
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是地理老师"},
            {"role": "user", "content": f"{country}的首都是？"}
        ]
    )
    capital = capital_response.choices[0].message.content
    
    # 第二步：写关于首都的诗
    poem_response = openai.chat.completions.create(
        name="write-poem",
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "你是诗人"},
            {"role": "user", "content": f"写一首关于{capital}的诗"}
        ],
        temperature=0.9
    )
    
    return poem_response.choices[0].message.content

# 调用
result = multi_step_task("中国")
print(result)
```

**Langfuse中的层级结构：**
```
Trace: multi_step_task
├── Span: get-capital (Generation)
│   ├── input: "中国的首都是？"
│   └── output: "北京"
└── Span: write-poem (Generation)
    ├── input: "写一首关于北京的诗"
    └── output: "..."
```

---

## 第二部分：LangChain集成 (15分钟)

### 🎯 为什么要集成LangChain？

**LangChain的优势：**
- 🔗 链式调用（Chain）
- 🤖 智能体（Agent）
- 🛠️ 工具集成（Tools）
- 💾 记忆管理（Memory）
- 📚 文档检索（RAG）

**集成Langfuse的价值：**
- 追踪复杂的链式调用
- 监控Agent的决策过程
- 分析工具使用情况
- 优化RAG系统性能

---

### 🚀 LangChain集成步骤

#### 步骤1：安装依赖

```bash
pip install langfuse==3.3.0 \
            langchain==0.3.27 \
            langchain-openai==0.3.31
```

#### 步骤2：初始化Langfuse回调处理器

```python
from langfuse.langchain import CallbackHandler

# 初始化回调处理器
langfuse_handler = CallbackHandler()

# 使用方式：在调用时添加config参数
# chain.invoke(..., config={"callbacks": [langfuse_handler]})
```

---

### 📝 示例1：简单的LangChain LCEL

**LCEL = LangChain Expression Language（LangChain表达式语言）**

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langfuse.langchain import CallbackHandler

# 初始化回调
langfuse_handler = CallbackHandler()

# 创建提示模板
prompt = ChatPromptTemplate.from_template("{person}来自哪座城市？")

# 创建模型
model = ChatOpenAI(model="gpt-4o", temperature=0)

# 创建输出解析器
output_parser = StrOutputParser()

# 构建链
chain = prompt | model | output_parser

# 执行链并追踪
result = chain.invoke(
    {"person": "苏东坡"},
    config={"callbacks": [langfuse_handler]}
)

print(f"结果: {result}")  # 输出: 眉山或杭州
```

**Langfuse中的追踪结构：**
```
Trace
├── Span: ChatPromptTemplate
│   ├── input: {"person": "苏东坡"}
│   └── output: "苏东坡来自哪座城市？"
├── Span: ChatOpenAI (Generation)
│   ├── input: "苏东坡来自哪座城市？"
│   ├── output: "眉山"
│   ├── tokens: 35
│   └── cost: $0.0002
└── Span: StrOutputParser
    ├── input: AIMessage(content="眉山")
    └── output: "眉山"
```

---

### 🔗 示例2：复杂的多步骤链

```python
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

langfuse_handler = CallbackHandler()

# 第一个提示：查询城市
prompt1 = ChatPromptTemplate.from_template("{person}来自哪座城市？")

# 第二个提示：查询国家
prompt2 = ChatPromptTemplate.from_template(
    "城市{city}位于哪个国家？请用{language}回答"
)

model = ChatOpenAI(model="gpt-4o", temperature=0)

# 第一个链：人名 → 城市
chain1 = prompt1 | model | StrOutputParser()

# 第二个链：城市 + 语言 → 国家
chain2 = (
    {
        "city": chain1,  # 使用chain1的输出
        "language": itemgetter("language")  # 从输入提取language
    }
    | prompt2
    | model
    | StrOutputParser()
)

# 执行复杂链
result = chain2.invoke(
    {"person": "莫言", "language": "英文"},
    config={"callbacks": [langfuse_handler]}
)

print(f"结果: {result}")
```

**Langfuse中的嵌套追踪：**
```
Trace
├── Span: chain2
│   ├── Span: chain1
│   │   ├── prompt1: "莫言来自哪座城市？"
│   │   ├── model: "高密"
│   │   └── parser: "高密"
│   ├── Span: RunnableParallel
│   │   ├── city: "高密" (from chain1)
│   │   └── language: "英文" (from input)
│   ├── Span: prompt2
│   │   └── "城市高密位于哪个国家？请用英文回答"
│   ├── Span: model (Generation)
│   │   └── "China"
│   └── Span: parser
│       └── "China"
```

---

### 🏃 示例3：Runnable方法追踪

```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# 假设chain已定义（同上）
chain = prompt | model | StrOutputParser()

# 1. 同步调用
result = chain.invoke(
    {"person": "鲁迅"},
    config={"callbacks": [langfuse_handler]}
)

# 2. 异步调用
result = await chain.ainvoke(
    {"person": "巴金"},
    config={"callbacks": [langfuse_handler]}
)

# 3. 批处理
results = chain.batch([
    {"person": "老舍"},
    {"person": "茅盾"}
], config={"callbacks": [langfuse_handler]})

# 4. 流式输出
for chunk in chain.stream(
    {"person": "钱钟书"},
    config={"callbacks": [langfuse_handler]}
):
    print(chunk, end="", flush=True)
```

**每种方法都会在Langfuse中创建独立的Trace。**

---

### 📚 示例4：检索增强生成（RAG）

```python
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()

# 1. 加载文档
loader = TextLoader("state_of_the_union.txt")
documents = loader.load()

# 2. 分割文档
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# 3. 创建向量数据库
embeddings = OpenAIEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)

# 4. 创建检索问答链
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# 5. 执行问答并追踪
result = qa_chain.invoke(
    "美国国情咨文的核心主题是什么？",
    config={"callbacks": [langfuse_handler]}
)

print(f"答案: {result['result']}")
print(f"来源: {len(result['source_documents'])}个文档")
```

**Langfuse中的RAG追踪：**
```
Trace: RetrievalQA
├── Span: Retriever
│   ├── input: "美国国情咨文的核心主题是什么？"
│   ├── output: [Document1, Document2, Document3]
│   └── latency: 0.2s
├── Span: StuffDocumentsChain
│   ├── input: query + documents
│   └── Span: LLMChain
│       ├── Span: PromptTemplate
│       │   └── 将问题和文档组合成提示
│       ├── Span: ChatOpenAI (Generation)
│       │   ├── tokens: 1500
│       │   ├── cost: $0.003
│       │   └── latency: 2.5s
│       └── output: "核心主题是..."
```

---

## 💡 关键要点总结

### OpenAI SDK集成
```
✅ 只需改一行导入代码
✅ 完全兼容原生SDK
✅ 自动追踪所有调用
✅ 支持流式、异步、函数调用
```

### LangChain集成
```
✅ 使用CallbackHandler
✅ 在config中添加callbacks
✅ 追踪复杂的链式调用
✅ 支持所有Runnable方法
```

### 追踪数据的价值
```
📊 可视化执行流程
⏱️ 识别性能瓶颈
💰 精确计算成本
🐛 快速定位问题
```

---

## 🎯 实战练习

### 练习1：基础集成
为你的现有OpenAI调用添加Langfuse追踪。

### 练习2：LangChain链
创建一个包含至少3个步骤的LangChain，并追踪执行过程。

### 练习3：性能分析
运行同一个提示10次，在Langfuse中分析延迟分布。

### 练习4：成本优化
对比gpt-4o和gpt-3.5-turbo的成本差异。

---

**下一节：任务18 - 追踪LangGraph多角色智能体**


