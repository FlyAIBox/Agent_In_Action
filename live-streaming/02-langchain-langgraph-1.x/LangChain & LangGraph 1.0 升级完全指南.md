# LangChain & LangGraph 1.0 升级完全指南
## 从 0.x 到 1.0 的生产级跃升

---

## 📋 课程大纲

### 第1部分：核心痛点与解决方案
### 第2部分：LangChain 1.0 主要变化
### 第3部分：LangGraph 1.0 主要变化  
### 第4部分：关键迁移场景
### 第5部分：实战演练
### 第6部分：实际应用场景

---

## 🎯 第1部分：核心痛点与解决方案

---

## 核心痛点 #1: API 碎片化

### 🔴 **问题现状**
- 不同版本间API不一致
- `langgraph.prebuilt` vs `langchain.agents` 混乱
- 缺乏统一的Agent构建标准
- 开发者需要频繁查阅文档

### 💡 **1.0 解决方案**
```python
# ❌ 旧版 - 多处导入，职责不清
from langgraph.prebuilt import create_react_agent
from langchain.messages import SystemMessage

# ✅ 新版 - 统一入口，职责明确
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="你是助手",  # 更直观
    checkpointer=checkpointer
)
```

---

## 核心痛点 #2: 跨提供商兼容性差

### 🔴 **问题现状**
- 不同LLM提供商返回格式不统一
- OpenAI vs Anthropic vs Google 需要写不同解析代码
- 推理过程(thinking)、引用等高级特性访问困难
- 切换模型需要大量代码重构

### 💡 **1.0 解决方案：Standard Content Blocks**
```python
# ✅ 统一的内容访问方式
response = model.invoke("问题")

for block in response.content_blocks:
    match block["type"]:
        case "text":
            print(f"回答: {block['text']}")
        case "reasoning":  # o1模型的思考过程
            print(f"推理: {block['reasoning']}")
        case "tool_call":
            print(f"工具: {block['name']}({block['args']})")
```

**支持的内容块类型**：`text` | `reasoning` | `tool_call` | `citation` | `image`

---

## 核心痛点 #3: 缺乏可扩展性

### 🔴 **问题现状**
- 横切关注点(日志、PII过滤)散落各处
- 代码重复，难以维护
- 无法优雅地注入自定义逻辑
- 调试困难

### 💡 **1.0 解决方案：Middleware 中间件**

| Hook | 时机 | 用途 |
|------|------|------|
| `before_agent` | Agent执行前 | 加载记忆、验证输入 |
| `before_model` | LLM调用前 | 更新prompts、裁剪消息 |
| `wrap_model_call` | 围绕LLM调用 | 拦截请求/响应、重试 |
| `wrap_tool_call` | 围绕工具调用 | 权限校验、日志 |
| `after_model` | LLM响应后 | 验证输出、应用守护规则 |
| `after_agent` | Agent完成后 | 保存结果、清理 |

```python
from langchain.agents.middleware import PIIMiddleware, before_model

@before_model
def log_middleware(state, runtime):
    print(f"处理 {len(state['messages'])} 条消息")
    return None

agent = create_agent(
    model, tools,
    middleware=[
        PIIMiddleware("email", strategy="redact"),
        log_middleware
    ]
)
```

---

## 核心痛点 #4: Human-in-the-Loop 不够灵活

### 🔴 **问题现状 (0.x)**
- 静态 `interrupt_before` 配置
- 无法基于运行时条件决定是否中断
- 恢复流程繁琐

```python
# ❌ 旧版 - 编译时就固定了中断点
graph = builder.compile(
    interrupt_before=["risky_action"]
)
```

### 💡 **1.0 解决方案：动态 interrupt()**

```python
# ✅ 新版 - 运行时动态决定
from langgraph.types import interrupt, Command

@tool
def risky_action():
    if needs_approval():  # 条件判断
        response = interrupt({
            "message": "需要批准",
            "action": "delete_database"
        })
        if not response["approved"]:
            return "操作取消"
    return "操作完成"

# 恢复执行
agent.invoke(
    Command(resume={"approved": True}),
    config=config
)
```

