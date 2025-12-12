# 任务 05（直播）| 提示词与上下文工程：让智能体精准理解复杂任务需求 - PPT大纲

## 封面页 (Page 1)
- **标题**：提示词与上下文工程：让智能体精准理解复杂任务需求
- **副标题**：从 Prompt 到 Context 的系统化进阶
- **讲师/团队**：Agent 101 Team
- **时间**：2025

## 目录页 (Page 2)
1. **核心痛点与挑战**
2. **提示词工程系统方法论**
3. **上下文工程核心策略**
4. **实战演示：从简单提示到 RAG 增强**
5. **总结与最佳实践**

---

## 第一部分：核心痛点与挑战 (Page 3-4)

### Page 3: 为什么你的智能体“听不懂”话？（痛点分析）
- **核心痛点**：
  - **理解偏差**：模型输出与预期不符，Prompt 缺乏约束。
  - **窗口限制**：对话越长，模型“遗忘”越快，Context 充满噪声。
  - **成本失控**：无效的上下文导致 Token 费用线性增长。

### Page 4: 解决方案全景图 (基于 Notebook 实战)
- **提示词工程 (Prompt Engineering)**：
  - **核心目标**：提升单次生成的质量。
  - **代码对应**：`expanded_prompts` 实验 (Role, Examples, Constraints)。
- **上下文工程 (Context Engineering)**：
  - **核心目标**：优化多次交互的效率与成本。
  - **代码对应**：`calculate_metrics` (指标量化), `prune_context_layers` (自动剪枝), `RAG` (外部知识)。

---

## 第二部分：提示词工程系统方法论 (Page 5-9)

### Page 5: 提示词的基本原则
- **清晰性 (Clarity)**：避免歧义。
- **具体性 (Specificity)**：指定角色、格式、受众。
- **结构化 (Structure)**：使用 Markdown 或分隔符组织输入。
- **对比演示**：
  - *Bad*: "写个旅游计划。"
  - *Good*: "作为[专业导游]，为[大学生]制定一个[3天]的上海旅游计划，包含[交通、美食]。"

### Page 6: 进阶技巧 1：角色扮演 (Role-Playing)
- **原理**：为模型设定 Persona，激活特定领域的潜空间知识。
- **Notebook 实验**：对比 `base` 与 `with_role`。
- **代码变量**：`expanded_prompts["with_role"]`
  - *Prompt*: "你是一名专业的旅游规划师..."
- **效果**：Latency 降低，内容专业度提升。

### Page 7: 进阶技巧 2：少样本学习 (Few-Shot Prompting)
- **原理 (In-Context Learning)**：通过提供 Input-Output 对，让模型模仿模式。
- **Notebook 实验**：`expanded_prompts["with_examples"]`
- **优势**：
  - 显著提升输出格式的规范性（如 JSON, List）。
  - **数据洞察**：Token Efficiency 可能会降低（因为 Input 变长），但质量提升显著。

### Page 8: 进阶技巧 3：约束与受众 (Constraints & Audience)
- **约束 (Constraints)**：明确边界（如“至少包含三个关键点”、“以XX结尾”）。
  - **代码**：`expanded_prompts["with_constraints"]`
- **受众 (Audience)**：调整语言风格（如“面向大学生”）。
  - **代码**：`expanded_prompts["with_audience"]`
- **实战数据**：Notebook 运行结果显示，`with_audience` 往往会诱导模型生成更长的回复（Response Tokens 增加）。

### Page 9: 综合模板化 (The Comprehensive Template)
- **模板化函数**：`create_expanded_context(role, task, audience, guidelines, examples)`
- **实战案例**：**上海旅游规划**
  - **输入**：角色=资深旅行博主，受众=期末放松的大学生。
  - **输出**：生成一段包含emoji、语气活泼、分天规划的完整提示词。
- **意义**：将 Prompt 视为可维护、可复用的代码模块。

---

## 第三部分：上下文工程核心策略 (Page 10-15)

