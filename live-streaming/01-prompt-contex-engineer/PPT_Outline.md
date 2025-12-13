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
- **核心痛点 1：理解偏差 (Understanding Bias)**
  - *现象*：模型输出与预期完全不符，答非所问。
  - *根因*：Prompt 缺乏约束，存在歧义 (Ambiguity)。
  - *案例*：用户说“写个文案”，模型不知道是写“小红书”还是“公文”。
- **核心痛点 2：窗口限制 (Context Window Limits)**
  - *现象*：多轮对话后，模型“遗忘”之前的设定，或产生“幻觉”(Hallucination)。
  - *根因*：Context 充满噪声 (Noise)，有效信息被淹没 (Lost in the Middle)。
- **核心痛点 3：成本与效率 (Cost & Latency)**
  - *现象*：响应越来越慢，API 账单指数级增长。
  - *根因*：无效的上下文导致 Token 费用线性增长，计算量浪费。

### Page 4: 解决方案全景图 (基于 Notebook 实战)
- **提示词工程 (Prompt Engineering) -> 单点突破**
  - **核心目标**：提升单次生成的质量与精准度。
  - **关键手段**：
    - **Clarity & Specificity**: 清晰与具体。
    - **Structure**: 结构化输入。
    - **Few-Shot**: 少样本示范。
  - **代码对应**：Notebook 中的 `expanded_prompts` 实验 (Role, Examples, Constraints)。
- **上下文工程 (Context Engineering) -> 线面结合**
  - **核心目标**：优化多次交互的效率、一致性与成本。
  - **关键手段**：
    - **Layering**: 上下文分层。
    - **Pruning**: content 剪枝与压缩。
    - **RAG**: 外部知识检索增强。
  - **代码对应**：`calculate_metrics` (指标量化), `prune_context_layers` (自动剪枝), `RAG` (外部知识)。

---

## 第二部分：提示词工程系统方法论 (Page 5-9)

### Page 5: 提示词的基本原则 (The Basics)
- **原则 1：清晰性 (Clarity)**
  - 避免歧义，使用直接的动词。
  - No: "处理一下这个数据。" -> Yes: "计算这列数据的平均值。"
- **原则 2：具体性 (Specificity)**
  - 指定角色、格式、受众、长度。
  - No: "写个旅游计划。" -> Yes: "作为导游，为大学生制定3天上海穷游计划。"
- **原则 3：结构化 (Structure)**
  - 使用 Markdown、分隔符 (`###`, `---`) 区分指令与数据。
  - **对比演示**：
    - *Bad Prompt*: 混杂在一起的一段话。
    - *Good Prompt*: 分块清晰（Role, Task, Constraint）。

### Page 6: 进阶技巧 1：角色扮演 (Role-Playing)
- **原理**：为模型设定 Persona (人设)，激活模型潜在空间 (Latent Space) 中特定领域的知识分布。
- **Notebook 实验**：对比 `base` (无角色) 与 `with_role` (有角色)。
- **代码变量**：`expanded_prompts["with_role"]`
  - *Prompt*: "你是一名专业的旅游规划师。请写一段关于旅游路线规划的说明文字。"
- **效果分析**：
  - **Latency**: 4.50s (比 base 快)。
  - **Quality**: 语气更专业，内容更有条理，不再是泛泛而谈。

### Page 7: 进阶技巧 2：少样本学习 (Few-Shot Prompting)
- **原理 (In-Context Learning)**：模型具有强大的模仿能力。通过提供 Input-Output 对，让模型“照猫画虎”。
- **Notebook 实验**：`expanded_prompts["with_examples"]`
- **代码示例**：
  - *Input*: "示例 1：... 示例 2：..."
- **优势**：
  - **规范性**：显著提升输出格式的规范性（如强制输出 JSON, List）。
  - **冷启动**：某些难以用语言描述的风格，用例子最直接。
- **数据洞察**：虽然 Input Token 增加了 (118 tokens)，但 Output Token 往往更精简 (151 tokens)，整体效率并未降低太多，且质量大幅提升 (Latency 2.45s，极快)。

