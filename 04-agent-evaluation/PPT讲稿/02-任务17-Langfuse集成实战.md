# 任务17：Langfuse集成实战 - 追踪OpenAI和LangChain调用

**时长：** 30分钟  
**难度：** ⭐⭐⭐☆☆  
**交付成果：** 基础集成代码和追踪方案

---

## 第一部分：OpenAI SDK集成 (15分钟)

### 🎯 集成目标

**只需改一行代码，就能获得完整的可观测性！**

从 `from openai import OpenAI` 改为 `from langfuse.openai import openai`

### 🚀 快速开始

#### 步骤1：安装依赖
- langfuse==3.3.0
- openai==1.107.0

#### 步骤2：配置环境变量
- OPENAI_API_KEY
- LANGFUSE_PUBLIC_KEY
- LANGFUSE_SECRET_KEY

#### 步骤3：使用集成后的OpenAI客户端
- 使用 `name` 参数为调用命名
- 使用 `metadata` 添加自定义标签
- 完全兼容原生OpenAI SDK

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
- 支持多模态输入（文本+图像）
- 自动追踪图像URL和分析结果

---

### 🌊 流式输出追踪
- 开启 `stream=True` 启用流式输出
- Langfuse自动收集所有片段、计算token、记录完整输出

---

### ⚡ 异步调用追踪
- 使用 `AsyncOpenAI` 客户端
- 异步函数中的调用自动追踪
- 完全支持 async/await 语法

---

### 🔧 函数调用（Function Calling）
- 支持Function Calling追踪
- 自动记录：函数定义、参数、返回值
- 标记为特殊的Generation类型

---

### 🏷️ 高级功能：自定义元数据
- `langfuse_session_id`：会话ID
- `langfuse_user_id`：用户ID
- `langfuse_tags`：标签列表
- 自定义字段：environment、version等
- **好处：** 按session/user分析、按tags过滤、自定义分组统计

---

### 📋 将多次调用归并到同一个Trace
- 使用 `@observe()` 装饰器创建顶层trace
- 函数内的所有OpenAI调用自动归入同一trace
- 形成层级结构：顶层trace → 多个子span
- 每个span记录输入输出和执行时间

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
- langfuse==3.3.0
- langchain==0.3.27
- langchain-openai==0.3.31

#### 步骤2：初始化Langfuse回调处理器
- 创建 `CallbackHandler` 实例
- 在调用时通过 `config` 参数传递
- 格式：`config={"callbacks": [langfuse_handler]}`

---

### 📝 示例1：简单的LangChain LCEL
- **LCEL** = LangChain Expression Language
- 构建链：Prompt | Model | OutputParser
- 使用 `|` 符号连接组件
- **追踪结构：** Prompt → Model (Generation) → Parser
- 自动记录tokens和成本

---

### 🔗 示例2：复杂的多步骤链
- 支持链的嵌套调用
- chain1 的输出作为 chain2 的输入
- 使用 `RunnableParallel` 并行处理
- **追踪结构：** chain2 → chain1 → RunnableParallel → prompt2 → model → parser
- 完整记录每个步骤的执行

---

### 🏃 示例3：Runnable方法追踪
所有Runnable方法都支持追踪：
- `invoke()`：同步调用
- `ainvoke()`：异步调用
- `batch()`：批处理
- `stream()`：流式输出
- 每种方法都会在Langfuse中创建独立的Trace

---

### 📚 示例4：检索增强生成（RAG）
- 创建向量数据库（Chroma + OpenAI Embeddings）
- 构建检索问答链（RetrievalQA）
- 指定检索参数（k=3）
- **追踪结构：** Retriever → StuffDocumentsChain → LLMChain
- 记录：检索文档、tokens、成本、延迟

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


