# LangGraph 基础教程 - 从入门到实战

## 📚 课程模块概览

### 1️⃣ 简单图 (Simple Graph)
**核心概念：图的基本构成**
- **状态定义 (State)**: 使用 TypedDict 定义图状态
- **节点函数 (Nodes)**: 处理业务逻辑的基本单元
- **边连接 (Edges)**: 普通边 + 条件边实现路由控制
- **图编译执行**: StateGraph → compile() → invoke()

---

### 2️⃣ 链式结构 (Chain)
**核心概念：消息流转与工具调用**
- **消息类型**: HumanMessage、AIMessage、SystemMessage、ToolMessage
- **聊天模型集成**: ChatOpenAI 与消息列表处理
- **工具绑定机制**: bind_tools() + 函数签名自动转换
- **状态归约器**: add_messages 实现消息追加而非覆盖

---

### 3️⃣ 路由器模式 (Router)
**核心概念：智能决策与动态分支**
- **条件路由**: tools_condition 自动判断是否需要工具调用
- **ToolNode**: 内置工具执行节点，自动处理工具结果
- **双路径设计**: 直接回复 ↔ 工具调用循环
- **Agent 雏形**: 让大模型决定 "思考" 还是 "行动"

---

### 4️⃣ Agent 记忆 (Agent Memory)
**核心概念：状态持久化与会话管理**
- **检查点机制**: MemorySaver 在每一步自动保存状态
- **线程管理**: thread_id 实现多会话隔离
- **上下文延续**: 跨调用保持对话历史
- **Agent 三步循环**: Act (工具调用) → Observe (结果) → Reason (推理)

---

### 5️⃣ 外部数据库记忆 (External Memory)
**核心概念：生产级持久化方案**
- **SQLite 检查点器**: SqliteSaver 实现数据库持久化
- **消息摘要机制**: 自动压缩长对话 (>6条触发)
- **状态扩展**: 继承 MessagesState 添加 summary 字段
- **跨会话恢复**: 程序重启后状态不丢失

---

## 🎯 技术栈与核心依赖

```bash
langgraph==0.6.7          # 图执行框架
langchain_core==0.3.75    # 核心抽象
langchain_openai==0.3.32  # OpenAI 模型集成
langgraph-checkpoint-sqlite==2.0.11  # SQLite 持久化
```

---

## 💡 学习路径总结

```
简单图 → 链式调用 → 条件路由 → 内存管理 → 外部存储
  ↓         ↓          ↓          ↓          ↓
基础架构   工具集成   智能决策   会话保持   生产部署
```

**从概念到实战，5步构建智能体应用！**

