# 《Agentic AI 智能体开发实战》课程大纲

## 课程设计思路

### 这门课是讲给谁的？

本课程主要适合以下人群：

**主要目标群体：**
- 有5年左右开发经验的工程师
- 希望学习大模型和智能体应用开发的技术人员
- 对Agentic AI 智能体技术感兴趣的后端/全栈工程师
- 希望从传统软件开发转向AI应用开发的工程师

**基础要求：**
- 具备Python或JAVA编程基础，能够阅读和编写代码
- 了解基本的Web开发知识（API、HTTP协议等）
- 对机器学习和大语言模型有初步了解
- 熟悉Linux基本操作和Docker容器技术

**对于不同背景的学习者：**

| 人群类型 | 适用场景 | 收获价值 |
|---------|----------|----------|
| **后端开发工程师** | 希望将AI能力集成到现有系统 | 掌握智能体开发和部署的完整技术栈 |
| **AI算法工程师** | 希望将模型落地到生产环境 | 学会模型微调、推理优化和工程化部署 |
| **技术团队负责人** | 需要评估AI技术方案 | 理解智能体系统架构和成本优化策略 |
| **创业者/产品经理** | 进行AI产品规划 | 深度理解AI技术实现和商业化路径 |

### 课程开设背景

随着ChatGPT、Claude、DeepSeek等大语言模型的普及，AI技术正在从"能力演示"走向"生产落地"。然而，很多开发者在将AI技术应用到实际业务中时，遇到了以下挑战：

**1. 从单一模型到智能体系统的跨越**
- 很多开发者会调用LLM API，但不知道如何构建复杂的智能体系统
- 缺乏对多角色协作、工具调用、状态管理等核心概念的系统理解
- 不了解如何将智能体与现有业务系统集成

**2. 从演示Demo到生产环境的鸿沟**
- Demo能跑通，但不知道如何处理并发、稳定性、成本等生产环境问题
- 缺乏对模型推理优化、性能调优、监控评估的实践经验
- 不了解如何进行容器化部署和DevOps自动化

**3. 从通用模型到垂直领域的定制**
- 通用大模型在特定领域表现不佳，但不知道如何进行微调优化
- 缺乏对数据准备、模型训练、效果评估的系统方法
- 不了解如何平衡模型效果和推理成本

**4. 从碎片化学习到系统化掌握**
- 市面上的教程往往是单点技术，缺乏端到端的完整链路
- 各种新技术（MCP、LangGraph、vLLM等）层出不穷，不知如何选择和组合
- 缺少可直接参考的企业级实战案例

为了帮助开发者系统化地掌握Agentic AI技术，真正实现从理论到生产的跨越，我们开发了本课程。

### 这门课老师准备讲什么？

**本课程以"端到端构建企业级AI智能体系统"为核心目标**，通过一个完整的实战项目（AI旅行规划智能体），覆盖从需求分析、架构设计、开发实现、模型优化、部署运维到评估监控的全链路技能。

**课程核心特点：**

**1. 实战驱动，避免空谈**
- 基于真实的AI旅行规划项目，每个知识点都有完整的代码实现
- 采用"需求 → 设计 → 实现 → 优化"的闭环开发流程
- 提供可直接运行的完整代码和部署脚本，开箱即用

**2. 技术前沿，注重实用**
- 涵盖2025年最新的AI技术栈：MCP、LangGraph、vLLM、LlamaFactory、Langfuse
- 每个技术选型都有详细的对比分析和使用场景说明
- 注重工程化实践，而非纸上谈兵

**3. 系统化学习路径**
- 从基础的工具调用开始，逐步深入到多角色协作、模型微调、性能优化
- 模拟真实项目的迭代开发过程，循序渐进地构建完整系统
- 每个模块既相对独立，又构成完整的技术体系

**4. 企业级解决方案**
- 不仅讲"怎么做"，更讲"为什么这么做"和"生产环境怎么做"
- 包含性能优化、成本控制、安全防护、监控告警等生产实践
- 提供可直接应用于商业项目的架构模式和最佳实践

**5. 可扩展的通用框架**
- 虽然以旅游场景为例，但框架可应用于医疗、金融、教育等各个领域
- 核心架构和技术方案具有通用性和可复用性
- 提供医疗智能体等扩展案例，帮助理解框架的通用性

**通过学习本系列课程，您将达到如下目标：**

✅ **技术能力提升**
- 掌握工具调用（Function Call/MCP）和上下文工程的核心技术
- 深入理解多角色智能体协作机制，能够使用LangGraph构建复杂的Agent系统
- 掌握模型微调（LlamaFactory）和推理优化（vLLM）的完整流程
- 建立智能体评估（LangFuse）和性能压测（vLLM Benchmark）的工程化体系

✅ **实战项目经验**
- 获得一个完整的企业级AI旅行规划智能体项目
- 掌握从需求分析到生产部署的全链路开发技能
- 积累可直接写入简历的AI应用开发实战经验

✅ **架构设计能力**
- 理解智能体系统的分层架构和模块化设计
- 掌握多角色协作的工作流设计方法
- 学会平衡功能、性能、成本的架构决策

✅ **工程化能力**
- 掌握Docker容器化部署和DevOps实践
- 建立完整的监控、评估、优化闭环
- 学会生产环境的性能调优和成本控制

✅ **职业发展**
- 提升在AI应用开发领域的竞争力
- 获得转型AI工程师的技术储备
- 为从事AI创业或加入AI团队做好准备

---

## 课程内容总览

### 🧭 课程大纲速览