---

## 🎓 本节课你将掌握

### ✅ **核心技能**
1. **API 迁移能力**
   - 快速识别需要更新的代码
   - 掌握新旧API对应关系
   - 理解架构重组的设计思想

2. **新特性应用**
   - 使用 Content Blocks 实现提供商无关
   - 设计 Middleware 解决横切关注点
   - 实现灵活的 Human-in-the-Loop

3. **生产级实践**
   - Checkpointer 持久化策略
   - 结构化输出优化
   - 性能调优技巧

---

## 📦 第2部分：LangChain 1.0 主要变化

---

## 变化 1: `create_agent()` - 新的核心 API

### 🔄 **导入路径变化**
```python
# ❌ 旧版 (LangChain 0.x)
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools)

# ✅ 新版 (LangChain 1.0)
from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt="...")
```

### 📊 **参数对比**

| 特性 | 0.x `create_react_agent` | 1.0 `create_agent` |
|------|--------------------------|---------------------|
| **导入位置** | `langgraph.prebuilt` | `langchain.agents` |
| **系统提示** | `messages_modifier=SystemMessage()` | `system_prompt="..."` |
| **中间件** | ❌ 不支持 | ✅ `middleware=[]` |
| **架构决策** | LangGraph 负责 | LangChain 负责高级抽象 |

### ⚙️ **迁移步骤**
1. 更改导入：`langgraph.prebuilt` → `langchain.agents`
2. 更改函数名：`create_react_agent` → `create_agent`
3. 更改参数：`messages_modifier` → `system_prompt`
4. （可选）添加中间件：`middleware=[...]`

---

## 变化 2: Middleware - 可定制化的全新入口

### 🎯 **设计理念**
将横切关注点（日志、PII过滤、权限校验）从业务逻辑中解耦

### 🔧 **核心 Hooks**

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

# 内置中间件
agent = create_agent(
    model=model,
    tools=tools,
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True)
    ]
)
```

### 📝 **自定义中间件示例**

```python
from langchain.agents.middleware import before_model, after_model

@before_model
async def token_limit_middleware(state, runtime):
    """限制token数量"""
    messages = state["messages"]
    if len(messages) > 100:
        return {"messages": messages[-50:]}  # 保留最近50条
    return None

@after_model
async def safety_middleware(state, runtime):
    """内容安全检查"""
    last_message = state["messages"][-1]
    if contains_unsafe_content(last_message.content):
        return {"messages": [AIMessage("我无法回答这个问题")]}
    return None

agent = create_agent(
    model, tools,
    middleware=[
        token_limit_middleware,
        safety_middleware
    ]
)
```

---

## 变化 3: Standard Content Blocks

### 🔄 **跨提供商统一访问**

```python
# ✅ 新版 (LangChain 1.0) - 统一访问
response = model.invoke("问题")
for block in response.content_blocks:
    if block["type"] == "reasoning":
        print(f"推理: {block['reasoning']}")
    elif block["type"] == "text":
        print(f"回答: {block['text']}")
    elif block["type"] == "tool_call":
        print(f"工具调用: {block['name']}({block['args']})")

# ❌ 旧版 (0.x) - 依赖提供商特定的字段
# 需要针对不同提供商 (OpenAI、Anthropic 等) 写不同的解析代码
```

### 📋 **支持的内容块类型**

| 类型 | 说明 | 何时出现 |
|------|------|----------|
| `text` | 文本内容 | 所有模型 |
| `reasoning` | 推理过程 | o1、Claude thinking 模式 |
| `tool_call` | 工具调用 | 支持 function calling 的模型 |
| `citation` | 引用来源 | RAG、搜索增强模型 |
| `built_in_tool` | 内置工具 | web搜索、代码解释器 |

### 🎯 **实战应用：流式输出推理过程**

```python
for token, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "复杂问题"}]},
    stream_mode="messages"
):
    if metadata.get('langgraph_node') == 'model':
        for block in token.content_blocks:
            if block.get('type') == 'reasoning':
                print(f"🤔 思考: {block['reasoning']}", end='')
            elif block.get('type') == 'text':
                print(f"💬 回答: {block['text']}", end='')
