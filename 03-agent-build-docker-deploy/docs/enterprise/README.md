# 旅小智 AI 旅行规划智能体 - 企业级文档中心

## 📋 文档概述

本目录包含 **旅小智 AI 旅行规划智能体** 的完整企业级文档，涵盖需求分析、系统设计、数据模型、业务流程、部署运维等各个方面。这些文档遵循企业软件工程优秀做法，适用于需求评审、技术设计、开发实施、测试验收、生产部署等全生命周期。

## 🎯 系统特性

### 核心能力
- 🤖 **多智能体协作**：6个专业AI智能体协同工作
- 💬 **双模式交互**：支持传统表单和自然语言对话两种输入方式
- ⚡ **实时数据集成**：DuckDuckGo搜索 + MCP天气服务器
- 🎯 **个性化规划**：基于预算、兴趣、时间等多维度定制
- 📊 **可观测性**：完整的日志、监控和状态追踪
- 🐳 **容器化部署**：Docker Compose 一键部署

### 技术架构
- **前端**：Streamlit（Python Web框架）
- **后端**：FastAPI（异步API服务）
- **AI引擎**：LangGraph + OpenAI兼容LLM
- **工具集成**：DuckDuckGo搜索、MCP天气服务器
- **部署**：Docker + Docker Compose

## 📚 文档导航

### 🔍 第一步：了解项目（必读）

#### [00. 更新摘要](./00_UPDATES_SUMMARY.md) ⭐ NEW
**最新更新**：2025年11月17日  
**内容**：v2.0.0 自然语言交互版本更新说明
- 新增 `/chat` 接口：AI驱动的意图理解
- 双模式交互：对话式 + 表单式
- 完整的功能变更、技术亮点和扩展方向

#### [01. 需求调研报告](./01_discovery_research.md)
**目标读者**：产品经理、业务负责人、项目管理者  
**内容**：
- 项目背景与业务驱动
- 竞品分析与市场定位
- 业务目标与成功指标
- 用户画像与使用场景
- 技术可行性评估

**关键要点**：
- 为什么要做这个系统？
- 解决什么业务痛点？
- 与竞品的差异化在哪里？

---

### 📋 第二步：需求与设计（核心文档）

#### [02. 需求规格说明书](./02_requirements_spec.md) ⭐ UPDATED
**目标读者**：产品经理、开发工程师、测试工程师  
**内容**：
- 功能需求清单（FR-01 ~ FR-08）
  - **FR-08**：自然语言交互功能（新增）
- 非功能需求（性能、可用性、安全性）
- 集成需求（外部API、环境变量）
- 需求追踪矩阵

**关键要点**：
- 系统需要实现哪些功能？
- 性能、安全等指标是什么？
- 如何验证需求是否满足？

#### [03. 系统设计文档](./03_system_design.md) ⭐ UPDATED
**目标读者**：架构师、开发工程师  
**内容**：
- 总体架构图（前端、后端、智能体、工具、存储）
- 模块视图与职责划分
- 序列图（表单模式 + 自然语言模式）
- 错误与回退策略
- 扩展点与技术演进

**关键要点**：
- 系统的整体架构是什么？
- 各模块如何协作？
- 如何处理异常和降级？
- 未来如何扩展？

#### [04. 数据设计文档](./04_data_design.md) ⭐ UPDATED
**目标读者**：数据架构师、开发工程师  
**内容**：
- 核心数据实体（Weather、Attraction、Hotel、DayPlan、TripSummary）
- **新增**：ChatRequest、ChatResponse（自然语言交互模型）
- 关系模型与ER图
- 数据流设计（表单模式 + 自然语言模式）
- 存储策略与扩展建议

**关键要点**：
- 系统涉及哪些数据实体？
- 数据如何流转？
- 如何持久化与查询？

---

### 🔄 第三步：业务流程与集成

#### [05. 关键业务流程文档](./05_business_processes.md) ⭐ UPDATED
**目标读者**：业务分析师、运营人员、开发工程师  
**内容**：
- 端到端业务流程（表单模式 + 自然语言模式）
- LangGraph节点执行流程
- 任务状态生命周期
- 外部数据服务调用
- 运维与异常处理
- SLA与告警建议

**关键要点**：
- 用户如何使用系统？
- 系统内部如何运作？
- 如何监控和运维？

#### [07. 前端API调用说明](./07_frontend_api_calls.md) ⭐ UPDATED
**目标读者**：前端开发、测试工程师、运维人员  
**内容**：
- 接口列表与调用关系
  - `GET /health`：健康检查
  - `POST /plan`：表单模式创建任务
  - **`POST /chat`**：自然语言模式创建任务（新增）
  - `GET /status/{task_id}`：查询任务状态
  - `GET /download/{task_id}`：下载结果
- 调用流程与序列图
- 接口详细说明（请求/响应格式、超时策略、错误处理）
- 监控与日志建议

**关键要点**：
- 前端如何调用后端接口？
- 接口的输入输出格式是什么？
- 如何处理异常情况？

---

### 🚀 第四步：部署与运维

#### [06. 部署与运维指南](./06_deployment_and_operations.md)
**目标读者**：DevOps工程师、运维人员  
**内容**：
- Docker容器化部署
- Docker Compose编排
- 环境变量配置
- 健康检查与监控
- 日志管理
- 常见问题排查
- 扩缩容策略

**关键要点**：
- 如何部署系统？
- 如何监控系统运行状态？
- 遇到问题如何排查？

---

## 🆕 版本更新历史

### v2.0.0 - 自然语言交互版本（2025-11-17）