| 序号 | 课程模块 | 核心技术栈 | 能力产出 | 配套资料 |
|------|----------|-----------|----------|----------|
| **01** | 工具调用与MCP协议 | Function Call, MCP, 上下文工程 | 让智能体接入外部工具，拓展执行边界 | `01-agent-llm-mcp/` |
| **02** | 多角色智能体系统 | LangGraph, LangChain | 构建多角色协作的智能体骨架 | `02-agent-multi-role/` |
| **03** | 系统构建与容器化部署 | FastAPI, Streamlit, Docker | 完整的前后端系统和生产环境部署 | `03-agent-build-docker-deploy/` |
| **04** | 智能体评估与监控 | Langfuse, LangSmith | 建立质量评估和安全监控闭环 | `04-agent-evaluation/` |
| **05** | 模型微调与优化 | LlamaFactory, PEFT, LoRA | 打造垂直领域定制化模型 | `05-agent-model-finetuning/` |
| **06** | 模型推理部署 | vLLM, Transformers | 高性能推理服务部署与优化 | `06-agent-model-inference/` |
| **07** | 性能压测与评估 | vLLM Benchmark | 定量评估推理性能并持续优化 | `07-agent-llm_benchmark/` |

### 🏆 课程收获

| 收获类别 | 具体内容 |
|----------|----------|
| **🛠️ 完整技术栈** | 掌握从环境搭建到企业级部署的完整AI智能体技术链路 |
| **💼 实战项目** | 获得可直接应用于业务场景的企业级实战项目 |
| **🔬 前沿技术** | 深入理解MCP、LangGraph、vLLM、LlamaFactory、Langfuse等前沿技术 |
| **🏭 工程化能力** | 学会模型微调、推理优化、性能压测、成本控制等工程化实践 |
| **💡 职业发展** | 提升AI应用开发领域的就业竞争力 |

---

## 📋 课程详细大纲

### 模块一：工具调用与MCP协议

**📂 目录结构：** `01-agent-llm-mcp/`

#### 1.1 提示词工程基础 (Prompt Engineering)

**核心问题：** 如何让大模型准确理解需求并输出期望结果？

**知识点：**
- 提示词的基本原则：清晰性、具体性、结构化
- 零样本(Zero-shot)、少样本(Few-shot)提示技巧
- 思维链(Chain-of-Thought)提示方法
- 角色扮演和情境设定技巧
- 提示词模板化和复用

**实战案例：**
- 从简单对话到复杂任务的提示词演进
- 旅行规划场景的提示词设计实践
- 提示词效果评估和迭代优化

**配套代码：** `01_Complex_Prompts_from_Scratch.ipynb`

#### 1.2 工具调用与Function Call

**核心问题：** 如何让大模型突破知识边界，调用外部工具获取实时信息？

**知识点：**
- Function Calling的原理和机制
- 工具函数的定义和参数设计
- 工具调用的流程和最佳实践
- 多工具组合和链式调用
- 错误处理和容错机制

**实战案例：**
- 构建天气查询工具
- 地理位置和地图工具集成
- 酒店预订和价格比较工具

**配套代码：** `02_Tool_Use.ipynb`

#### 1.3 MCP (Model Context Protocol) 协议详解

**核心问题：** 如何标准化地让大模型与外部工具和数据源交互？

**知识点：**
- MCP协议的设计理念和架构
- Server-Client模式的工作原理
- 资源(Resources)、工具(Tools)、提示(Prompts)三大核心概念
- MCP服务端开发实践
- MCP客户端集成方法

**实战案例：**
- 构建MCP天气服务器
- 实现MCP客户端与DeepSeek/OpenAI集成
- MCP与LangChain的整合应用

**配套代码：**
- `server/weather_server.py` - MCP服务端实现
- `client/mcp_client_deepseek.py` - DeepSeek集成
- `client/mcp_client_langchain.py` - LangChain集成

**配套文档：**
- `docs/MCP（模型上下文协议）简介.md`
- `doc/weather_server.md` - 服务端开发指南
- `doc/mcp_client.md` - 客户端使用说明

#### 1.4 上下文工程 (Context Engineering)

**核心问题：** 如何有效管理和优化大模型的上下文窗口？

**知识点：**
- 上下文窗口的限制和优化策略
- 长文本的分块和检索方法
- 上下文的压缩和精简技巧
- RAG(检索增强生成)的基本原理
- 记忆管理和对话历史优化

**实战案例：**
- 旅游知识库的上下文管理
- 多轮对话的上下文优化
- 长篇文档的智能检索

**配套代码：** `context-engineer/prompt_to_context.ipynb`

**模块小结：**
通过本模块学习，你将掌握智能体的"输入输出"技能：如何通过精心设计的提示词让模型理解任务，如何通过工具调用让模型获取外部信息，如何通过MCP协议标准化工具集成，如何通过上下文工程优化模型表现。这些是构建实用智能体的基础能力。

---

### 模块二：多角色智能体系统

**📂 目录结构：** `02-agent-multi-role/`

#### 2.1 LangChain与LangGraph基础

**核心问题：** 如何从单一的LLM调用升级到复杂的智能体系统？

**知识点：**
- LangChain的核心概念：Chain、Agent、Memory、Tools
- LangGraph的设计理念：从链式到图状态
- 节点(Node)和边(Edge)的定义
- 状态管理和数据流转
- LangGraph vs 传统Chain的优势

**实战案例：**
- 构建第一个简单的LangGraph应用
- 从线性Chain到条件分支的演进
- 理解状态机的工作原理

**配套代码：**
- `0-Introduce/basics.ipynb` - LangGraph入门
- `1-Base/01-simple-graph.ipynb` - 简单图构建
- `1-Base/02-chain.ipynb` - 链式执行

**配套文档：**
- `0-docs/一文读懂「Lang Chain」langchain.md`
- `0-docs/01-Introduction_to_LangGraph_-_Motivation.pdf`

#### 2.2 状态管理与数据流

**核心问题：** 如何在多个智能体之间高效地传递和管理状态？

**知识点：**
- State Schema的设计原则
- 状态的创建、更新和查询
- State Reducers的使用方法
- 多Schema的场景和应用
- 消息过滤和裁剪策略

**实战案例：**
- 旅行规划中的状态设计
- 预算信息的跨Agent传递
- 用户偏好的状态管理