```

---

## 变化 4: 简化的命名空间

### 📦 **核心包重构**

```python
# ✅ 新版核心模块
from langchain.agents import create_agent         # Agent 创建
from langchain.messages import HumanMessage        # 消息类型
from langchain.tools import tool                   # 工具装饰器
from langchain.chat_models import init_chat_model  # 模型初始化
from langchain.embeddings import init_embeddings   # 嵌入模型
```

### 🔄 **迁移到 `langchain-classic`**

```python
# ⚠️ 需要安装 langchain-classic
# pip install langchain-classic

# ❌ 旧位置 → ✅ 新位置
from langchain.chains import LLMChain
from langchain_classic.chains import LLMChain

from langchain.retrievers import MultiQueryRetriever
from langchain_classic.retrievers import MultiQueryRetriever

from langchain import hub
from langchain_classic import hub
```

### 💡 **为什么这样做？**
- **核心包聚焦**：`langchain` 专注于 Agent 构建的核心抽象
- **向后兼容**：旧功能在 `langchain-classic` 中完全保留
- **性能优化**：减少核心包依赖，加快安装和导入速度

---

## 变化 5: 结构化输出改进

### 🔄 **在主循环内生成**

```python
# ✅ 新版 (LangChain 1.0)
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    condition: str

agent = create_agent(
    model,
    tools=[weather_tool],
    response_format=ToolStrategy(Weather)  # 在主循环中生成
)

result = agent.invoke({"messages": [...]})
weather = result["structured_response"]  # Weather(temperature=70.0, condition='sunny')
```

### 📊 **优势**
- ✅ **成本降低**：无需额外 LLM 调用
- ✅ **延迟减少**：减少网络往返
- ✅ **灵活策略**：可选择工具调用或提供商原生结构化输出

---

## 🔷 第3部分：LangGraph 1.0 主要变化

---

## 变化 1: 核心 API 稳定性承诺

### ✅ **稳定的核心原语**
- `StateGraph` - 状态图构建器
- `add_node()` / `add_edge()` / `add_conditional_edges()` - 图构建方法
- `compile()` - 图编译
- `invoke()` / `stream()` - 执行方法
- `Checkpointer` 接口 - 持久化

### 🎯 **语义化版本控制**
```
1.0.0 → 1.x.x  # 无破坏性变化
1.x.x → 2.0.0  # 可能有破坏性变化
```

---

## 变化 2: `create_react_agent` 弃用

### 🔄 **为什么弃用？**

1. **架构重组**：Agent 抽象应属于 LangChain 层，LangGraph 专注于图执行引擎
2. **功能增强**：新 API 支持中间件，提供更强的可定制性
3. **简化依赖**：减少 LangGraph 对高层抽象的依赖

### 📝 **迁移示例**

```python
# ❌ 旧版 (LangGraph 0.x)
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools, messages_modifier=system_message)

# ✅ 新版 (LangChain 1.0 / LangGraph 1.0)
from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt="You are helpful")
```

---

## 变化 3: 新的中断机制 `interrupt()`

### 🔄 **从静态到动态**

```python
# ❌ 旧版 (LangGraph 0.x) - 静态配置
builder = StateGraph(State)
builder.add_node("risky_action", risky_action_node)
graph = builder.compile(
    interrupt_before=["risky_action"]  # 编译时指定
)

# ✅ 新版 (LangGraph 1.0) - 动态中断
from langgraph.types import interrupt

@tool
def risky_action():
    # 可以基于条件动态决定是否中断
    if needs_approval():
        response = interrupt({
            "message": "需要批准",
            "action": "..."
        })
        if not response["approved"]:
            return "操作取消"
    return "操作完成"
