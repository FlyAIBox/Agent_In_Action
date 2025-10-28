# 从0到1打造多角色AI Agent - 完整学习指南

<div align="center">

![AI Agent Logo](https://img.shields.io/badge/AI-Agent-brightgreen?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.10.18-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.3.x-orange?style=for-the-badge&logo=langchain)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**企业级AI旅行规划智能体 · 从理论到实战的全链路开发技能**

[快速开始](#-快速开始) • [课程内容](#-课程内容) • [技术栈](#-技术栈) • [实战项目](#-实战项目) • [环境搭建](#-环境搭建)

</div>

---

## 📚 课程简介

### 🎯 课程目标

本课程聚焦"从零到一"构建企业级AI旅行规划智能体，旨在帮助学员掌握从理论到实战的全链路开发技能。通过实战驱动的学习路径，学员将能够独立开发可商用的AI旅行规划解决方案，并获得在AI应用开发领域的就业竞争力。

### 👥 适合人群

| 人群类型 | 适用场景 | 收获价值 |
|---------|----------|----------|
| **AI开发初学者** | 计算机专业学生或对AI感兴趣的开发者 | 系统学习大模型应用开发 |
| **旅游科技团队** | 需要快速掌握AI旅行规划技术的开发团队 | 实用的技术解决方案 |
| **转型工程师** | 从传统软件开发转向AI+旅游方向 | 新技术栈的掌握和应用 |
| **创业者/产品经理** | 进行产品规划和商业模式探索 | 技术实现的深度理解 |

### 🎨 课程特色

- **📈 通用框架**：核心架构可应用于医疗、金融、科研等不同行业
- **🎯 实战导向**：以完整的AI旅行规划项目为核心案例
- **🔧 技术前沿**：涵盖MCP、n8n、vLLM、多智能体协作等最新技术
- **💼 企业级解决方案**：满足真实业务需求，注重性能优化和成本控制
- **🎓 职业发展**：包含面试技巧和职业规划指导

---

## 📖 课程内容

### 🧭 课程大纲速览

| 序号 | 课程主题 | 配套资料 | 能力产出 |
|------|----------|----------|----------|
| 00 | 🛠️ 环境与API | `00-agent-env/` | 配好开发栈，能拉起基础推理服务 |
| 01 | 🧠 提示词核心 | `01-agent-prompt-or-context/` | 写出稳健提示词，控制模型行为 |
| 02 | 🔌 工具链集成 | `02-agent-llm-mcp/` | 让智能体接入外部工具，拓展执行边界 |
| 03 | 🤝 多角色协作 | `03-agent-multi-role/` | 搭建旅行智能体的协作骨架 |
| 04 | 🏗️ 系统搭建 | `04-agent-build-docker-deploy/` | 组装前后端与容器化部署方案 |
| 05 | 📊 评估体系 | `05-agent-evaluation/` | 建立质量与安全评估闭环 |
| 06 | 🔄 业务编排 | `06-agent-workflow-n8n/` | 零代码快速接入业务流程 |
| 07 | 🔧 模型微调 | `07-agent-model-finetuning/` | 打造垂直领域定制模型适配器 |
| 08 | 🎯 模型推理 | `08-agent-model-inference/` | 部署高吞吐推理服务，掌握性能杠杆 |
| 09 | 🚀 性能压测 | `09-agent-llm_benchmark/` | 定量衡量推理性能并持续优化 |
| 10 | 🧭 职业发展 | `10-agent-review/` | 沟通项目价值，准备求职答辩 |
| 11 | ✨ 行业洞察 | `11-agent-docs/` | 固化方法论，规划后续进阶路径 |

### 🏆 课程收获

| 收获类别 | 具体内容 |
|----------|----------|
| **🛠️ 完整技术栈** | 掌握从环境搭建到企业级部署的完整AI旅行规划技术链路 |
| **💼 实战项目** | 获得可直接应用于旅游业务场景的实战项目经验 |
| **🔬 前沿技术** | 深入理解MCP、n8n、vLLM、多智能体协作、大模型微调等最新技术 |
| **🏭 企业级能力** | 学习如何降低推理成本/微调垂直模型/压测和评估等，提升系统性能和稳定性 |
| **💡 职业发展** | 获得AI应用开发领域的面试技巧和职业发展指导 |

### 📋 课程大纲

#### 📁 00. 环境准备阶段
```
📂 00-agent-env/
├── 🐧 00-linux_ops/                 - Ubuntu 22.04 运维脚本与常用命令
├── 🐍 01-python-base/               - Python 3.10.18 环境与依赖管理
├── 📓 02-jupyter-ops/               - JupyterLab 扩展与多内核配置
├── 🎯 03-cursor-ops/                - Cursor 辅助开发配置与实践
├── 🐳 04-docker-ops/                - Milvus 等核心服务的容器化部署
├── ☁️ 05-colab-ops/                 - Google Colab 云端开发环境
├── 🧪 first_llm_app.py              - 第一次调用大模型 API 的示例
└── ⚙️ setup_agent101_dev.sh         - 本地一键环境初始化脚本
```

#### 🧠 01. 提示词与上下文工程
```
📂 01-agent-prompt-or-context/
├── 🧱 prompt-enginner/              - 提示词结构化设计与角色模板
├── 🔁 context-engineer/             - 上下文记忆管理与检索策略
├── 🌟 prompts_best_practice/        - 图文与视频提示词最佳实践合集
└── 📚 docs/                         - 理论笔记与案例解析
```

#### 🔌 02. 工具链集成与 MCP
```
📂 02-agent-llm-mcp/
├── 📚 docs/                         - MCP Illustrated Guidebook 等资料
└── 🧪 mcp-demo/                     - 完整的工具调用 Demo
    ├── server/                      - MCP 服务端实现
    ├── client/                      - MCP 客户端示例
    └── doc/                         - 流程说明与操作指南
```

#### 🤝 03. 多角色智能体系统
```
📂 03-agent-multi-role/
├── 🖼️ img/                          - 多角色协作流程图与示例
└── 🕸️ langgraph/                    - LangGraph 多角色示例工程
    ├── 0-Introduce/                 - 课程引导与环境说明
    ├── 1-Base/                      - 基础节点与状态管理
    ├── 2-StateAndMemory/            - 记忆与上下文持久化策略
    ├── 3-HumanInTheLoop/            - 人在回路的交互设计
    ├── 4-BuildYourAssiant/          - 多角色旅行助手搭建
    └── 5-LongTermMemroy/            - 长期记忆与回访机制
```

#### 🏗️ 04. 系统搭建与容器化
```
📂 04-agent-build-docker-deploy/
├── ⚙️ backend/                      - FastAPI 等后端服务实现
├── 💻 frontend/                     - Web 前端界面与交互
├── 🐳 docker/                       - Docker 与 Compose 部署配置
├── 📚 docs/                         - 架构说明与运维手册
├── 🚀 setup_environment.sh          - 环境初始化脚本
├── ▶️ start_backend.sh              - 后端启动脚本
└── ▶️ start_frontend.sh             - 前端启动脚本
```

#### 📈 05. 智能体评估体系
```
📂 05-agent-evaluation/
└── 📊 langfuse/                     - Langfuse 指标、评估流程与图示
```

#### 🔄 06. 工作流自动化
```
📂 06-agent-workflow-n8n/
├── 📘 doc/                          - n8n 平台介绍与操作手册
├── 🖼️ images/                       - 界面截图与流程示意
├── 🧩 template/                     - n8n 工作流模板集合
├── 📄 n8n服务管理脚本使用说明.md    - 服务管理脚本使用指南
└── 🛠️ n8n-manager.sh               - n8n 服务管理脚本
```

#### 🔧 07. 模型微调与优化
```
📂 07-agent-model-finetuning/
├── 🦙 llamafactory/                 - LlamaFactory 微调流程与实验记录
└── 📊 peft/                         - LoRA/PEFT 策略与适配器示例
```

#### 🎯 08. 模型推理部署
```
📂 08-agent-model-inference/
├── 📘 Transformers.md               - Transformers 入门与速查
├── 🤖 transformer/                  - 基础示例与 Notebook
├── ⚡ vllm/                          - vLLM 部署、扩展与性能调优
├── 🧭 大语言模型推理：核心概念、挑战与优化方案.md
└── 📄 LLM 推理（LLM Inference）.md  - 推理服务详细说明
```

#### 🚀 09. 性能压测框架
```
📂 09-agent-llm_benchmark/
├── 📈 llm_benchmark/                - 压测脚本、配置与报告
│   ├── src/                         - 指标采集与分析代码
│   ├── reports/                     - 测试报告与总结
│   ├── charts/                      - 可视化素材
│   ├── docs/                        - 使用说明
│   ├── main.py                      - 压测入口
│   └── config.yaml                  - 参数配置
└── 📄 vLLM推理服务压测框架：让大模型性能评估有据可依.md
```

#### 🧭 10. 职业发展与项目复盘
```
📂 10-agent-review/
└── 📝 README.MD                     - 面试考点与复盘方法
```

#### ✨ 11. 行业洞察与延展阅读
```
📂 11-agent-docs/
├── 📑 lecture/                      - 课程讲义与演示素材
├── 🖼️ img/                          - 行业趋势与架构图
└── 📄 *.pdf                         - 行业报告与白皮书合集
```

---

## 🛠️ 技术栈

### 🏗️ 系统架构图

```mermaid
graph TB
    A[用户界面层] --> B[智能体协调层]
    B --> C[LangGraph多角色系统]
    B --> D[MCP工具集成层]
    
    C --> E[旅行规划智能体]
    C --> F[预算管理智能体]
    C --> G[行程优化智能体]
    
    D --> H[天气查询工具]
    D --> I[地图导航工具]
    D --> J[酒店预订工具]
    
    E --> K[大模型推理层]
    F --> K
    G --> K
    
    K --> L[vLLM推理引擎]
    L --> M[DeepSeek-R1模型]
    L --> N[微调适配器]
    
    O[工作流自动化] --> P[n8n平台]
    P --> Q[数据处理节点]
    P --> R[AI服务节点]
    
    S[评估监控] --> T[Langfuse平台]
    T --> U[性能监控]
    T --> V[质量评估]
    
    W[压测框架] --> X[vLLM基准测试]
    X --> Y[性能指标收集]
    X --> Z[可视化报告]
```

### 🔧 核心技术组件

| 技术领域 | 核心技术 | 版本 | 应用场景 |
|---------|----------|------|----------|
| **🧠 大语言模型** | GPT/DeepSeek-R1 | 4o/32B | 核心推理引擎 |
| **⚡ 推理框架** | vLLM | 0.8.5+ | 高性能推理服务 |
| **🔗 智能体框架** | LangChain + LangGraph | 0.3.x  | 多角色协作系统 |
| **🌐 模型上下文协议** | MCP (Model Context Protocol) | 1.5.0 | 工具集成协议 |
| **🎯 微调框架** | LlamaFactory | 0.9.2 | 模型个性化微调 |
| **📊 评估平台** | Langfuse | 3.3.0 | 性能监控与评估 |
| **📋 模型压测** | vLLM Benchmark | 0.8.5+ | 大模型推理服务压测 |
| **🔄 工作流引擎** | n8n | 1.101.1 | 自动化流程编排 |
| **🐍 运行环境** | Python/Docker/DockerCompose | 3.10+/20+ | 开发环境 |


## 🏨 实战项目

### 🎯 核心项目：AI旅行规划智能体

#### 📋 项目概述

构建一个企业级的AI旅行规划智能体系统，该系统能够：

- **🗣️ 自然语言交互**：理解用户的旅行需求和偏好
- **👥 多角色协作**：多个专业智能体协同工作
- **🔧 工具集成**：调用外部API获取实时信息
- **📊 个性化推荐**：基于用户画像生成定制化方案
- **💰 成本优化**：平衡预算约束和体验质量

#### 🤖 智能体角色设计

| 智能体角色 | 核心职责 | 技能特长 | 工具集成 |
|-----------|----------|----------|----------|
| **🎯 需求分析师** | 理解用户需求，提取关键信息 | 自然语言理解、意图识别 | 对话管理、信息抽取 |
| **🗺️ 行程规划师** | 设计旅行路线和时间安排 | 地理知识、时间规划 | 地图API、交通查询 |
| **💰 预算管理师** | 控制成本，优化性价比 | 价格分析、成本控制 | 价格比较API、预算工具 |
| **❤️ 偏好学习师** | 学习用户偏好，个性化推荐 | 推荐算法、用户画像 | 评分系统、偏好数据库 |
| **🔧 协调调度器** | 协调各智能体，生成最终方案 | 决策融合、冲突解决 | 状态管理、结果整合 |


### 🏥 扩展案例：医疗智能体

#### 🩺 眼科诊断助手系统

基于相同的技术框架，展示如何将旅游智能体架构扩展到医疗领域：

**核心功能**：
- 📝 症状智能分析和疾病初筛
- 🔍 医学影像辅助诊断
- 💊 个性化治疗方案推荐
- ⚠️ 风险评估和预警系统
- 📋 病历智能生成和管理

---

## 📁 项目结构

```
AIAgent101/
├── 00-agent-env/                     # 环境配置与基础设施
│   ├── 00-linux_ops/
│   ├── 01-python-base/
│   ├── 02-jupyter-ops/
│   ├── 03-cursor-ops/
│   ├── 04-docker-ops/
│   ├── 05-colab-ops/
│   ├── first_llm_app.py
│   └── setup_agent101_dev.sh
│
├── 01-agent-prompt-or-context/       # 提示词与上下文工程
│   ├── context-engineer/
│   ├── prompt-enginner/
│   ├── prompts_best_practice/
│   └── docs/
│
├── 02-agent-llm-mcp/                 # MCP 协议与工具链
│   ├── docs/
│   └── mcp-demo/
│       ├── client/
│       ├── server/
│       └── doc/
│
├── 03-agent-multi-role/              # 多角色智能体系统
│   ├── img/
│   └── langgraph/
│       ├── 0-Introduce/
│       ├── 1-Base/
│       ├── 2-StateAndMemory/
│       ├── 3-HumanInTheLoop/
│       ├── 4-BuildYourAssiant/
│       └── 5-LongTermMemroy/
│
├── 04-agent-build-docker-deploy/     # 系统搭建与容器部署
│   ├── backend/
│   ├── frontend/
│   ├── docker/
│   ├── docs/
│   ├── setup_environment.sh
│   ├── start_backend.sh
│   └── start_frontend.sh
│
├── 05-agent-evaluation/              # 智能体评估体系
│   └── langfuse/
│
├── 06-agent-workflow-n8n/            # 业务流程自动化
│   ├── doc/
│   ├── images/
│   ├── template/
│   ├── n8n-manager.sh
│   ├── n8n服务管理脚本使用说明.md
│   └── README.MD
│
├── 07-agent-model-finetuning/        # 模型微调与优化
│   ├── llamafactory/
│   └── peft/
│
├── 08-agent-model-inference/         # 大模型推理部署
│   ├── transformer/
│   ├── vllm/
│   ├── Transformers.md
│   ├── 大语言模型推理：核心概念、挑战与优化方案.md
│   └── LLM 推理（LLM Inference）.md
│
├── 09-agent-llm_benchmark/           # 推理性能压测
│   ├── llm_benchmark/
│   │   ├── src/
│   │   ├── reports/
│   │   ├── charts/
│   │   ├── docs/
│   │   ├── main.py
│   │   └── config.yaml
│   └── vLLM推理服务压测框架：让大模型性能评估有据可依.md
│
├── 10-agent-review/                  # 项目复盘与职业规划
│   └── README.MD
│
├── 11-agent-docs/                    # 行业洞察与参考资料
│   ├── lecture/
│   ├── img/
│   └── *.pdf
│
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🛠️ 环境搭建

### 💻 系统要求

#### 🏗️ 硬件环境
| 组件 | 当前配置 | 说明 |
|------|----------|------|
| **🖥️ 操作系统** | Ubuntu 22.04.4 LTS · 内核 5.15.0-157 | 运行在 VMware 虚拟机 |
| **🧠 CPU** | 4 vCPU · Intel Core i5-1135G7 @ 2.40GHz | Hypervisor: VMware |
| **💾 内存** | 6 GiB | 未配置 Swap |
| **💿 存储** |  150 GB | 最小100 GB |
| **🎮 GPU** | 未配置 | 如需 GPU 微调需另行配置 |
| **🐍 Python** | 3.10.18 | 系统默认 Python 版本 |

#### ☁️ 云端环境支持
- **Google Colab**：免费GPU资源，适合学习和小规模实验

### 🚀 一键安装脚本

#### 📋 快速安装 (推荐)
```bash
# 克隆项目代码
# 1. 初始化 LFS
git lfs install
# 2. 克隆仓库 (LFS 文件将自动下载)
git clone https://github.com/FlyAIBox/AIAgent101.git
# 3.切换到新克隆的仓库目录
cd AIAgent101
# 4.手动拉取所有 LFS 管理的大文件
git lfs pull


# 一键安装脚本(Ubuntu 22.04)
chmod +x 00-agent-env/setup_agent101_dev.sh
./00-agent-env/setup_agent101_dev.sh
```

#### 🔧 安装脚本功能

**`setup_agent101_dev.sh` 自动完成以下配置：**

| 安装模块 | 具体内容 | 配置说明 |
|---------|----------|----------|
| **🔄 系统更新** | 更新包管理器，安装基础依赖 | curl, wget, git, build-essential |
| **🎮 GPU驱动** | 自动检测并安装NVIDIA驱动 | 支持nvidia-smi检测 |
| **🔥 CUDA环境** | 安装CUDA 12.1工具包 | 配置环境变量和符号链接 |
| **🐍 Python环境** | 安装Python 3.10.18 | 包含dev包和虚拟环境支持 |
| **🐍 Conda管理** | 安装Miniconda环境 | 创建agent101虚拟环境 |
| **📓 Jupyter Lab** | 配置交互式开发环境 | 支持远程访问和密码认证 |
| **🔧 开发工具** | Git配置和环境变量设置 | 用户信息配置和API密钥模板 |

### 🔐 环境变量配置

#### 📝 创建环境配置文件
```bash
# 复制环境变量模板
cp env.template .env

# 编辑配置文件
nano .env
```

#### 🔑 必需的API密钥

**`.env` 文件配置示例：**
```bash
# =========================
# 🤖 大语言模型API配置
# =========================
# OpenAI API (GPT-4, GPT-3.5)
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# DeepSeek API (推荐用于中文场景)  
DEEPSEEK_API_KEY=sk-your-deepseek-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# =========================
# 🛠️ 工具集成API配置
# =========================
# 和风天气API (MCP天气工具)
QWEATHER_API_KEY=your-qweather-api-key
QWEATHER_API_BASE=https://devapi.qweather.com

# Tavily搜索API (LangGraph搜索工具)
TAVILY_API_KEY=tvly-your-tavily-api-key

# =========================
# 📊 监控评估平台配置
# =========================
# LangSmith (LangChain监控)
LANGSMITH_API_KEY=your-langsmith-api-key
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT=aiagent101

# Langfuse (智能体评估)
LANGFUSE_PUBLIC_KEY=pk-your-langfuse-public-key
LANGFUSE_SECRET_KEY=sk-your-langfuse-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 🚀 快速开始

### ⚡ 5分钟快速体验

#### 🎯 第一步：运行第一个AI应用
```bash
# 激活虚拟环境
conda activate agent101

# 配置API密钥 (使用你的实际密钥)
export OPENAI_API_KEY="sk-your-openai-api-key"

# 运行第一个应用
python 00-agent-env/first_llm_app.py
```

**🎉 预期输出：**
```
🤖 AI助手：你好！我是你的AI旅行规划助手。
请告诉我你想去哪里旅行？

👤 用户输入：我想去北京玩3天
🤖 AI助手：为你推荐北京3日游行程...
第一天：天安门广场 → 故宫博物院 → 王府井
第二天：长城一日游 → 鸟巢水立方夜景
第三天：颐和园 → 圆明园 → 南锣鼓巷
```

#### 🌟 第二步：体验多角色智能体
```bash
# 进入多角色智能体目录
cd 03-agent-multi-role/langgraph

# 启动可视化调试工具
langgraph dev

# 访问 https://smith.langchain.com/studio 进行可视化调试
```

#### 🔧 第三步：集成MCP工具
```bash
# 进入MCP演示目录  
cd 02-agent-llm-mcp/mcp-demo

# 启动天气服务器
python server/weather_server.py &

# 运行集成客户端
python client/mcp_client_deepseek.py

# 测试天气查询功能
# 输入：今天北京天气怎么样？
```


### 🎯 学习目标检查清单

#### ✅ 基础技能掌握
- [ ] 能够配置完整的AI开发环境
- [ ] 掌握提示词工程的核心技巧
- [ ] 理解大语言模型的基本原理
- [ ] 能够部署本地推理服务
- [ ] 熟悉MCP协议和工具集成

#### ✅ 进阶技能掌握  
- [ ] 能够设计多角色智能体系统
- [ ] 掌握LangChain和LangGraph框架
- [ ] 能够进行模型微调和优化
- [ ] 建立完整的评估监控体系
- [ ] 熟悉工作流自动化工具
---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

### 📋 使用权限
- ✅ 个人学习和研究使用
- ✅ 企业内部使用和二次开发  
- ✅ 开源项目集成和引用
- ✅ 商业项目使用（保留版权声明）

### ⚠️ 免责声明
- 项目仅供学习和研究使用
- 生产环境使用请充分测试
- API密钥和数据安全请自行保障
- 对使用本项目造成的损失不承担责任

---

## 📞 获取帮助

- 🐛 **Bug报告**: [GitHub Issues](https://github.com/FlyAIBox/AIAgent101/issues)
- 💬 **技术讨论**: [GitHub Discussions](https://github.com/FlyAIBox/AIAgent101/discussions)
- 📧 **邮件联系**: fly910905@sina.com
- 🔗 **微信公众号**: 萤火AI百宝箱

## 🙏 致谢

本项目使用了以下开源项目：

<table>
<tr>
<td align="center">
<img src="https://pytorch.org/assets/images/logo-dark.svg" width="60">
<br>PyTorch
</td>


<td align="center">
<img src="https://raw.githubusercontent.com/vllm-project/vllm/main/docs/assets/logos/vllm-logo-text-light.png" width="60">
<br>Vllm
</td>

<td align="center">
<img src="https://raw.githubusercontent.com/langchain-ai/.github/main/profile/logo-dark.svg#gh-light-mode-only" width="70">
<br>Langchain
</td>


<td align="center">
<img src="https://raw.githubusercontent.com/hiyouga/LLaMA-Factory/main/assets/logo.png" width="60">
<br>LLaMA Factory
</td>
</tr>
</table>

特别感谢所有贡献者和社区成员的支持！

---

<div align="center">


**⭐ 如果这个项目对你有帮助，请给个Star支持！⭐**

<a href="https://star-history.com/#FlyAIBox/AIAgent101&Date">

  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=FlyAIBox/AIAgent101&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=FlyAIBox/AIAgent101&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=FlyAIBox/AIAgent101&type=Date" />
  </picture>

</a>

**🔗 更多访问：[大模型实战101](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzkzODUxMTY1Mg==&action=getalbum&album_id=3945699220593803270#wechat_redirect)**

</div>