**配套代码：**
- `2-StateAndMemory/01-state-schema.ipynb` - 状态模式
- `2-StateAndMemory/02-state-reducers.ipynb` - 状态归约
- `2-StateAndMemory/03-multiple-schemas.ipynb` - 多模式
- `2-StateAndMemory/04-trim-filter-messages.ipynb` - 消息管理

#### 2.3 记忆与持久化

**核心问题：** 如何让智能体具备长期记忆能力？

**知识点：**
- 短期记忆 vs 长期记忆
- 对话历史的存储和检索
- 外部数据库的集成（SQLite、PostgreSQL）
- 记忆的总结和压缩策略
- Checkpointer的使用方法

**实战案例：**
- 实现智能体的对话记忆
- 用户画像的持久化存储
- 历史行程的检索和复用

**配套代码：**
- `1-Base/05-agent-memory.ipynb` - Agent记忆
- `2-StateAndMemory/05-chatbot-summarization.ipynb` - 对话总结
- `2-StateAndMemory/06-chatbot-external-memory.ipynb` - 外部记忆

**配套文档：**
- `0-docs/02-LangGraph记忆.pdf`
- `0-docs/02-Introduction_to_LangGraph_-_Long-Term_Memory.pdf`

#### 2.4 路由与决策

**核心问题：** 如何让智能体根据不同情况做出不同决策？

**知识点：**
- 条件边(Conditional Edge)的定义
- 路由函数的设计方法
- 多分支决策树的构建
- 动态路由的实现
- 循环和递归的处理

**实战案例：**
- 根据用户需求路由到不同Agent
- 预算判断的决策逻辑
- 异常情况的处理分支

**配套代码：**
- `1-Base/03-router.ipynb` - 路由机制
- `1-Base/04-agent.ipynb` - Agent决策

#### 2.5 人机交互 (Human-in-the-Loop)

**核心问题：** 如何让人类参与智能体的决策过程？

**知识点：**
- 中断(Interrupt)机制的原理
- 断点(Breakpoint)的设置方法
- 状态编辑和人工干预
- 动态断点的实现
- Time Travel和状态回溯

**实战案例：**
- 旅行方案的人工审核
- 预算超支的确认机制
- 行程调整的交互式编辑

**配套代码：**
- `3-HumanInTheLoop/01-streaming-interruption.ipynb` - 流式中断
- `3-HumanInTheLoop/02-breakpoints.ipynb` - 断点设置
- `3-HumanInTheLoop/03-edit-state-human-feedback.ipynb` - 状态编辑
- `3-HumanInTheLoop/04-dynamic-breakpoints.ipynb` - 动态断点
- `3-HumanInTheLoop/05-time-travel.ipynb` - 时间旅行

#### 2.6 多角色协作实战

**核心问题：** 如何设计和实现多个专业智能体的协作系统？

**知识点：**
- 角色分工的设计原则
- 并行执行 vs 串行执行
- 子图(Sub-graph)的组织方法
- Agent间的通信机制
- 冲突解决和决策融合

**实战案例：**
- 构建AI旅行规划多角色系统：
  - 需求分析师：理解用户意图
  - 行程规划师：设计路线和时间
  - 预算管理师：控制成本
  - 偏好学习师：个性化推荐
  - 协调调度器：整合最终方案

**配套代码：**
- `4-BuildYourAssiant/01-parallelization.ipynb` - 并行化执行
- `4-BuildYourAssiant/02-sub-graph.ipynb` - 子图构建

#### 2.7 LangGraph Cloud部署

**核心问题：** 如何将LangGraph应用部署到生产环境？

**知识点：**
- LangGraph Studio的使用
- API服务的部署方法
- 环境变量和配置管理
- 监控和日志记录
- 生产环境的最佳实践

**实战案例：**
- 部署DeepResearch智能体应用
- Docker容器化部署
- API接口的测试和调用

**配套代码和文档：**
- `deepresearch/deployment/` - 完整部署示例
- `deepresearch/01-deploy-deepresearch-creating.ipynb`
- `deepresearch/02-deploy-deepresearch-connecting.ipynb`
- `deepresearch/deployment/doc/QUICKSTART.md`
- `deepresearch/deployment/doc/配置说明.md`

**配套文档：**
- `0-docs/03-Introduction_to_LangGraph_-_Deployment.pdf`
- `LangGraph多角色Agent课程讲稿.md`

**模块小结：**
通过本模块学习，你将掌握构建复杂多角色智能体系统的核心能力：从单一Agent到多Agent协作，从简单链式到复杂图状态，从无状态到有记忆，从全自动到人机交互。这些技能将让你能够设计和实现企业级的智能体应用。

---

### 模块三：系统构建与容器化部署

**📂 目录结构：** `03-agent-build-docker-deploy/`

#### 3.1 系统架构设计

**核心问题：** 如何设计一个可扩展、可维护的智能体系统架构？

**知识点：**
- 分层架构设计：前端、后端、智能体层、工具层
- 模块化设计原则
- API接口设计规范(RESTful)
- 数据模型设计
- 配置管理和环境隔离

**架构图：**
- 系统架构总览
- LangGraph智能体协作工作流
- 数据模型与API交互流程
- 提示词和工具调用机制

**配套文档：**
- `docs/1-AI旅行规划智能体 - 系统架构总览.svg`
- `docs/2-AI旅行规划智能体 -LangGraph智能体协作工作流.svg`
- `docs/3-AI旅行规划智能体 - 数据模型与API交互流程.svg`
- `docs/5-AI旅行规划智能体 - 提示词和工具调用机制.svg`
- `docs/architecture_diagram.md`

#### 3.2 后端开发实战

**核心问题：** 如何用FastAPI构建高性能的智能体后端服务？

**知识点：**
- FastAPI框架基础
- API路由和请求处理
- 异步编程和并发处理
- 数据验证和错误处理
- API文档自动生成

**实战内容：**
- 智能体API接口实现
- 配置管理系统
- 工具集成层开发
- 数据模型定义