```

### 🎯 **动态中断的优势**
- ✅ **条件性**：基于运行时逻辑决定是否中断（如"置信度低时才中断"）
- ✅ **上下文传递**：可以向用户传递任意数据
- ✅ **灵活控制**：在工具、节点内部任意位置调用

---

## 变化 4: `Command` 对象统一状态更新和路由

### 🔄 **统一状态和路由**

```python
# ❌ 旧版 (LangGraph 0.x) - 分离的状态和路由
def node(state):
    # 只能返回状态更新
    return {"messages": [...]}

def route_fn(state):
    # 需要单独的函数决定下一步
    if condition:
        return "next_node"
    return "end"

# ✅ 新版 (LangGraph 1.0) - Command 统一两者
from langgraph.types import Command

def node(state):
    # 可以同时指定状态更新和路由
    return Command(
        update={"messages": [...]},
        goto="next_node"
    )
```

### 🚀 **Command 对象的威力**

```python
# 恢复中断时也使用 Command
agent.invoke(
    Command(resume={"approved": True}),
    config=config
)

# 多目标路由（广播）
return Command(
    update={...},
    goto=["node1", "node2"]  # 并行执行
)
```

---

## 变化 5: Checkpointer 接口统一

### 🔄 **统一持久化接口**

```python
# ✅ 标准 Checkpointer 使用方式
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

# 开发环境
checkpointer = MemorySaver()

# 生产环境
checkpointer = SqliteSaver.from_conn_string("sqlite:///checkpoints.db")

agent = create_agent(
    model,
    tools,
    checkpointer=checkpointer
)
```

### 📊 **支持的 Checkpointer**

| 类型 | 适用场景 | 特点 |
|------|----------|------|
| `MemorySaver` | 开发/测试 | 内存存储，重启丢失 |
| `SqliteSaver` | 小规模生产 | 文件数据库，易部署 |
| `PostgresSaver` | 大规模生产 | 高性能，支持分布式 |
| 自定义实现 | 特殊需求 | 实现 `BaseCheckpointSaver` 接口 |

---

## 🔄 第4部分：关键迁移场景

---

## 场景 1: 简单的 ReAct Agent

```python
# ❌ 旧版 (LangChain 0.x + LangGraph 0.x)
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool

@tool
def search(query: str) -> str:
    return "搜索结果"

model = ChatOpenAI()
agent = create_react_agent(model, [search])

# ✅ 新版 (LangChain 1.0 + LangGraph 1.0)
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool  # 位置不变

@tool
def search(query: str) -> str:
    return "搜索结果"

model = init_chat_model("openai:gpt-4")
agent = create_agent(
    model, 
    [search],
    system_prompt="You are a helpful assistant"
)
```

---

## 场景 2: 带记忆的 Agent

```python
# ❌ 旧版 - 需要手动配置较多
# pip install langgraph-checkpoint-sqlite==2.0.11
from langgraph.checkpoint.sqlite import SqliteSaver

memory = SqliteSaver.from_conn_string(":memory:")
agent = create_react_agent(model, tools, checkpointer=memory)

# ✅ 新版 - 接口统一，使用更简洁
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model,
    tools,
    checkpointer=MemorySaver()  # 开发环境
)
```

---

## 场景 3: Human-in-the-Loop

```python
# ❌ 旧版 (LangGraph 0.x) - 静态配置
builder.add_node("action", action_node)
graph = builder.compile(interrupt_before=["action"])

# 运行到中断点
result = graph.invoke(input)

# 恢复 - 需要重新 invoke 整个输入
result = graph.invoke(None, config=config)

# ✅ 新版 (LangGraph 1.0) - 动态中断
from langgraph.types import interrupt, Command

@tool
def sensitive_action():
    approval = interrupt({"message": "需要批准吗?"})
    if approval["approved"]:
        return "执行成功"
    return "取消"

agent = create_agent(model, [sensitive_action], checkpointer=MemorySaver())

# 运行到中断
result = agent.invoke(input, config=config)

# 恢复 - 使用 Command
result = agent.invoke(
    Command(resume={"approved": True}),
    config=config
)
```

---

## 场景 4: 使用中间件增强 Agent

```python
# ❌ 旧版 - 没有中间件概念，需要手动在节点中实现
def agent_node(state):
    # 手动实现日志、PII 过滤等逻辑
    messages = filter_pii(state["messages"])  # 自己实现
    response = model.invoke(messages)
    log_interaction(response)  # 自己实现
    return {"messages": [response]}

