# LangGraph + Langfuse 集成实战

**一页速览：构建可观测的多智能体应用**

---

## 🎯 核心价值

**LangGraph** = LangChain + 图结构（支持复杂工作流、多智能体协作）  
**Langfuse** = 可观测性平台（追踪、监控、评分、优化）

**集成效果：** 自动追踪复杂智能体的完整执行链路

---

## 🚀 三步快速集成

### 1️⃣ 初始化 Langfuse
- 获取 Langfuse 客户端实例
- 创建 CallbackHandler 回调处理器
- 自动读取环境变量中的认证信息

### 2️⃣ 构建 LangGraph 智能体
- 创建 StateGraph 状态图
- 添加节点（定义业务逻辑）
- 编译图形为可执行对象

### 3️⃣ 添加追踪（两种方式）

**方式A：运行时添加**
- 在调用 `invoke()` 时通过 `config` 参数传递回调处理器
- 适合本地开发和测试场景

**方式B：编译时预配置（Server部署推荐）**
- 使用 `with_config()` 在编译时预配置回调
- 所有请求自动启用追踪，无需重复配置
- 适合生产环境部署

---

## 🤝 多智能体协作追踪

**场景：** 主智能体调用子智能体，需要在同一条trace中聚合

**实现步骤：**
1. **生成共享 trace_id** - 使用 `Langfuse.create_trace_id()` 创建唯一标识
2. **子智能体封装为工具** - 使用 `@tool` 装饰器包装子智能体
3. **注入共享 trace_id** - 通过 `trace_context` 传递共享标识
4. **创建主智能体** - 使用 `create_react_agent` 并注入工具列表
5. **执行并追踪** - 通过 `callbacks` 启用自动追踪

**效果：** 主智能体和所有子智能体的执行都聚合在同一条trace中，便于全局分析

---

## 📊 添加评分（质量评估）

**三种评分方式：**

**方式1：在span上下文中评分**
- 使用 `span.score_trace()` 直接在执行过程中记录评分
- 适合实时评估场景
- 可以添加评论说明

**方式2：评分当前trace**
- 使用 `score_current_trace()` 为正在执行的trace评分
- 无需持有span对象
- 适合在回调函数中使用

**方式3：异步评分**
- 使用 `create_score()` 配合 trace_id 进行评分
- 适合离线批处理和延迟评估
- 可在执行完成后任意时间添加评分

---

## 💡 关键概念速查

| 概念 | 说明 | 用途 |
|:---|:---|:---|
| **StateGraph** | LangGraph核心，定义状态和工作流 | 构建复杂智能体 |
| **CallbackHandler** | Langfuse回调处理器 | 自动采集执行数据 |
| **trace_id** | 追踪标识符 | 聚合多智能体调用 |
| **span** | 单个执行单元 | 记录节点级别细节 |
| **Score** | 评分机制 | 质量评估和反馈 |

---

## 🎨 可视化工作流

**方法：** 使用 `graph.get_graph().draw_mermaid_png()` 生成流程图

**支持格式：**
- PNG图片 - `draw_mermaid_png()`
- SVG矢量图 - `draw_mermaid_svg()`
- 输出到文件 - `draw_mermaid_file()`

**效果：** 自动生成流程图，清晰展示节点、边和执行顺序

---

## 📈 Langfuse追踪能力

✅ **完整执行链路**：从入口到输出的每一步  
✅ **节点级别监控**：每个节点的耗时、输入、输出  
✅ **Token和成本统计**：精确计算API调用费用  
✅ **多智能体聚合**：通过trace_id合并调用链  
✅ **实时评分**：支持数值、文本、分类评分  

---

## 🔧 生产环境最佳实践

### Server 部署
- ✅ 使用 `with_config()` 预配置回调
- ✅ 所有请求自动追踪，无需手动添加
- ✅ 环境变量配置 Langfuse 认证信息

### 多智能体场景
- ✅ 使用共享 `trace_id` 聚合调用链
- ✅ 为每个子智能体创建独立 span
- ✅ 记录输入输出，便于排查问题

### 评分策略
- ✅ 在线反馈：用户满意度、有用性
- ✅ 离线评估：准确性、相关性、安全性
- ✅ A/B测试：按trace聚合对比效果

---

## 🎯 学习成果

完成本实战后，你将能够：

1. ✅ 使用 LangGraph 构建状态图智能体
2. ✅ 通过 Langfuse 自动追踪执行过程
3. ✅ 监控多智能体协作系统
4. ✅ 为追踪添加评分进行质量评估
5. ✅ 在生产环境中部署可观测的智能体

---

## 📚 相关资源

- **LangGraph 文档**: https://langchain-ai.github.io/langgraph/
- **Langfuse 文档**: https://langfuse.com/docs
- **LangChain 集成**: https://langfuse.com/integrations/frameworks/langchain
- **自定义评分**: https://langfuse.com/docs/scores/custom

---

**💪 立即开始：** 将 Langfuse 集成到你的 LangGraph 应用，获得完整的可观测性！