**配套代码：**
- `backend/api_server.py` - API服务器主程序
- `backend/agents/` - 智能体实现目录
  - `travel_agent.py` - 旅行智能体
  - `coordinator.py` - 协调器
  - `tools_agent.py` - 工具调用
- `backend/tools/` - 工具集成
  - `weather_tool.py` - 天气工具
  - `map_tool.py` - 地图工具
  - `hotel_tool.py` - 酒店工具
  - `search_tool.py` - 搜索工具
- `backend/config/` - 配置管理
- `backend/data/` - 数据模型
- `backend/utils/` - 工具函数

#### 3.3 前端开发实战

**核心问题：** 如何用Streamlit快速构建智能体交互界面？

**知识点：**
- Streamlit框架基础
- 交互组件的使用
- 状态管理和会话管理
- 流式输出和实时反馈
- 界面布局和样式定制

**实战内容：**
- 用户输入界面设计
- 对话历史展示
- 旅行方案可视化
- 实时状态反馈

**配套代码：**
- `frontend/streamlit_app.py` - 前端主程序

#### 3.4 Docker容器化部署

**核心问题：** 如何将智能体系统容器化并部署到生产环境？

**知识点：**
- Docker基础概念和命令
- Dockerfile编写最佳实践
- Docker Compose多容器编排
- 环境变量和配置注入
- 容器网络和数据卷

**实战内容：**
- 后端服务容器化
- 前端服务容器化
- Docker Compose一键部署
- 生产环境配置

**配套代码：**
- `backend/Dockerfile` - 后端容器配置
- `frontend/Dockerfile` - 前端容器配置
- `docker-compose.yml` - 编排配置
- `setup_environment.sh` - 环境初始化
- `start_backend.sh` - 后端启动脚本
- `start_frontend.sh` - 前端启动脚本

**配套文档：**
- `docs/4-AI旅行规划智能体 - Docker容器化部署架构图.svg`
- `docs/container_deployment_guide.md`

#### 3.5 企业级部署实践

**核心问题：** 如何将系统部署到企业生产环境？

**知识点：**
- 负载均衡和高可用
- 日志收集和监控
- 安全防护和权限管理
- CI/CD自动化部署
- 成本优化策略

**配套文档：**
- `docs/enterprise/` - 企业级部署指南
  - 高可用架构设计
  - 安全防护方案
  - 性能优化策略
  - 运维监控体系
  - 成本控制方案

**配套文档：**
- `docs/5-AI旅行Agent：基于LangGraph实战多角色智能体协作.md`
- `docs/6-AI旅行Agent：端到端项目构建与生产环境容器化部署.md`
- `docs/6-AI旅行Agent端到端项目构建PPT讲稿.md`

**模块小结：**
通过本模块学习，你将掌握从零到一构建企业级智能体系统的完整技能：系统架构设计、前后端开发、容器化部署、生产环境运维。你将获得一个可直接用于商业项目的完整代码库和部署方案。

---

### 模块四：智能体评估与监控

**📂 目录结构：** `04-agent-evaluation/`

#### 4.1 为什么需要评估体系？

**核心问题：** 如何衡量智能体系统的质量和性能？

**知识点：**
- 评估的必要性和价值
- 评估指标体系设计
- 评估 vs 监控 vs 调试
- 端到端评估框架

**配套文档：**
- `langfuse/大模型评估体系与Langfuse实战指南.md`

#### 4.2 Langfuse集成与追踪

**核心问题：** 如何追踪和记录智能体的执行过程？

**知识点：**
- Langfuse的核心概念：Trace、Span、Generation
- OpenAI SDK集成方法
- LangChain集成方法
- LangGraph集成方法
- 追踪数据的结构和分析

**实战案例：**
- 集成Langfuse到智能体系统
- 追踪多轮对话的执行过程
- 分析工具调用的性能

**配套代码：**
- `langfuse/01_01_integration_openai_sdk.ipynb` - OpenAI集成
- `langfuse/01_02_integration_langchain.ipynb` - LangChain集成
- `langfuse/01_03_integration_langgraph.ipynb` - LangGraph集成

#### 4.3 评估指标与方法

**核心问题：** 如何定义和计算智能体的评估指标？

**知识点：**
- 准确性(Accuracy)评估
- 相关性(Relevance)评估
- 安全性(Safety)评估
- 成本(Cost)评估
- 延迟(Latency)评估
- 自定义评估器的开发

**实战案例：**
- 旅行方案质量评估
- 工具调用准确性评估
- 用户满意度评估

**配套代码：**
- `langfuse/02_evaluation_with_langchain.ipynb` - LangChain评估

#### 4.4 LLM安全监控

**核心问题：** 如何防范智能体系统的安全风险？

**知识点：**
- Prompt注入攻击检测
- 敏感信息泄露防护
- 有害内容过滤
- 异常行为检测
- 实时告警机制

**实战案例：**
- 构建LLM安全监控系统
- 实时检测恶意输入
- 敏感信息脱敏处理

**配套代码：**
- `langfuse/04_example_llm_security_monitoring.ipynb` - 安全监控

#### 4.5 生产环境监控实践

**核心问题：** 如何在生产环境持续监控智能体性能？

**知识点：**
- 实时监控仪表盘
- 性能指标采集
- 异常检测和告警
- 用户反馈收集
- 持续优化迭代

**实战案例：**
- 构建智能体监控仪表盘
- 设置性能告警规则
- 分析用户行为数据

**配套代码：**
- `langfuse/03_example_langgraph_agents.ipynb` - LangGraph Agent监控

**配套文档：**
- `langfuse/docs/` - 评估方法论文档
- `langfuse/img/` - 可视化图表
- `langfuse/大模型智能体监测和评估课程大纲（精简版）.md`
- `langfuse/大模型智能体监测评估课程大纲与讲稿.md`