### Page 8: 进阶技巧 3：约束与受众 (Constraints & Audience)
- **约束 (Constraints) -> 做减法**
  - 明确“做什么”和“不做什么”。
  - **代码**：`expanded_prompts["with_constraints"]` ("至少包含三个关键点", "以XX结尾")。
  - **效果**：减少废话，聚焦核心信息 (Token 减少，Latency 降低)。
- **受众 (Audience) -> 做加法/调优**
  - 调整语言风格以匹配目标读者。
  - **代码**：`expanded_prompts["with_audience"]` ("面向第一次自由行的大学生")。
  - **实战数据**：Notebook 运行结果显示，`with_audience` 导致 Response Token 激增 (440 tokens)，因为模型试图解释得更详细、更通俗。
  - **启示**：Cost 敏感场景需慎用 Audience，或配合 Constraints 使用。

### Page 9: 综合模板化 (The Comprehensive Template)
- **为什么需要模板？**：将 Prompt 视为可维护、可复用、版本控制的“代码”。
- **模板结构函数**：`create_expanded_context(role, task, audience, guidelines, examples)`
- **实战案例**：**上海旅游规划**
  - **输入参数**：
    - `role`: 资深旅行博主
    - `task`: 为期末大学生规划3天路线
    - `style`: 活泼有趣 + 实用
  - **输出 Prompt**：自动组装成一段包含 Emoji、分模块的结构化文本。
  - **模型响应**：生成的回答结构清晰（Day 1, Day 2...），语气贴切（"活力四射的大上海"）。

---

## 第三部分：上下文工程核心策略 (Page 10-15)

### Page 10: 上下文窗口的挑战与量化 (The Context Limits)
- **挑战 1：迷失中间 (Lost in the Middle)**
  - 模型倾向于记住开头和结尾，忽略 Context 中间的信息。
- **挑战 2：成本与速度**
  - **Latency**: 随 Token 增加而增加，直接影响用户体验。
  - **Cost**: Token 越多，$ 燃烧越快。
- **量化指标 (Code: `calculate_metrics`)**
  1. **Token Efficiency**: `Response Tokens / Prompt Tokens`（投入产出比）。
  2. **Latency per 1k Tokens**: 排除长度影响后的纯处理速度（反映计算密度）。
- **可视化解读**：Notebook 中的 2x2 子图显示，Prompt 虽然短 (`base`)，但可能因 Output 不可控导致总 Latency 高；而结构化 Prompt (`with_structure`) 能“引导”模型快速回答。

### Page 11: 策略 1：上下文分层管理 (Layered Context)
- **分层逻辑 (L1-L3 Model)**
  - **L1 Core (不可丢弃)**: Task Definition, Role, Current Query.
  - **L2 Guidance (高价值)**: Constraints, Few-Shot Examples, Output Format.
  - **L3 Context (可压缩/交易)**: User Profile, Chat History, Retrieved Knowledge.
- **代码体现**：在 `prune_context_layers` 函数中，将 Context 拆分为字典 (`layers` dict)，通过代码动态组合 `role`, `audience`, `constraints`, `example`。

### Page 12: 策略 2：自动化评估 (Model-Based Evaluation)
- **核心问题**：如何自动判断 Prompt 修改后是变好了还是变坏了？人工看太慢。
- **解决方案**：LLM-as-a-Judge (用 LLM 评估 LLM)。
- **代码实现**：`evaluate_response_quality(prompt, response, criteria)`
  - **Prompt**: "请为以下响应基于标准打分..."
  - **Output**: 总体评分 (0.0 - 1.0)。
- **应用场景**：批量测试 Prompt 变体，筛选最佳版本。

### Page 13: 策略 3：自动化上下文修剪 (Auto-Pruning)
- **核心逻辑 (`prune_context_layers`)**
  1. **基准测试**：先测 Base (无上下文) 和 All Layers (全量)。
  2. **消融实验 (Ablation)**：逐个移除 Layer (如移除 Audience, Example)。
  3. **智能决策**：
     - 如果 Quality 显著提升 -> 剪掉该层（说明是噪声）。
     - 如果 Quality 差不多 但 Token 减少 -> 剪掉该层（更省钱）。
- **案例结果**：在 **北京旅游规划** 场景下，代码移除了 `example` 层，因为得分未降且节省了 45 tokens，保留了 `role` 和 `constraints`。