# ✅ 新版 - 使用内置或自定义中间件
from langchain.agents.middleware import PIIMiddleware, before_model

@before_model
def log_middleware(state, runtime):
    print(f"处理 {len(state['messages'])} 条消息")
    return None

agent = create_agent(
    model,
    tools,
    middleware=[
        PIIMiddleware("email", strategy="redact"),
        log_middleware
    ]
)
```

---

## 📊 完整对比表

| 功能 | LangChain/LangGraph 0.x | LangChain/LangGraph 1.0 | 迁移复杂度 |
|------|------------------------|------------------------|-----------|
| **Agent 创建** | `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` | 🟢 简单 |
| **中间件** | ❌ 不支持 | ✅ 完整支持 | 🟡 中等 (新功能) |
| **人机交互** | 静态 `interrupt_before` | 动态 `interrupt()` | 🟡 中等 |
| **状态 + 路由** | 分离的函数 | `Command` 对象 | 🟢 简单 |
| **Content Blocks** | 提供商特定 | 统一 `content_blocks` | 🟢 简单 |
| **命名空间** | 所有功能在 `langchain` | 核心在 `langchain`，遗留在 `langchain-classic` | 🟢 简单 |
| **结构化输出** | 需要额外 LLM 调用 | 主循环内生成 | 🟢 简单 |
| **Checkpointer** | 配置方式不统一 | 统一接口 | 🟢 简单 |
| **核心 Graph API** | 实验性 | 稳定 (语义化版本) | 🟢 无需迁移 |

**复杂度说明**：
- 🟢 **简单**：直接替换导入路径或 API 调用
- 🟡 **中等**：需要理解新概念，重构部分代码
- 🔴 **复杂**：需要重新设计架构（本次升级无）

---

## ✅ 迁移检查清单

### 1. 依赖更新
```bash
# 更新到 1.x 版本
pip install --upgrade langchain>=1.1.0 langgraph>=1.0.0

