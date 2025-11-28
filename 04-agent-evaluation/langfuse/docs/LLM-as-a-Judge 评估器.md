### 一、创建新的 LLM-as-a-Judge 评估器

1. **导航**：进入 Langfuse 控制台`左侧栏`的 **Evaluators** 的` LLM-as-a-Judge `。
2. **操作**：点击 `Create Evaluator` 按钮以初始化一个新的评估配置。

![image-20251126165332628](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261653010.png)

### 二、设置默认模型(Set up default model)

您需要定义用于执行评估任务的默认 LLM（裁判模型）。

![image-20251126165906049](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261659568.png)

- `LLM adapter`:  `openai`

- `API Base URL`：`https://api.apiyi.com/v1`

- `API Key`：在`https://api.apiyi.com`申请

  > OpenAI国内代理地址
  > https://api.apiyi.com/register/?aff_code=we80
  > 新用户注册送0.1美金

设置后，选择模型名称

![image-20251126170023999](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261700395.png)

### 三、选择评估器 (Pick an Evaluator)

在此步骤中，您需要确定评估逻辑的来源，主要有两种方式，**我们选择`托管评估器`**：

1. **托管评估器 (Managed Evaluator)**：

   ![image-20251126170134380](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261701760.png)

   - **来源**：Langfuse 官方或合作伙伴（如 Ragas）维护的现成目录。
   - **内容**：涵盖常见的质量维度，如*幻觉 (Hallucination)*、*上下文相关性 (Context-Relevance)*、*毒性 (Toxicity)*、*有用性 (Helpfulness)*。
   - **优势**：无需编写 Prompt，即开即用，且持续更新。

   > 我们选择托管评估器中`Answer Correctness`评估器

2. **自定义评估器 (Custom Evaluator)**：

   - **适用场景**：当通用库无法满足特定的业务逻辑需求时。
   - **配置步骤**：
     1. 编写包含 `{{variables}}` 占位符的评估 Prompt（例如 `{{input}}`, `{{output}}`, `{{ground_truth}}`）。
     2. （可选）自定义评分标准（0-1分）和推理引导词，以规范 LLM 的输出。
     3. （可选）为此评估器绑定特定的模型（如果不绑定，则使用默认模型）。
   - **复用性**：保存后，该评估器可在整个项目中复用。

### 四、选择评估数据源

> 我们选择托管评估器中`Answer Correctness`评估器后，进入评估期设置

配置评估器运行的目标数据范围，分为生产数据和数据集数据，**我们选择`数据集运行 (Dataset runs)`**：

1. **实时生产数据 (Live Data)**：

   - **监控目标**：实时监控线上应用的表现。
   - **范围 (Scope)**：建议选择 `New traces only`（仅新产生的 Trace）；也可选择回填历史数据。
   - **过滤器 (Filter)**：通过 Trace name、Tags、`userId` 等字段精确筛选。*强烈建议先通过 Filter 缩小范围*。
   - **预览**：系统会展示过去 24 小时内匹配当前 Filter 的 Trace 样本，供您核对。
   - **采样 (Sampling)**：配置运行百分比（例如 5%）以控制成本和评估吞吐量。

   ![image-20251126171503359](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261715850.png)

2. **数据集运行 (Dataset runs)**：

   - **过滤器 (Filter)**：通过 Datase字段精确筛选。*强烈建议先通过 Filter 缩小范围*。

   ![image-20251126172840308](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261728654.png)

### 五、映射变量并预览 Prompt

> 此步骤将 Trace 或数据集中的实际数据字段绑定到 Prompt 变量（如 `{{input}}`）。
>
> 1. **数据映射**：
>    - **Live Data**：通常将 Trace Input 映射到 `{{input}}`，Trace Output 映射到 `{{output}}`。
>    - **JSONPath 支持**：如果数据嵌套在 JSON 对象中，使用 JSONPath 表达式提取（例如 `$.choices[0].message.content`）。
>    - **Dataset**：系统通常会自动建议映射（如 Dataset 的 `expected_output` 映射到 `{{ground_truth}}`）。
> 2. **实时预览 (Live Preview)**：
>    - Langfuse 会使用匹配 Filter 的历史 Trace 填充 Prompt。
>    - **操作**：请务必切换几条不同的 Trace，检查 Prompt 中的数据填充是否符合预期，确保评估上下文完整。

![image-20251126172944653](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261730128.png)

##### 1. 确定评估范围 (Target Filter)

- **选择数据集**：在 "Target filter" 中，选择你要评估的特定数据集，如 `qa-dataset_langgraph-agent`。
- 这决定了评估器将针对哪些历史数据或测试集运行。

##### 2. 配置评估 Prompt 与变量映射 (Variable Mapping)

目的是告诉评估模型（Judge LLM）从哪里获取数据来填入 Prompt。

- **配置 `{{ground_truth}}`（基准事实）：**
  - **来源对象 (Object)**：选择 `Dataset item`（数据集条目）。
  - **来源变量 (Variable)**：选择 `Expected output`（预期输出/标准答案）。
  - *含义*：告诉评估器，Prompt 中的“基准事实”字段，应直接读取数据集中预设好的标准答案。
- **配置 `{{answer}}`（大模型回答）：**
  - **来源对象 (Object)**：选择 `Trace`（链路追踪数据）。
  - **来源变量 (Variable)**：选择 `Output`（模型实际输出）。
  - *含义*：告诉评估器，Prompt 中的“回答”字段，应读取大模型在实际运行（Trace）中生成的最终回复。

##### 3. 执行评估 (Execute)

- 点击右下角的 **"Execute"** 按钮。
- 系统将开始遍历数据集，将每一条的 `Expected output` 和对应的 Trace `Output` 填入你编写的 Prompt 中，调用大模型（Judge）进行 TP/FP/FN 的分类和打分。

### 六、查看评估过程

LLM-as-a-Judge 的每一次运行本身也是一条 Trace，您可以通过以下四种方式查看其详细执行过程（包括发送给裁判的 Prompt、Token 消耗、延迟等）：

![image-20251126175814773](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261758011.png)

- 在左侧导航栏中，点击 **"LLM-as-a-Judge"** 菜单项。
- **操作**：在 "Logs"（日志）一列下，点击 **"View"** 按钮

### 七、理解执行状态

监控评估器的运行状况：

- **Completed**：评估成功完成。
- **Error**：评估失败（点击 Execution trace ID 查看具体报错）。
- **Delayed**：触发了 LLM 提供商的速率限制，系统正在进行指数退避重试。
- **Pending**：评估任务已进入队列，等待运行。

![image-20251126175931708](https://cdn.jsdelivr.net/gh/Fly0905/note-picture@main/imag/202511261759085.png)