**模块小结：**
通过本模块学习，你将建立起完整的智能体评估和监控体系：从开发阶段的调试追踪，到测试阶段的质量评估，再到生产阶段的实时监控。你将能够量化智能体的性能，发现潜在问题，持续优化系统质量。

---

### 模块五：模型微调与优化

**📂 目录结构：** `05-agent-model-finetuning/`

#### 5.1 为什么需要模型微调？

**核心问题：** 什么时候应该考虑微调大模型？

**知识点：**
- 通用模型 vs 垂直领域模型
- 微调的适用场景和价值
- 微调 vs Prompt Engineering vs RAG
- 成本收益分析
- 微调策略选择

**配套文档：**
- `llamafactory/00-docs/01-大模型微调、推理、压测与评估.md`
- `llamafactory/00-docs/09-LLaMA Factory 技术白皮书：从入门到生产环境部署全链路指南.md`

#### 5.2 LoRA与PEFT技术

**核心问题：** 如何高效地进行大模型微调？

**知识点：**
- 全量微调 vs 参数高效微调(PEFT)
- LoRA(Low-Rank Adaptation)原理
- QLoRA量化微调技术
- Adapter、Prefix Tuning等其他PEFT方法
- 微调显存优化策略

**实战案例：**
- GPT-2模型的LoRA微调实践
- 垃圾短信分类任务微调
- 显存优化和参数调整

**配套代码：**
- `peft/lora-demo.ipynb` - LoRA基础示例
- `peft/lora-demo-optimized.ipynb` - LoRA优化版本
- `peft/training.ipynb` - 训练流程

**配套文档：**
- `llamafactory/00-docs/img/LLaMA Factory-微调显存优化策略的流程图.svg`
- `llamafactory/01-llm-fine-tuning/lora/README.md`

#### 5.3 LlamaFactory框架实战

**核心问题：** 如何使用LlamaFactory快速进行模型微调？

**知识点：**
- LlamaFactory框架介绍和架构
- 配置文件的编写方法
- 训练参数的调整策略
- 多GPU训练和分布式训练
- 模型合并和导出

**实战案例：**
- 使用LlamaFactory微调Qwen/Llama模型
- 医疗领域模型微调
- 金融领域模型微调

**配套代码：**
- `llamafactory/01-llm-fine-tuning/llamafactory/configs/` - 配置文件
  - `dtk2504-llamafactory092-ds32b-20250809.yaml`

**配套文档：**
- `llamafactory/00-docs/09-LLaMA Factory 技术白皮书：从入门到生产环境部署全链路指南.md`
- `llamafactory/00-docs/img/LLaMA Factory 参数体系.svg`

#### 5.4 微调数据集构建

**核心问题：** 如何准备高质量的微调数据？

**知识点：**
- 数据集格式：Alpaca、ShareGPT等
- 数据清洗和预处理
- 数据增强技术
- 数据质量评估
- Easy Dataset：让大模型高效学习领域知识

**实战案例：**
- 构建医疗问答数据集
- 构建金融分析数据集
- 使用TOC(Table of Contents)结构化数据

**配套代码和数据：**
- `llamafactory/01-llm-fine-tuning/dataset/` - 数据集目录
  - `MedicalData-2025/` - 医疗数据
  - `FinancialData-SecondQuarter-2024/` - 金融数据
  - `MedicalData-2025-For-LLaMA Factory/` - LlamaFactory格式数据
    - `alpaca.json` - Alpaca格式
    - `sharegpt.json` - ShareGPT格式
    - `dataset_info.json` - 数据集信息
    - `toc/` - 目录结构文件

**配套文档：**
- `llamafactory/00-docs/02-LLaMA Factory：Easy Dataset 让大模型高效学习领域知识.md`
- `llamafactory/00-docs/img/微调数据集构建方式.svg`
- `llamafactory/01-llm-fine-tuning/dataset/medical_o1_sft_Chinese_alpaca_cot/README.md`

#### 5.5 微调效果评估与优化

**核心问题：** 如何评估微调后的模型效果？

**知识点：**
- 评估指标选择：Loss、Perplexity、BLEU、ROUGE等
- 测试集设计和验证方法
- 过拟合和欠拟合的诊断
- 超参数调优策略
- 模型版本管理

**实战案例：**
- 评估旅游领域微调模型
- 对比微调前后的效果
- 迭代优化微调策略

#### 5.6 微调模型推理部署

**核心问题：** 如何将微调后的模型部署到生产环境？

**知识点：**
- 模型导出和格式转换
- LoRA权重的加载方法
- 推理服务的部署方式
- 性能优化和加速技巧

**配套代码：**
- `llamafactory/02-llm-inference/llm-infer-test.sh` - 推理测试脚本

**配套文档：**
- `llamafactory/00-docs/03-vLLM大模型推理部署.md`
- `llamafactory/00-docs/03-大模型推理部署.md`

**模块小结：**
通过本模块学习，你将掌握大模型微调的完整流程：从理解微调的适用场景，到选择合适的微调方法（LoRA/PEFT），再到使用LlamaFactory进行实际微调，最后到效果评估和部署。你将能够针对特定领域定制化自己的大模型，大幅提升智能体在垂直场景的表现。

---

### 模块六：模型推理部署

**📂 目录结构：** `06-agent-model-inference/`

#### 6.1 大语言模型推理基础

**核心问题：** 大语言模型推理的核心概念和挑战是什么？

**知识点：**
- LLM推理的基本流程
- Prefill阶段 vs Decode阶段
- 推理延迟的来源分析
- 吞吐量vs延迟的权衡
- 推理成本构成

**配套文档：**
- `LLM 推理（LLM Inference）.md`
- `大语言模型推理：核心概念、挑战与优化方案.md`
- `vllm/大语言模型推理：核心概念、挑战与优化方案.md`

#### 6.2 Transformers推理框架

**核心问题：** 如何使用Transformers进行模型推理？

**知识点：**
- Transformers库的基本使用
- Pipeline API快速上手
- 模型加载和配置
- 批处理和并发推理
- 流式输出实现