# 如果使用遗留功能
pip install langchain-classic
```

### 2. 代码迁移步骤

#### Step 1: 替换 Agent 创建
- [ ] 将 `from langgraph.prebuilt import create_react_agent` 改为 `from langchain.agents import create_agent`
- [ ] 添加 `system_prompt` 参数
- [ ] 移除 `messages_modifier`（合并到 `system_prompt`）

#### Step 2: 迁移遗留功能
- [ ] 检查是否使用 `langchain.chains`
- [ ] 检查是否使用 `langchain.retrievers`
- [ ] 检查是否使用 `langchain.hub`
- [ ] 如果使用，安装 `langchain-classic` 并更新导入

#### Step 3: 升级 Human-in-the-Loop
- [ ] 将静态 `interrupt_before` 替换为动态 `interrupt()`
- [ ] 更新恢复逻辑使用 `Command(resume=...)`

#### Step 4: (可选) 添加中间件
- [ ] 识别重复的横切逻辑（日志、PII 过滤等）
- [ ] 实现或使用内置中间件
- [ ] 在 `create_agent()` 中添加 `middleware` 参数

#### Step 5: 测试
- [ ] 运行现有测试套件
- [ ] 验证 checkpointer 行为
- [ ] 验证工具调用
- [ ] 验证流式输出
- [ ] 验证 interrupt/resume 流程

---

## 🚀 第5部分：实战演练

---

## 实战任务：构建支持审批的数据库操作Agent

### 🎯 **需求**
构建一个Agent，能够：
1. 查询数据库信息
2. 执行危险操作前需要人工审批
3. 记录所有操作日志
4. 过滤敏感信息（PII）

### 📝 **完整实现**

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents.middleware import PIIMiddleware, before_model, after_model
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
import logging

# 1. 定义工具
@tool
def query_database(sql: str) -> str:
    """执行只读SQL查询"""
    # 模拟查询
    return f"查询结果: SELECT * FROM users WHERE ..."

@tool
def delete_records(table: str, condition: str) -> str:
    """删除数据库记录（危险操作）"""
    # 需要人工批准
    approval = interrupt({
        "type": "approval_request",
        "message": f"⚠️ 即将删除 {table} 表中符合 {condition} 的记录",
        "severity": "high"
    })
    
    if not approval.get("approved"):
        return "❌ 操作被拒绝"
    
    # 执行删除
    return f"✅ 已删除 {table} 中的记录"

# 2. 定义中间件
@before_model
async def log_request_middleware(state, runtime):
    """记录每次LLM调用"""
    logging.info(f"🤖 LLM调用: {len(state['messages'])} 条消息")
    return None

@after_model
async def validate_output_middleware(state, runtime):
    """验证输出安全性"""
    last_message = state["messages"][-1]
    if "DROP TABLE" in last_message.content.upper():
        return {
            "messages": [AIMessage("⚠️ 检测到危险操作，已被拦截")]
        }
    return None

# 3. 创建Agent
model = init_chat_model("openai:gpt-4")

agent = create_agent(
    model=model,
    tools=[query_database, delete_records],
    system_prompt="""你是一个数据库管理助手。
    - 对于查询操作，直接执行
    - 对于删除操作，必须先获得批准
    - 始终注意数据安全""",
    checkpointer=MemorySaver(),
    middleware=[
        PIIMiddleware("email", strategy="redact"),
        log_request_middleware,
        validate_output_middleware
    ]
)

# 4. 使用Agent
from langsmith import uuid7

config = {"configurable": {"thread_id": uuid7()}}

# 第一步：执行查询（无需批准）
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "查询所有用户"}]},
    config=config
)
print(result1["messages"][-1].content)

# 第二步：尝试删除（触发审批）
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "删除inactive状态的用户"}]},
    config=config
)

# 此时Agent会中断，等待审批
if result2.get("__interrupt__"):
    print("⏸️ 等待审批...")
    
    # 人工审批
    user_decision = input("是否批准删除？(y/n): ")
    
    # 恢复执行
    result3 = agent.invoke(
        Command(resume={"approved": user_decision == "y"}),
        config=config
    )
    print(result3["messages"][-1].content)
```

### 📊 **实战要点**

1. **动态中断**：`delete_records` 工具内部调用 `interrupt()`
2. **中间件应用**：
   - PII过滤保护敏感信息
   - 请求日志记录所有调用
   - 输出验证拦截危险操作
3. **状态持久化**：使用 `MemorySaver` 保持上下文
4. **Command恢复**：使用 `Command(resume=...)` 传递审批结果

---

## 📱 第6部分：实际应用场景

---

## 场景 1: 企业知识库智能问答

### 🎯 **业务需求**
- 多数据源查询（文档、数据库、API）
- 需要记录用户对话历史
- 敏感信息脱敏
- 引用来源可追溯

### 💡 **1.0 解决方案**

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

@tool
def search_docs(query: str) -> str:
    """搜索企业文档"""
    return "文档内容..."

@tool
def query_crm(customer_id: str) -> str:
    """查询CRM系统"""
    return "客户信息..."

agent = create_agent(
    model=init_chat_model("openai:gpt-4"),
    tools=[search_docs, query_crm],
    system_prompt="你是企业知识库助手，回答时请引用来源",
    checkpointer=PostgresSaver(...),  # 生产级持久化
    middleware=[
        PIIMiddleware("phone", strategy="mask"),
        PIIMiddleware("email", strategy="mask")
    ]
)

# 使用 Content Blocks 提取引用
response = agent.invoke({"messages": [...]})
for block in response["messages"][-1].content_blocks:
    if block["type"] == "citation":
        print(f"📚 来源: {block['source']}")
```

### ✅ **1.0 优势**
- ✅ **Content Blocks** 统一处理引用信息
- ✅ **Middleware** 自动脱敏PII
- ✅ **Checkpointer** 支持多轮对话历史

---

## 场景 2: 自动化运维Agent

### 🎯 **业务需求**
- 自动诊断服务器问题
- 危险操作需要审批（重启服务、删除文件）
- 记录所有操作日志
- 支持回滚

### 💡 **1.0 解决方案**

```python
from langgraph.types import interrupt, Command