### Page 14: 策略 4：记忆管理 (Memory Management)
- **滑动窗口 (Sliding Window)**：只保留最近 N 轮对话 (Simple but aggressive)。
- **摘要压缩 (Summarization)**：
  - 将旧的对话历史总结为 Summary 放入 Context。
  - *Prompt*: "总结我们之前的对话，保留关键决策点。"
- **实体提取 (Entity Extraction)**：只保留对话中的实体（Entity）和待办（Todo），构建“状态机”而非“流水账”。

### Page 15: 策略 5：RAG 检索增强 (Retrieval-Augmented Generation)
- **原理**：Context Window 有限，外部知识库无限。
- **Notebook 实现步骤**：
  1. **Knowledge Base (`kb`)**: 构建 List of Dict (模拟向量数据库)。
  2. **Retrieval (`retrieve_relevant_info`)**: 基于关键词 (如 "旅游规划") 检索 Top-K 相关条目。
  3. **Augment (`create_rag_context`)**: 动态拼接 `相关信息：...` 到 Prompt 中。
- **价值**：
  - **解决幻觉**：强迫模型基于检索到的 Fact 回答。
  - **时效性**：无需微调即可更新知识（如最新的签证政策）。

---

## 第四部分：实战演示 (Page 16-18)

### Page 16: 实战 1：基础 vs 扩展 (Benchmark Demo)
- **演示代码**：运行 `generate_response` 对比 `base_prompt` vs `comprehensive_prompt`。
- **结果解析 (图表)**：
  - **Token Usage**: `comprehensive` 提示 Token 多，但 Output Token 控制得当。
  - **Latency**: 有趣的发现 —— `with_examples` (Few-Shot) 往往比 `base` 更快，因为模型不需要“思考”格式，直接补全。
  - **Token Efficiency**: `base` 效率看似最高，但生成内容往往不可用（太泛）。

### Page 17: 实战 2：自动化剪枝演练 (Pruning Demo)
- **场景**：为大学生规划北京 5 日游。
- **运行代码**：调用 `prune_context_layers`。
- **Log 分析**：
  - 测试 `without_role`: Quality 1.0 -> 0.9 (下降，说明 Role 很重要)。
  - 测试 `without_example`: Quality 1.0 -> 1.0 (不变，说明 Example 冗余)。
- **Action**: 自动移除了 Example 层，Prompt 变短，质量维持。
- **启示**：并非所有精心设计的 Prompt 都是必需的，Let Data Speak。

### Page 18: 实战 3：RAG 知识注入 (Knowledge Injection)
- **场景**：询问“如何规划自由行”。
- **Before RAG**：模型回答泛泛而谈，列出通用步骤（订票、打包）。
- **After RAG (Code: `rag_ctx`)**：
  - **Retrieval**: 检索到 `kb` 中的“预算控制”（含门票餐饮占比）、“打包行李”（含药品证件提醒）。
  - **Augment**: `rag_ctx` = Prompt + "相关信息：..."。
  - **Generation**: 最终回答包含了具体的“预订交通”、“购买保险”等来自知识库的深度建议，且结构化良好。
- **价值验证**：让通用模型瞬间变成懂特定业务规则的专家。

---

## 第五部分：总结与展望 (Page 19-20)

### Page 19: 知识点回顾 (Key Takeaways)
- **Prompt Engineering**: 
  - 核心是 **Constraint (约束)** 和 **Structure (结构)**。
  - 把写 Prompt 当作写代码：模块化、参数化。
- **Context Engineering**: 
  - 是一种 **资源管理艺术**（Token 预算 vs 质量回报）。
  - 分层管理 Context，无关信息早点剪枝。
- **Tools**: 
  - 善用 **Template Functions** (构建器)。
  - 利用 **LLM-as-a-Judge** 进行自动化测试。

### Page 20: Q&A 与 互动 (Next Steps)
- **互动环节**：现场挑选一个观众的模糊 Prompt，用我们的 Pipeline 进行优化。
- **下期预告**：
  - **Agent 工具调用 (Function Calling)**：让模型不仅仅是说话，还能做事（查询天气、读文件）。
  - **任务编排 (Orchestration)**：LangChain / LangGraph 入门。
- **资源链接**：
  - Notebook 下载地址 (Github/Colab)。
  - 推荐阅读：《OpenAI Prompt Engineering Guide》。