**实战案例：**
- 加载和使用预训练模型
- 实现流式对话应用
- 批量文本生成任务

**配套代码：**
- `transformer/llm_tutorial.ipynb` - LLM教程
- `transformer/transformer-quicktour.ipynb` - Transformers快速入门

**配套文档：**
- `Transformers.md`
- `transformer/Transformers.md`

#### 6.3 vLLM高性能推理

**核心问题：** 如何实现大规模、高吞吐的模型推理服务？

**知识点：**
- vLLM的核心技术：PagedAttention
- Continuous Batching持续批处理
- KV Cache优化策略
- 张量并行和流水线并行
- vLLM vs Transformers性能对比

**实战案例：**
- 使用vLLM部署Qwen/Llama模型
- 构建OpenAI兼容的API服务
- 性能调优和参数配置

**配套代码：**
- `vllm/code/` - vLLM代码示例

**配套文档：**
- `vllm/README.md`
- `vllm/LLM 推理（LLM Inference）.md`
- `vllm/大语言模型推理：核心概念、挑战与优化方案.md`

#### 6.4 推理优化技术

**核心问题：** 如何进一步优化推理性能？

**知识点：**
- 模型量化：INT8、INT4、GPTQ、AWQ
- 投机解码(Speculative Decoding)
- FlashAttention加速技术
- 内存优化和显存管理
- 多模型服务和资源调度

**实战案例：**
- 量化模型的加载和使用
- FlashAttention集成
- 多GPU推理部署

#### 6.5 生产环境推理服务

**核心问题：** 如何构建稳定可靠的生产级推理服务？

**知识点：**
- 服务高可用架构设计
- 负载均衡和请求调度
- 错误处理和容错机制
- 日志监控和性能分析
- 自动扩缩容策略

**实战案例：**
- 构建企业级推理服务
- 实现请求队列和限流
- 监控推理性能指标

**配套文档：**
- `vllm/README.md` - 包含生产部署指南

**模块小结：**
通过本模块学习，你将掌握大语言模型推理部署的核心技能：理解推理的底层原理和性能瓶颈，掌握Transformers和vLLM两大推理框架，学会各种推理优化技术，最终能够构建高性能、高可用的生产级推理服务。这些技能将帮助你在保证服务质量的同时，大幅降低推理成本。

---

### 模块七：性能压测与评估

**📂 目录结构：** `07-agent-llm_benchmark/`

#### 7.1 为什么需要性能压测？

**核心问题：** 如何定量评估推理服务的性能？

**知识点：**
- 性能压测的必要性
- 核心性能指标：吞吐量、延迟、并发数
- 压测 vs 评估 vs 监控
- 压测场景设计

**配套文档：**
- `vLLM推理服务压测框架：让大模型性能评估有据可依.md`

#### 7.2 vLLM Benchmark压测框架

**核心问题：** 如何系统化地进行大模型推理服务压测？

**知识点：**
- vLLM Benchmark工具介绍
- 压测配置和参数设置
- 并发请求的模拟方法
- 数据采集和统计分析
- 压测报告生成

**实战案例：**
- 压测Qwen/DeepSeek模型
- 不同并发度的性能对比
- 不同参数配置的性能分析

**配套代码：**
- `llm_benchmark/main.py` - 压测主程序
- `llm_benchmark/config.yaml` - 配置文件
- `llm_benchmark/src/` - 源代码目录
  - 指标采集模块
  - 数据分析模块
  - 报告生成模块
  - 可视化模块

#### 7.3 性能指标体系

**核心问题：** 如何全面评估推理服务的性能？

**知识点：**
- 吞吐量(Throughput)：请求数/秒、Token数/秒
- 延迟(Latency)：首Token延迟(TTFT)、Token间延迟(TPOT)
- 并发能力：最大并发数、排队时间
- 资源利用：GPU利用率、显存占用、CPU使用率
- 成本效率：每美元处理请求数、TCO分析

**实战案例：**
- 采集和分析各项性能指标
- 绘制性能曲线和热力图
- 识别性能瓶颈

**配套代码：**
- `llm_benchmark/src/` - 指标采集和分析代码

#### 7.4 压测报告与可视化

**核心问题：** 如何直观地呈现压测结果？

**知识点：**
- 压测报告的结构设计
- 数据可视化最佳实践
- 性能曲线和趋势分析
- 对比分析和基准测试
- 结论和优化建议

**实战案例：**
- 生成详细的压测报告
- 绘制性能对比图表
- 撰写优化建议

**配套代码和资源：**
- `llm_benchmark/reports/` - 压测报告目录
- `llm_benchmark/charts/` - 可视化图表
- `llm_benchmark/docs/` - 使用文档

#### 7.5 性能优化实践

**核心问题：** 基于压测结果如何优化推理服务？

**知识点：**
- 瓶颈诊断方法
- 参数调优策略（batch size、max_tokens等）
- 硬件配置优化
- 模型优化（量化、剪枝）
- 系统级优化（缓存、预热）

**实战案例：**
- 基于压测结果进行参数调优
- 对比优化前后的性能提升
- 制定成本优化方案

**配套文档：**
- `llm_benchmark/docs/` - 优化指南
- `vLLM推理服务压测框架：让大模型性能评估有据可依.md`

**模块小结：**
通过本模块学习，你将建立起完整的推理性能评估体系：从设计压测场景，到使用vLLM Benchmark进行系统化压测，再到分析性能指标和生成报告，最后到基于数据进行优化。你将能够定量评估推理服务的性能，发现瓶颈，持续优化系统，实现性能和成本的最佳平衡。

---

## 🎯 学习路径建议

### 初级学习者（0-6个月AI经验）

**学习顺序：**
1. **模块一：工具调用与MCP协议** (2周)
   - 重点掌握提示词工程和Function Call
   - 熟悉MCP协议的基本使用
   - 完成至少3个工具调用实战