@tool
def check_service_status(service: str) -> str:
    """检查服务状态"""
    return f"{service} 运行正常"

@tool
def restart_service(service: str) -> str:
    """重启服务（需要审批）"""
    approval = interrupt({
        "message": f"即将重启 {service}，是否继续？",
        "risk_level": "medium",
        "estimated_downtime": "30s"
    })
    
    if approval.get("approved"):
        return f"✅ {service} 已重启"
    return "❌ 操作取消"

@before_model
async def audit_log_middleware(state, runtime):
    """审计日志"""
    logging.info(f"操作记录: {state['messages'][-1]}")
    return None

agent = create_agent(
    model=init_chat_model("openai:gpt-4"),
    tools=[check_service_status, restart_service],
    system_prompt="你是运维助手，执行危险操作前需获得批准",
    checkpointer=PostgresSaver(...),
    middleware=[audit_log_middleware]
)

# 支持回滚：利用Checkpointer的历史状态
def rollback_to_checkpoint(thread_id, checkpoint_id):
    config = {
        "configurable": {
            "thread_id": thread_id,
            "checkpoint_id": checkpoint_id
        }
    }
    return agent.get_state(config)
```

### ✅ **1.0 优势**
- ✅ **动态 interrupt** 实现灵活审批
- ✅ **Middleware** 自动记录审计日志
- ✅ **Checkpointer** 支持操作回滚

---

## 场景 3: 多模态客服Agent

### 🎯 **业务需求**
- 处理文本+图片输入
- 调用多个API（订单查询、退款、物流）
- 智能路由到人工客服
- 响应时间监控

### 💡 **1.0 解决方案**

```python
from langchain.agents.middleware import wrap_model_call
import time

@tool
def query_order(order_id: str) -> str:
    """查询订单信息"""
    return "订单详情..."

@tool
def transfer_to_human():
    """转接人工客服"""
    interrupt({"type": "transfer_to_human"})
    return "正在转接..."

@wrap_model_call
async def latency_monitor_middleware(invoke_func, state, runtime):
    """监控响应时间"""
    start = time.time()
    result = await invoke_func(state, runtime)
    latency = time.time() - start
    
    if latency > 3.0:  # 超过3秒预警
        logging.warning(f"⚠️ LLM响应慢: {latency:.2f}s")
    
    return result

agent = create_agent(
    model=init_chat_model("openai:gpt-4o"),  # 支持多模态
    tools=[query_order, transfer_to_human],
    system_prompt="你是客服助手，无法解决的问题请转接人工",
    middleware=[latency_monitor_middleware]
)

# 处理图片输入
response = agent.invoke({
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "这个产品有问题"},
            {"type": "image_url", "image_url": "..."}
        ]
    }]
})

# 使用 Content Blocks 获取图片分析结果
for block in response["messages"][-1].content_blocks:
    if block["type"] == "image_analysis":
        print(f"🖼️ 图片分析: {block['description']}")
```

### ✅ **1.0 优势**
- ✅ **Content Blocks** 统一处理多模态内容
- ✅ **wrap_model_call** 实现性能监控
- ✅ **动态 interrupt** 灵活转接人工

---

## 场景 4: 代码审查Agent

### 🎯 **业务需求**
- 自动检查代码质量
- 提供改进建议
- 高危问题需要人工确认
- 生成结构化报告

### 💡 **1.0 解决方案**

```python
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel

class CodeReviewReport(BaseModel):
    issues_count: int
    severity: str
    suggestions: list[str]
    approved: bool

@tool
def run_linter(code: str) -> str:
    """运行代码检查"""
    return "发现3个问题..."

@tool
def suggest_fixes(issues: str) -> str:
    """生成修复建议"""
    return "建议修改..."

