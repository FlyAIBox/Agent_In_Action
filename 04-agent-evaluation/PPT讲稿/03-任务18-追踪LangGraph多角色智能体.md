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
- 定义状态结构（TypedDict）
- 包含：messages、user_info、context等字段
- 使用 `StateGraph(State)` 创建
- **作用：** 管理整个工作流的状态

#### 2. Node（节点）
- 节点是一个函数：接收state，返回更新
- 处理具体的业务逻辑
- 使用 `graph.add_node(name, function)` 添加
- **作用：** 执行具体的业务逻辑

#### 3. Edge（边）
- **无条件边：** `add_edge("node_a", "node_b")` 总是执行
- **条件边：** `add_conditional_edges()` 根据路由函数选择下一个节点
- 路由函数返回下一个节点的名称
- **作用：** 定义节点之间的流转关系

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
- 创建 `CallbackHandler` 实例
- 编译图后在 `invoke` 时传递callbacks
- 格式：`config={"callbacks": [langfuse_handler]}`
- **特点：** 简单，适合快速集成

#### 方式2：使用@observe装饰器
- 在节点函数上使用 `@observe()` 装饰器
- 精细控制每个节点的追踪
- 可自定义span名称和元数据
- **特点：** 精细控制，可自定义span

#### 方式3：预配置图对象（Server模式）
- 在编译时使用 `.with_config()` 预配置
- 之后的所有 `invoke` 都会自动追踪
- 无需每次传递callbacks参数
- **特点：** 适合生产环境，无需重复配置

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

### 📝 实现步骤

#### 步骤1：定义状态结构
定义 `EmailState` 包含以下字段：
- email：原始邮件数据
- is_spam：是否垃圾邮件
- spam_reason：垃圾邮件原因
- email_category：邮件分类
- draft_response：回复草稿
- messages：LLM对话历史

#### 步骤2：定义节点函数
创建5个节点函数：
- **read_email**：读取邮件信息
- **classify_email**：使用LLM判断邮件是否为垃圾邮件
- **handle_spam**：处理垃圾邮件
- **drafting_response**：起草回复内容
- **notify_mr_wayne**：通知主人

#### 步骤3：构建图结构
- 创建 `StateGraph(EmailState)`
- 添加所有节点
- 定义路由逻辑：根据 `is_spam` 选择分支
- 添加边：START → read_email → classify_email
- 添加条件边：分为spam和legitimate两个分支
- 结束边：最终到达END

#### 步骤4：执行并追踪
- 创建 `CallbackHandler` 实例
- 准备测试邮件数据
- 调用 `compiled_graph.invoke()` 执行
- 通过config传递langfuse_handler进行追踪

### 📊 在Langfuse中的追踪结构

```
Trace: email-processing
├── read_email (0.001s)
├── classify_email (1.2s, $0.0008, 150 tokens)
├── drafting_response (2.3s, $0.0015, 300 tokens)
└── notify_mr_wayne (0.001s)

Total: 3.5s, $0.0023
```

---

## 第四部分：高级功能 - 多智能体协作 (5分钟)

### 🤝 场景：主Agent调用子Agent

**实现方式：**
- 生成共享的 `trace_id`
- 子Agent封装为工具函数（使用 `@tool` 装饰器）
- 在工具函数内使用 `start_as_current_span` 创建span
- 传递共享的 `trace_context`
- 主Agent使用 `create_react_agent` 创建，工具列表包含子Agent
- 执行时传递callbacks进行追踪

**追踪效果：**
- main-agent → Tool Call (research_agent) → sub-agent (节点1, 2, 3) → 最终回答
- 所有调用归入同一个Trace
- 形成清晰的层级关系

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