2. **模块二：多角色智能体系统** (3周)
   - 从简单的LangGraph应用开始
   - 循序渐进学习状态管理和记忆
   - 构建一个简单的多角色系统

3. **模块三：系统构建与容器化部署** (2周)
   - 掌握FastAPI和Streamlit基础
   - 完成旅行智能体的部署
   - 学会Docker的基本使用

4. **模块四：智能体评估与监控** (1周)
   - 集成Langfuse进行追踪
   - 建立基本的评估指标

**后续学习：**
- 模块五、六、七为高级内容，建议在有一定经验后再学习

### 中级学习者（6-18个月AI经验）

**学习顺序：**
1. **快速回顾模块一和二** (1周)
   - 重点关注MCP协议和LangGraph高级特性
   
2. **深入学习模块三** (2周)
   - 掌握企业级部署实践
   - 学习高可用架构设计

3. **模块四：智能体评估与监控** (2周)
   - 建立完整的评估体系
   - 实现生产环境监控

4. **模块五：模型微调与优化** (2-3周)
   - 掌握LoRA和LlamaFactory
   - 完成垂直领域模型微调

5. **模块六：模型推理部署** (2周)
   - 掌握vLLM部署和优化
   - 构建高性能推理服务

6. **模块七：性能压测与评估** (1周)
   - 建立完整的压测体系
   - 进行系统性能优化

### 高级学习者（18个月以上AI经验）

**学习策略：**
- 可以选择性学习感兴趣的模块
- 重点关注企业级实践和优化技巧
- 结合自己的项目进行深度实践
- 参与社区讨论和贡献

**建议重点：**
- 模块五、六、七的高级优化技术
- 模块三的企业级部署实践
- 模块四的完整监控体系

---

## 🛠️ 技术栈与环境要求

### 💻 开发环境

| 组件 | 推荐配置 | 最低配置 |
|------|---------|---------|
| **操作系统** | Ubuntu 22.04 LTS | Ubuntu 20.04+ / Windows 10+ / macOS 12+ |
| **CPU** | 8 核心 | 4 核心 |
| **内存** | 16 GB | 8 GB |
| **存储** | 200 GB SSD | 100 GB |
| **GPU** | NVIDIA RTX 3090/4090 (24GB) | NVIDIA GTX 1080 (8GB) 或无GPU |
| **Python** | 3.10.x | 3.9+ |

### 📦 核心依赖

```python
# 智能体框架
langchain==0.3.x
langgraph==0.3.x
langchain-openai==0.3.x

# MCP协议
mcp==1.5.0

# Web框架
fastapi==0.115.0
streamlit==1.41.1

# 模型微调
transformers==4.46.0
peft==0.13.2
llamafactory==0.9.2

# 推理服务
vllm==0.6.2
torch==2.4.0

# 评估监控
langfuse==3.3.0
langsmith==0.1.x

# 工具库
httpx==0.27.0
pydantic==2.9.0
```

### 🔑 API密钥准备

| API服务 | 用途 | 获取方式 | 是否必需 |
|---------|------|---------|---------|
| **OpenAI API** | GPT-4/GPT-3.5 | https://platform.openai.com | 可选 |
| **DeepSeek API** | DeepSeek-R1/Chat | https://platform.deepseek.com | 推荐 |
| **和风天气 API** | MCP天气工具 | https://dev.qweather.com | 模块一必需 |
| **Tavily API** | LangGraph搜索 | https://tavily.com | 模块二推荐 |
| **Langfuse** | 评估监控 | https://cloud.langfuse.com | 模块四必需 |
| **LangSmith** | LangChain监控 | https://smith.langchain.com | 模块四可选 |

---

## ❓ 常见问题 FAQ

### Q1: 我没有GPU，能学习这门课程吗？

**A:** 可以！大部分内容都可以在CPU环境下学习：
- 模块一到四：完全不需要GPU，使用云端API即可
- 模块五（微调）：可以使用Google Colab的免费GPU
- 模块六、七（推理和压测）：可以使用云端推理服务，或者学习理论知识

### Q2: 这门课需要多长时间学完？

**A:** 取决于你的基础和投入时间：
- **全职学习**：8-10周可以完成基础内容
- **业余学习**（每周10-15小时）：3-4个月完成核心内容
- **深度实践**：建议预留6-12个月时间，结合实际项目深化理解

### Q3: 课程代码支持哪些大模型？

**A:** 课程设计具有很好的模型兼容性：
- **支持的LLM**：OpenAI GPT系列、DeepSeek、Claude、Qwen、Llama、GLM等
- **推荐使用**：DeepSeek（性价比高，中文友好）或GPT-4（效果最好）
- **替换方式**：代码采用统一的LLM接口，切换模型只需修改配置

### Q4: 微调需要多大的数据集？

**A:** 取决于任务类型和目标效果：
- **最小数据量**：100-500条高质量数据可以看到初步效果
- **推荐数据量**：1000-5000条数据可以获得较好效果
- **大规模微调**：10000+条数据适合生产环境
- **数据质量**：比数量更重要，课程中会详细讲解数据构建

### Q5: 部署到生产环境需要注意什么？

**A:** 课程中会详细讲解，核心要点包括：
- **高可用**：负载均衡、服务冗余、故障转移
- **安全性**：API鉴权、输入验证、敏感信息保护
- **性能**：缓存策略、并发控制、资源限制
- **监控**：日志收集、性能指标、告警机制
- **成本**：请求限流、模型选择、资源优化

### Q6: 课程项目能否用于商业项目？

**A:** 可以！但需要注意：
- **代码许可**：项目采用MIT协议，可自由使用和修改
- **API费用**：生产环境需要自行承担API调用费用
- **模型许可**：确认使用的大模型支持商业使用
- **数据合规**：确保用户数据处理符合隐私法规

### Q7: 如何获得学习支持？

**A:** 多种支持渠道：
- **GitHub Issues**：技术问题和Bug报告
- **GitHub Discussions**：学习交流和经验分享
- **微信公众号**：萤火AI百宝箱 - 技术文章和更新
- **代码注释**：项目代码有详细的中文注释
- **配套文档**：每个模块都有完整的技术文档