agent = create_agent(
    model=init_chat_model("openai:gpt-4"),
    tools=[run_linter, suggest_fixes],
    system_prompt="你是代码审查助手，提供专业建议",
    response_format=ToolStrategy(CodeReviewReport)  # 结构化输出
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "审查这段代码: ..."}]
})

# 直接获取结构化报告
report: CodeReviewReport = result["structured_response"]
print(f"发现 {report.issues_count} 个问题")
print(f"严重程度: {report.severity}")

# 无需额外LLM调用！
```

### ✅ **1.0 优势**
- ✅ **结构化输出** 在主循环内生成，无额外成本
- ✅ **类型安全** 使用 Pydantic 模型
- ✅ **成本优化** 减少LLM调用次数

---

## 🎯 迁移优先级建议

| 优先级 | 任务 | 复杂度 | 收益 | 时间估计 |
|--------|------|--------|------|----------|
| 🔴 高 | 更新 `create_agent` API | 低 | 访问新功能 | 1-2天 |
| 🔴 高 | 配置 Checkpointer | 低 | 启用记忆和 interrupt | 0.5天 |
| 🟡 中 | 采用 Content Blocks | 低 | 提供商无关性 | 1天 |
| 🟡 中 | 迁移 Human-in-the-Loop | 中 | 更灵活的审批流程 | 2-3天 |
| 🟡 中 | 添加 Middleware | 中 | 代码更清晰 | 2-3天 |
| 🟢 低 | 迁移遗留功能到 classic | 低 | 按需迁移 | 按需 |
| 🟢 低 | 优化结构化输出 | 低 | 降低成本 | 1天 |

---

## 📚 参考资源

### 📖 **官方文档**
- [LangChain 1.0 发布说明](https://docs.langchain.com/oss/python/releases/langchain-v1)
- [LangGraph 1.0 发布说明](https://docs.langchain.com/oss/python/releases/langgraph-v1)
- [LangChain 1.0 迁移指南](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [LangGraph 1.0 迁移指南](https://docs.langchain.com/oss/python/migrate/langgraph-v1)

### 🎓 **学习资源**
- [LangChain 学院](https://academy.langchain.com/)
- [LangChain vs LangGraph 对比](https://www.clickittech.com/ai/langchain-1-0-vs-langgraph-1-0/)
- [LangSmith 调试工具](https://smith.langchain.com)

### 💬 **社区支持**
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangGraph GitHub](https://github.com/langchain-ai/langgraph)
- [Discord 社区](https://discord.gg/langchain)

---

## 🎉 总结

### ✅ **核心收获**

1. **架构更清晰**
   - LangChain 负责高级抽象
   - LangGraph 专注图执行引擎
   
2. **功能更强大**
   - Middleware 实现横切关注点
   - Content Blocks 跨提供商统一
   - 动态 interrupt 灵活控制流程

3. **生产更友好**
   - API 稳定性承诺
   - 统一的 Checkpointer 接口
   - 更好的性能和成本优化

### 🚀 **立即行动**

1. ✅ 更新依赖到 1.x
2. ✅ 按优先级迁移核心API
3. ✅ 试用新特性（Middleware、Content Blocks）
4. ✅ 在生产环境逐步推广

---

## Q&A

### 💬 **常见问题**

**Q1: 0.x 和 1.0 可以共存吗？**
A: 可以。可以在不同的虚拟环境中并行使用，逐步迁移。

**Q2: 迁移会破坏现有代码吗？**
A: 核心 Graph API 向后兼容，主要是导入路径和高级API变化。

**Q3: 必须使用 Middleware 吗？**
A: 不是必须，但强烈推荐。它能显著提升代码质量。

**Q4: 结构化输出真的不需要额外LLM调用吗？**
A: 是的，1.0 在主循环内生成，省钱省时。

**Q5: Content Blocks 支持哪些模型？**
A: 已支持 OpenAI、Anthropic、Google、AWS、Ollama。

---

# 感谢观看！

**🎯 记住：迁移不是负担，而是通往生产级Agent的必经之路！**

**📧 联系我们：** 
- GitHub: https://github.com/langchain-ai
- Discord: https://discord.gg/langchain

---

**End of Presentation**