### Page 10: 上下文窗口的挑战与量化
- **挑战**：Latency 随 Token 增加而增加；Token 越多，$ 燃烧越快。
- **量化指标 (Code: `calculate_metrics`)**：
  1. **Token Efficiency**: `Response Tokens / Prompt Tokens`（投入产出比）。
  2. **Latency per 1k Tokens**: 排除长度影响后的纯处理速度。
- **可视化解读**：解读 Notebook 中的 2x2 子图 (Token Usage, Efficiency, Latency)。

### Page 11: 策略 1：上下文分层管理 (Layered Context)
- **分层逻辑**：
  - **L1 Core**: Task, Role (必须保留)。
  - **L2 Guidance**: Constraints, Examples (高价值)。
  - **L3 Context**: Audience, History (可被交易)。
- **代码体现**：在 `prune_context_layers` 中，将 Context 拆分为字典 (`layers` dict)。

### Page 12: 策略 2：自动化评估 (Model-Based Evaluation)
- **核心问题**：如何自动判断剪枝后的 Prompt 好坏？
- **解决方案**：用 LLM 评估 LLM。
- **代码函数**：`evaluate_response_quality(prompt, response, criteria)`
  - **机制**：让模型打分 (0.0 - 1.0)。
  - **Criterion**：设定具体的评分标准（如“行程是否合理”、“语气是否吸引人”）。

### Page 13: 策略 3：自动化上下文修剪 (Auto-Pruning)
- **核心逻辑 (`prune_context_layers`)**：
  - **基准测试**：先测 Base 和 All Layers。
  - **消融实验**：逐个移除 Layer (Audience, Example...)。
  - **决策算法**：
    - 如果 Quality 显著提升 -> 剪掉该层。
    - 如果 Quality 差不多 但 Token 减少 -> 剪掉该层（更省钱）。
- **案例结果**：**北京旅游规划**场景下，移除了 `example` 层，因为得分未降且节省了 45 tokens。

### Page 14: 策略 4：RAG 检索增强 (Retrieval-Augmented Generation)
- **原理**：Context Window 有限，知识库无限。
- **实现步骤 (Code)**：
  1. **Knowledge Base (`kb`)**: 模拟的 List of Dict 数据结构。
  2. **Retrieval (`retrieve_relevant_info`)**: 简单的关键词匹配。
  3. **Augment (`create_rag_context`)**: 动态拼接 `相关信息` 到 Prompt。
- **场景**：自由行规划（模型不知道最新的签证政策或冷门景点，需外挂知识库）。

---

## 第四部分：实战演示 (Page 16-18)

### Page 16: 实战 1：基础 vs 扩展 (Benchmark)
- **演示图表**：`plot_bars()` 生成的 4 个对比图。
- **结论**：
  - **Efficiency**: `base` 提示效率看似最高（Prompt短），但结果不可控。
  - **Latency**: `with_examples` 不仅规范了输出，反而降低了 Latency（模型不需要“思考”格式）。

### Page 17: 实战 2：自动化剪枝演练
- **场景**：北京 5 日游规划。
- **代码**：调用 `prune_context_layers`。
- **发现**：移除 `Audience` 描述后，评分依然是 1.0，但 Token 从 436 降到了 392。
- **启示**：并非所有精心设计的 Prompt 都是必须的，要用数据说话。

### Page 18: 实战 3：RAG 知识注入
- **场景**：询问“如何规划自由行”。
- **Before RAG**：模型回答泛泛而谈。
- **After RAG (Code: `rag_ctx`)**：
  - 检索到 `kb` 中的“预算控制”、“打包行李”条目。
  - 最终回答包含了具体的“预订交通”、“购买保险”等来自知识库的建议。
- **价值**：让通用模型变成领域专家。

---

## 第五部分：总结与展望 (Page 19-20)

### Page 19: 知识点回顾
- **Prompt Engineering**: 结构化 > 也就是写小作文。
- **Context Engineering**: 是一种资源管理艺术（Token vs Quality）。
- **Tools**: 使用模板化函数、自动化修剪脚本来提升开发效率。

### Page 20: Q&A 与 互动
- **互动环节**：现场调试一个 Prompt。
- **下期预告**：Agent 工具调用与编排。
- **资源链接**：Notebook 下载地址与参考文档。