#### 重大更新
- ✨ **新增自然语言交互功能**
  - 用户可用对话方式描述旅行需求
  - AI自动提取关键信息并创建任务
  - 支持信息不足时的智能引导
  
- 🔧 **技术实现**
  - 新增 `POST /chat` 接口
  - 集成 LLM 进行意图理解
  - 新增 `ChatRequest`/`ChatResponse` 数据模型
  
- 📖 **文档更新**
  - 所有企业级文档已全面更新
  - 新增"更新摘要"文档
  - 补充自然语言交互的设计与流程

#### 详细更新内容
详见：[00_UPDATES_SUMMARY.md](./00_UPDATES_SUMMARY.md)

### v1.0.0 - 初始版本

- 🎯 多智能体旅行规划系统
- 📝 表单式输入
- 🔍 DuckDuckGo搜索集成
- 🌤️ MCP天气服务集成
- 🐳 Docker容器化部署

---

## 📊 文档使用指南

### 按角色推荐阅读

#### 产品经理 / 业务负责人
1. 📄 [01. 需求调研报告](./01_discovery_research.md) - 了解项目背景
2. 📄 [02. 需求规格说明书](./02_requirements_spec.md) - 掌握功能需求
3. 📄 [05. 关键业务流程](./05_business_processes.md) - 理解业务流程

#### 系统架构师
1. 📄 [03. 系统设计文档](./03_system_design.md) - 架构设计
2. 📄 [04. 数据设计文档](./04_data_design.md) - 数据模型
3. 📄 [06. 部署与运维指南](./06_deployment_and_operations.md) - 部署策略

#### 开发工程师
1. 📄 [02. 需求规格说明书](./02_requirements_spec.md) - 功能需求
2. 📄 [03. 系统设计文档](./03_system_design.md) - 技术设计
3. 📄 [04. 数据设计文档](./04_data_design.md) - 数据模型
4. 📄 [07. 前端API调用说明](./07_frontend_api_calls.md) - 接口规范

#### 测试工程师
1. 📄 [02. 需求规格说明书](./02_requirements_spec.md) - 测试用例来源
2. 📄 [05. 关键业务流程](./05_business_processes.md) - 测试场景
3. 📄 [07. 前端API调用说明](./07_frontend_api_calls.md) - 接口测试

#### DevOps / 运维工程师
1. 📄 [06. 部署与运维指南](./06_deployment_and_operations.md) - 部署运维
2. 📄 [03. 系统设计文档](./03_system_design.md) - 架构理解
3. 📄 [05. 关键业务流程](./05_business_processes.md) - 监控指标

---

## 🎓 快速开始

### 新人入职推荐路径

#### 第1天：了解项目
- 阅读 [00_UPDATES_SUMMARY.md](./00_UPDATES_SUMMARY.md) - 快速了解最新功能
- 阅读 [01_discovery_research.md](./01_discovery_research.md) - 理解项目背景
- 阅读项目根目录的 [README.md](../../README.md) - 运行Demo

#### 第2-3天：掌握需求与设计
- 详细阅读 [02_requirements_spec.md](./02_requirements_spec.md)
- 详细阅读 [03_system_design.md](./03_system_design.md)
- 结合代码理解架构

#### 第4-5天：深入技术细节
- 阅读 [04_data_design.md](./04_data_design.md)
- 阅读 [05_business_processes.md](./05_business_processes.md)
- 阅读 [07_frontend_api_calls.md](./07_frontend_api_calls.md)

#### 第1周末：实践部署
- 阅读 [06_deployment_and_operations.md](./06_deployment_and_operations.md)
- 自己部署一遍系统
- 尝试修改和扩展

---

## 🔧 文档维护规范

### 更新原则
1. **及时性**：代码功能变更后，24小时内更新相关文档
2. **一致性**：确保文档与代码实现保持一致
3. **完整性**：每次更新需同步相关的所有文档
4. **可追溯**：在更新摘要中记录重要变更

### 更新流程
1. 代码功能开发完成
2. 更新相关技术文档（02-07）
3. 更新 00_UPDATES_SUMMARY.md
4. 更新本 README.md 的版本历史
5. 提交 Pull Request，注明文档变更

### 文档规范
- 使用 Markdown 格式
- 包含 Mermaid 图表（架构图、流程图、序列图）
- 代码示例使用语法高亮
- 中英文混排遵循 [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)

---

## 📞 联系方式

### 文档反馈
如果您在使用文档过程中发现任何问题，欢迎反馈：
- 📧 提交 Issue：描述问题和改进建议
- 💬 内部讨论：团队技术讨论群
- 📝 Pull Request：直接提交文档修改

### 技术支持
- 📚 开发文档：`backend/` 和 `frontend/` 目录下的代码注释
- 🎯 API文档：启动后端后访问 `http://localhost:8080/docs`
- 🔍 问题排查：参考 [06_deployment_and_operations.md](./06_deployment_and_operations.md)

---

## 📝 附录

### 相关资源
- 🏠 [项目主README](../../README.md)
- 📊 [架构图集](../img/)
- 🔧 [配置示例](../../backend/env.example)
- 🐳 [Docker配置](../../docker-compose.yml)

### 技术栈文档
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://docs.streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Docker](https://docs.docker.com/)

### 外部服务文档
- [DuckDuckGo Search API](https://duckduckgo.com/api)
- [QWeather API](https://dev.qweather.com/)
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)

---

<div align="center">

**旅小智 AI 旅行规划智能体**  
_让旅行规划变得更简单、更智能_

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](./00_UPDATES_SUMMARY.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../LICENSE)
[![Documentation](https://img.shields.io/badge/docs-enterprise-orange.svg)](./README.md)

</div>

