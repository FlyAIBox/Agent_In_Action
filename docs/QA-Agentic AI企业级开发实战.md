# QA：Agentic AI企业级开发实战

## 0. 前置：环境安装配置等

#### Q: 项目要求的 Python 版本是多少？

A: 推荐使用 Python 3.10+。项目中使用到的 LangGraph 和 MCP 等库对新特性有依赖，3.10 是一个稳定且兼容性好的选择。

#### Q: 国内环境如何加速依赖安装？

A: 建议配置 pip 镜像源，如清华源或阿里云源。
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## 1. 智能体-工具调用 (Agent Tool Use & MCP)

**相关资源：**
- [MCP实战演示](../01-agent-tool-mcp/mcp-demo/README.md)
- [简单的Agent框架](../01-agent-tool-mcp/ASimpleAgentFramework.ipynb)

#### Q: 什么是 MCP (Model Context Protocol)？为什么要用它？

A: MCP 是一个开放协议，用于标准化大模型与外部系统（如数据库、API、文件系统）的交互。
- **解决痛点**：传统的 Function Calling 需要为每个模型单独适配接口。MCP 提供了一套统一的客户端-服务器协议，只需实现一次 MCP Server，即可被 Claude、DeepSeek 等支持 MCP 的客户端通用调用。
- **核心优势**：解耦了 "模型" 与 "工具"，极大地提高了工具的复用性和安全性。

#### Q: MCP 中的 stdio 和 sse 模式有什么区别？

A:
- **stdio (标准输入输出)**：适用于**本地单机**场景。Client 直接启动 Server 进程，通过 stdin/stdout 通信。优点是配置简单、延迟低、安全（无网络暴露）。
- **sse (Server-Sent Events)**：适用于**网络/分布式**场景。Server 以 Web 服务运行，Client 通过 HTTP 连接。优点是支持远程访问、多 Client 复用同一个 Server。

#### Q: 如何调试 MCP Server？

A: 推荐使用官方的 **MCP Inspector**。它提供了一个 Web 界面，可以直观地测试工具调用、查看参数校验错误和流式输出。
命令示例：
```bash
npx @modelcontextprotocol/inspector python server/weather_server.py
```

## 2. 多角色智能体系统 (Multi-Agent Systems)

**相关资源：**
- [LangGraph 基础](../02-agent-multi-role/langgraph)
- [Deep Research 实现](../02-agent-multi-role/deepresearch)

#### Q: 为什么选择 LangGraph 而不是 LangChain 的 AgentExecutor？

A:
- **LangChain AgentExecutor**：适合简单的 ReAct 任务，但在构建复杂的多智能体工作流时，状态管理和执行路径控制（循环、条件分支）较为黑盒。
- **LangGraph**：引入了 **Graph (图)** 的概念（Nodes, Edges, State），提供了更细粒度的控制力：
    1. **Statefulness (有状态)**：可以精确定义各个 Agent 之间共享的数据结构。
    2. **Cyclic (循环能力)**：原生支持循环（Loop），适合“规划-执行-反思”的迭代过程。
    3. **Persistence (持久化)**：内置 Checkpointer，可轻松实现断点续传和人机协作（Human-in-the-loop）。

#### Q: 在多智能体系统中，Router (路由器) 的作用是什么？

A: Router 是“分流器”，它不执行具体任务，而是根据当前 State 或上一个 Agent 的输出来决定下一步走向。例如，在“AI旅行规划师”中，Coordinator Router 会根据需求将任务分发给“天气分析师”或“预算优化师”。

## 3. 智能体构建、容器化部署 (Build & Deploy)

**相关资源：**
- [AI旅行规划师部署指南](../03-agent-build-docker-deploy/README.md)

#### Q: 生产环境推荐的部署架构是什么？

A: 推荐 **前后端分离 + 容器化** 架构。
- **Backend**: FastAPI (高性能异步处理，适合 I/O 密集型的 Agent 任务)。
- **Frontend**: Streamlit (快速构建交互式 UI) 或 React/Vue。
- **Orchestration**: Docker Compose (单机编排) 或 Kubernetes (集群大规模部署)。

#### Q: 部署时常见的 API 连接问题如何排查？

A:
1. **网络连通性**：容器内部是否能访问外部 API（如 OpenAI, QWeather）。注意 DNS 配置或代理设置 (`HTTP_PROXY`)。
2. **环境变量**：确保 `.env` 文件正确加载，且 API Key 无误。
3. **API 配额**：检查服务商的 Rate Limit。

## 4. 智能体评估 (Evaluation)

**相关资源：**
- [LLM-as-a-Judge 评估器指南](../04-agent-evaluation/langfuse/docs/LLM-as-a-Judge%20%E8%AF%84%E4%BC%B0%E5%99%A8.md)
- [Langfuse](../04-agent-evaluation/langfuse)