---

## 📚 推荐学习资源

### 官方文档

- **LangChain文档**: https://python.langchain.com/docs
- **LangGraph文档**: https://langchain-ai.github.io/langgraph
- **MCP规范**: https://modelcontextprotocol.io
- **vLLM文档**: https://docs.vllm.ai
- **LlamaFactory文档**: https://github.com/hiyouga/LLaMA-Factory
- **Langfuse文档**: https://langfuse.com/docs

### 扩展阅读

- **大模型基础**: 
  - Attention Is All You Need (Transformer论文)
  - GPT系列论文
  
- **智能体理论**:
  - ReAct: Synergizing Reasoning and Acting in Language Models
  - AutoGPT、BabyAGI等开源项目

- **提示词工程**:
  - Prompt Engineering Guide
  - OpenAI Prompt Engineering

- **模型微调**:
  - LoRA: Low-Rank Adaptation of Large Language Models
  - QLoRA: Efficient Finetuning of Quantized LLMs

### 推荐工具

- **开发工具**: VS Code、PyCharm、Cursor
- **调试工具**: LangSmith、LangGraph Studio
- **部署工具**: Docker、Kubernetes、Portainer
- **监控工具**: Prometheus、Grafana、Langfuse

---

## 🎓 学习目标检查清单

### ✅ 模块一：工具调用与MCP协议

- [ ] 能够编写高质量的提示词，实现复杂任务
- [ ] 掌握Function Calling，能够集成外部工具
- [ ] 理解MCP协议，能够开发MCP服务端和客户端
- [ ] 掌握上下文管理和优化策略
- [ ] 完成至少3个工具调用的实战项目

### ✅ 模块二：多角色智能体系统

- [ ] 理解LangGraph的核心概念和设计理念
- [ ] 能够设计和实现复杂的状态管理方案
- [ ] 掌握记忆和持久化技术
- [ ] 能够实现条件路由和动态决策
- [ ] 掌握人机交互的交互设计
- [ ] 能够构建多角色协作的智能体系统
- [ ] 完成AI旅行规划智能体项目

### ✅ 模块三：系统构建与容器化部署

- [ ] 能够设计可扩展的智能体系统架构
- [ ] 掌握FastAPI后端开发
- [ ] 掌握Streamlit前端开发
- [ ] 能够使用Docker进行容器化部署
- [ ] 理解企业级部署的最佳实践
- [ ] 完成完整系统的部署和上线

### ✅ 模块四：智能体评估与监控

- [ ] 理解评估体系的必要性和价值
- [ ] 能够集成Langfuse进行追踪
- [ ] 掌握各类评估指标的定义和计算
- [ ] 能够构建LLM安全监控系统
- [ ] 建立生产环境的监控和告警机制

### ✅ 模块五：模型微调与优化

- [ ] 理解模型微调的适用场景
- [ ] 掌握LoRA和PEFT技术
- [ ] 能够使用LlamaFactory进行模型微调
- [ ] 掌握微调数据集的构建方法
- [ ] 能够评估微调效果并进行优化
- [ ] 完成至少一个垂直领域的模型微调

### ✅ 模块六：模型推理部署

- [ ] 理解LLM推理的核心概念和挑战
- [ ] 掌握Transformers推理框架
- [ ] 掌握vLLM高性能推理部署
- [ ] 了解各种推理优化技术
- [ ] 能够构建生产级推理服务

### ✅ 模块七：性能压测与评估

- [ ] 理解性能压测的必要性
- [ ] 掌握vLLM Benchmark压测框架
- [ ] 能够设计完整的性能指标体系
- [ ] 能够生成专业的压测报告
- [ ] 掌握基于数据的性能优化方法

---

## 🚀 课程总结

通过学习《Agentic AI 智能体开发实战》课程，你将获得：

### 🎯 核心技能

1. **工具集成能力**：掌握Function Call、MCP协议、上下文工程，让智能体能够调用外部工具和服务
2. **系统设计能力**：掌握LangGraph多角色协作、状态管理、人机交互等核心技术
3. **工程实践能力**：掌握FastAPI、Streamlit、Docker等技术栈，实现完整的系统开发和部署
4. **评估优化能力**：掌握Langfuse评估、LLM安全监控、持续优化的方法论
5. **模型定制能力**：掌握LoRA/LlamaFactory微调技术，定制垂直领域模型
6. **推理部署能力**：掌握vLLM高性能推理部署和优化技术
7. **性能评估能力**：掌握vLLM Benchmark压测和性能优化方法

### 💼 实战项目

- **AI旅行规划智能体**：完整的企业级多角色智能体系统
- **MCP工具集成**：天气查询、地图导航等工具的标准化集成
- **Docker化部署方案**：可直接用于生产环境的容器化部署
- **评估监控系统**：完整的Langfuse集成和安全监控
- **垂直领域微调**：医疗、金融等领域的模型定制
- **高性能推理服务**：基于vLLM的企业级推理部署
- **性能压测框架**：完整的vLLM Benchmark压测体系

### 🔮 职业发展

完成本课程后，你将具备：

- **AI工程师岗位**：能够独立开发和部署AI应用
- **智能体架构师**：能够设计复杂的多角色协作系统
- **AI产品经理**：深度理解AI技术实现和商业化路径
- **技术团队负责人**：能够评估技术方案和管理AI项目
- **AI创业者**：掌握从0到1构建AI产品的完整技能

### 🌟 持续学习

AI技术日新月异，建议：

1. **关注前沿**：持续关注LangChain、OpenAI、Anthropic等的技术更新
2. **实践驱动**：将所学应用到实际项目中，在实践中深化理解
3. **社区参与**：参与开源项目，与社区交流学习
4. **扩展应用**：将智能体技术扩展到更多垂直领域
5. **技术创新**：探索Agentic AI 智能体的新场景和新玩法