#### Q: 什么是 LLM-as-a-Judge？

A: 这是一种使用强大的 LLM（如 GPT-4）作为裁判，来评价小模型或 Agent 输出质量的方法。
它解决了开放式生成任务（如写作、聊天）难以用传统指标（BLEU, ROUGE）衡量的难题。

#### Q: 如何在 Langfuse 中设置自动化评估？

A:
1. **创建 Dataset**：上传测试用例（Input + Expected Output）。
2. **配置 Evaluator**：在 Langfuse 后台选择 "Managed Evaluator" (如 Answer Correctness) 或编写自定义 Prompt。
3. **变量映射**：将 Trace 中的 Output 映射到 `{{answer}}`，Dataset 中的 Expected Output 映射到 `{{ground_truth}}`。
4. **运行**：点击 Execute，系统会自动跑批并生成评分报告。

## 5. 大模型微调 (Model Fine-tuning)

### 1. 需求分析 (Requirement Analysis)

#### Q: 既然有 RAG（检索增强生成），为什么还需要微调？

A: RAG 解决的是“知识时效性”和“事实准确性”问题，而微调解决的是“行为规范”问题。

在工业界，微调的核心价值通常是：

1. **固定格式：** 强迫模型输出标准的 JSON、SQL 或特定公文格式。
2. **统一风格：** 模仿企业客服的语气（如：“亲切、专业、合规”）。
3. **降本提效：** 用微调后的 7B 模型替代昂贵的 GPT-4/Qwen-72B，在特定任务上达到同等效果。

#### Q: 如何判断这个项目适合微调？

A: 如果 Prompt Engineering（提示词工程）写了 1000 字还是经常出错，或者 RAG 检索回来的内容模型无法正确总结，就是微调的最佳切入点。

------

### 2. 数据准备 (Data Preparation)

#### Q: 数据是不是越多越好？

A: 绝对不是。 工业界遵循 "Quality > Quantity"（质量 > 数量）。

- **误区：** 塞入几万条未清洗的文档片段。
- **正解：** 1,000 条高质量、经过人工校验的 Instruction 数据（指令微调数据）通常优于 10,000 条噪声数据。

#### Q: 微调后模型变傻了（灾难性遗忘）怎么办？

A: 这是最常见的问题。解决方案是数据配比：

在训练垂直领域数据时，必须混入 一定比例的通用数据集（如 General QA、逻辑推理题），保持模型的通用智商和逻辑能力。

------

### 3. 分布式部署/训练 (Distributed Training)

#### Q: 显存不够（OOM）如何解决？

A: 在企业级训练中（通常涉及多卡或多机），主要靠技术栈优化：

1. **DeepSpeed ZeRO：** 开启 ZeRO-2 或 ZeRO-3，将模型参数切分到多张显卡上，打破单卡显存限制。
2. **Flash Attention 2：** 必须开启，它能显著降低显存占用并提升 3 倍以上的训练速度。
3. **梯度累积 (Gradient Accumulation)：** 用时间换空间，显存不够就减小 Batch Size，增加累积步数。

#### Q: LoRA 和 全量微调 (Full Fine-tuning) 怎么选？

A: 90% 的企业场景选 LoRA 即可。它训练快、显存小、效果在垂直任务上通过调整 Rank (如 r=64) 几乎能追平全量。只有在模型需要学习全新的语言（如藏语）或极度生僻的领域知识时，才考虑全量。

------

### 4. 评估 (Evaluation)

#### Q: Loss 曲线下降了，模型就一定好用吗？

A: 不一定。 Loss 只能代表模型“背书”的能力，不代表“应用”能力。

企业级评估标准：

1. **金标准集 (Golden Set)：** 业务专家人工撰写的 100 个高难度真实场景问题。
2. **LLM-as-a-Judge：** 写脚本调用 GPT-5 或 Qwen-Max，让大模型充当裁判，对微调后小模型的回答进行打分（准确性、格式、安全性）。
3. **拒绝回答测试：** 故意问一些无关或违规问题，看模型是否能正确拒绝，而不是胡编乱造。

------

### 5. 上线 (Deployment & Inference)

#### Q: 用 HuggingFace 原生代码上线推理行不行？

A: 仅限于测试，生产环境绝对不行。 Python 原生推理并发性能极差。

#### Q: 生产环境推荐什么推理方案？

A: 必须上高性能推理引擎：

1. **vLLM：** 目前最推荐。吞吐量极高，支持 PagedAttention，易于集成。
2. **量化 (Quantization)：** 上线时使用 **AWQ (4-bit)** 或 **GPTQ** 量化模型。这能让显存占用减半（7B 模型仅需约 6-8G 显存），且推理速度提升 2-3 倍，几乎无损精度。

------

### 下一步建议

**Would you like a diagram illustrating the "LLM-as-a-Judge" automated evaluation workflow to include in your presentation?**