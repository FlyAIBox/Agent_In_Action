按照这个课程大纲，整理详细的讲稿

## AI旅行Agent：端到端项目构建与生产环境容器化部署

| 节标题                                    | 教学环节           | 教学形式              | 预估 时长 （分） | 实际 时长 （分） | 学习目标+教学方法（备注）                                    |
| ----------------------------------------- | ------------------ | --------------------- | ---------------- | ---------------- | ------------------------------------------------------------ |
| 本章导览：端到端智能体项目全景认知        | 项目总览与学习路线 | 讲授+互动问答         | 20               |                  | 【教学方法】基于项目架构图和文档进行逐层解读，引导学员理解端到端开发思路。【学习目标】掌握AI旅行规划智能体的业务背景、技术选型、架构设计与学习路径，为后续深入学习建立全局认知框架。 |
| 需求分析与架构设计：多智能体协作蓝图规划  | 需求拆解与架构设计 | 案例分析+架构绘制     | 35               |                  | 【教学方法】通过旅行规划场景分析，引导学员理解多智能体分工的必要性，绘制系统架构图。【学习目标】掌握复杂AI应用的需求分析方法、多智能体架构设计原理、前后端分离架构及技术栈选型的决策思路。 |
| 开发环境与配置管理：生产级项目初始化      | 环境配置与依赖管理 | 讲授+实操演示         | 30               |                  | 【教学方法】演示环境变量配置、依赖安装、API密钥管理的完整流程，强调生产环境配置的最佳实践。【学习目标】掌握OpenAI兼容接口配置、和风天气API、高德地图API等第三方服务接入，理解环境隔离和密钥安全管理。 |
| LangGraph配置与模型接入：智能体引擎配置   | 核心配置解析       | 代码走读+参数调优     | 25               |                  | 【教学方法】逐行解析LangGraph配置类，对比不同模型参数的影响，演示OpenAI兼容接口的灵活性。【学习目标】理解ChatOpenAI模型配置要点、温度和token参数调优原理、DuckDuckGo搜索引擎配置及国内外API兼容性处理。 |
| 应用级配置与常量管理：系统参数化设计      | 全局配置讲解       | 讲授+最佳实践         | 20               |                  | 【教学方法】解析应用配置类的设计模式，说明配置参数化对系统可维护性的价值。【学习目标】掌握应用级配置的组织方式、默认值设置策略、系统限制参数设计及配置集中管理的工程实践。 |
| 外部API集成与容错设计：第三方服务接入策略 | API集成与异常处理  | 案例分析+代码实现     | 40               |                  | 【教学方法】逐个解析和风天气、高德地图、汇率API的集成代码，重点讲解异常处理和降级策略。【学习目标】掌握第三方API的标准接入模式、错误处理和超时机制、API配额管理及服务降级的工程实现方案。 |
| DuckDuckGo搜索工具集：实时信息获取引擎    | 工具设计与实现     | 代码走读+工具测试     | 45               |                  | 【教学方法】逐个解析7个搜索工具的实现逻辑，演示@tool装饰器的使用，测试搜索效果。【学习目标】掌握LangChain工具系统设计、DuckDuckGo搜索API使用、异步工具实现、搜索结果格式化及工具组合使用策略。 |
| 多智能体状态设计：协作通信的数据基础      | 状态管理架构       | 数据结构分析+状态流转 | 30               |                  | 【教学方法】解析TravelPlanState数据结构，绘制状态流转图，说明智能体间通信机制。【学习目标】理解LangGraph状态管理机制、TypedDict类型安全设计、消息历史管理及多智能体协作的数据传递模式。 |
| 协调员智能体：多智能体工作流编排核心      | 中央控制器设计     | 核心逻辑剖析+决策算法 | 40               |                  | 【教学方法】深入解析协调员智能体的路由逻辑，分析决策树和状态管理，演示工作流控制。【学习目标】掌握多智能体系统的中央编排模式、智能路由决策算法、工作流状态控制及任务分发与结果整合机制。 |
| 专业智能体实现：领域专家能力构建          | 智能体角色设计     | 角色建模+能力定义     | 50               |                  | 【教学方法】逐个分析旅行顾问、天气分析师、预算优化师、当地专家、行程规划师的实现，对比不同角色的prompt设计和MCP工具设计。【学习目标】理解专业智能体的角色建模方法、领域知识注入技巧、提示词工程在多智能体中的应用及智能体间协作的实现模式。 |
| LangGraph工作流构建：状态图与路由系统     | 工作流引擎实现     | 流程图绘制+路由分析   | 45               |                  | 【教学方法】解析StateGraph构建过程，绘制节点关系图，分析条件路由的实现逻辑。【学习目标】掌握LangGraph StateGraph的构建方法、节点与边的定义方式、条件路由实现原理及复杂工作流的设计与调试技巧。 |
| 工具执行与智能路由：动态决策引擎          | 工具调度系统       | 调度逻辑+智能匹配     | 35               |                  | 【教学方法】解析工具执行节点的实现，分析智能工具选择算法，演示异步工具调用。【学习目标】理解工具执行节点的调度机制、智能工具匹配算法、异步执行模式及工具调用的错误处理与回退策略。 |
| FastAPI后端服务：异步任务管理与API设计    | 后端服务架构       | API设计+异步处理      | 50               |                  | 【教学方法】解析FastAPI应用结构，分析异步任务处理机制，演示API接口设计和错误处理。【学习目标】掌握FastAPI异步API设计、后台任务处理模式、任务状态管理、超时与降级机制及RESTful API的最佳实践。 |
| 任务状态持久化：生产级状态管理            | 状态管理机制       | 持久化设计+状态恢复   | 25               |                  | 【教学方法】分析任务状态的持久化方案，演示JSON文件存储和内存缓存的结合使用。【学习目标】理解任务状态持久化的必要性、JSON文件存储的优缺点、内存缓存策略及系统重启后的状态恢复机制。 |
| Streamlit前端界面：用户交互体验设计       | 前端界面构建       | 界面设计+交互实现     | 45               |                  | 【教学方法】解析Streamlit组件使用，分析表单设计和状态管理，演示实时进度显示和结果展示。【学习目标】掌握Streamlit Web应用开发、响应式表单设计、实时状态监控、结果可视化展示及用户体验优化技巧。 |
| Docker容器化构建：镜像制作与优化          | 容器化实现         | 镜像构建+优化策略     | 35               |                  | 【教学方法】解析前后端Dockerfile的编写，分析多阶段构建和镜像优化策略，演示构建过程。【学习目标】掌握Python应用容器化的标准流程、Dockerfile最佳实践、镜像层优化技巧及容器安全配置方法。 |
| Docker Compose编排：多服务协同部署        | 服务编排实践       | 编排文件+服务通信     | 30               |                  | 【教学方法】解析docker-compose.yml配置，分析服务间网络通信，演示完整部署流程。【学习目标】理解Docker Compose多服务编排原理、容器间网络配置、数据卷管理、健康检查配置及生产环境部署注意事项。 |
| 启动脚本与自动化：部署流程标准化          | 自动化部署         | 脚本分析+自动化流程   | 25               |                  | 【教学方法】解析启动脚本的实现逻辑，分析自动化部署流程，演示一键启动效果。【学习目标】掌握Shell脚本在项目部署中的应用、环境检查和服务启动的自动化、错误处理和日志管理及CI/CD集成的基础知识。 |
| 系统监控与日志管理：生产环境运维实践      | 运维监控体系       | 日志分析+监控实现     | 30               |                  | 【教学方法】分析日志配置和监控实现，演示健康检查和错误追踪，讲解运维最佳实践。【学习目标】理解生产环境日志管理策略、系统健康监控方法、错误追踪和报警机制及运维自动化的基本实现。 |
| 故障排除与性能优化：问题诊断与解决        | 故障处理与优化     | 问题分析+解决方案     | 35               |                  | 【教学方法】分析常见问题和解决方案，演示性能瓶颈识别和优化方法，提供故障排除清单。【学习目标】掌握多智能体系统的常见故障类型、问题诊断方法、性能优化策略及系统可用性提升的工程实践。 |
| 本章总结：智能体开发实战经验沉淀          | 知识总结与扩展     | 经验总结+未来规划     | 25               |                  | 【教学方法】组织学员总结关键收获，梳理实践难点，讨论技术扩展方向和商业化可能性。【学习目标】形成端到端AI智能体开发的完整知识体系，掌握从需求分析到生产部署的全流程能力，建立持续学习和项目扩展的思路。 |



以“AI 旅行规划 Agent”项目为主线，覆盖课程大纲的 13 个章节。每节包含教学准备、讲解结构、示例/演示要点、互动与练习提示，以及推荐的代码/文档定位。您可以直接按此流程带着学员逐步完成端到端智能体实战。

------

### 1. Agent导览：认知端到端旅行规划项目蓝图

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/README.md`，配合投影展示。
**讲解结构**

1. 项目定位开场（5 分钟）
   - 介绍本章是“零基础实战 Agent”系列的综合项目，通过“AI 旅行规划 Agent”来串联前期的提示词工程、上下文工程、工具调用、LangGraph 实战。
   - 引导学员阅读 README 开头的介绍部分，熟悉项目目标：生成个性化旅行计划，并具备生产级部署流程。
2. 功能与产出概览（5 分钟）
   - 逐条浏览 README 的“系统功能”、“AI 智能体团队”、“使用说明”章节，强调最终成果包括：
     - 多智能体协同生成旅行行程。
     - 前端 Streamlit 可视化。
     - Docker 化部署流程。
3. 课程路线图说明（5 分钟）
   - 展示课程大纲表格，说明每节课的主题、学习目标和参考代码路径。
   - 强调学习方式：讲解原理 → 对照代码 → 现场演示 → 布置练习 → 提炼经验。

**互动提示**

- 提问：“你最期待 AI 旅行 Agent 解决哪些问题？”
- 邀请学员分享前序章节中印象最深刻的内容，为综合实战建立期待。

------

### 2. Agent技术栈透视：LangChain×LangGraph×Tavily 协同

**教学准备**：打开 03-agent-multi-role/langgraph/0-docs/ 下的架构资料（PDF），提前打印或投影展示。
**讲解结构**

1. 整体架构拆解（10 分钟）
   - 从架构图的顶层开始，逐层讲解用户界面、API 服务、智能体编排、外部工具和数据源、容器化部署。
   - 用颜色或标注突出 LangChain 工具、LangGraph 状态流、搜索服务（如 Tavily）与外部 API（天气、地图、汇率等）。
2. 数据流与调用链（10 分钟）
   - 引导学员跟着箭头了解：前端上送表单 → FastAPI 接收并创建任务 → 调用 LangGraph 智能体 → 各模块/工具协作生成旅行计划 → 结果返回并展示。
   - 让学员在纸上画出简化流程图，加强记忆。
3. 技术选择背后原因（5 分钟）
   - 说明为何选择 LangGraph（易于构建状态流和条件路由）、LangChain（工具与 LLM 集成）、Tavily（简单易用的搜索服务，已在本目录依赖中提供）等。
   - 强调国内可访问 API（和风天气、AMap、exchangerate.host）在实战中的重要性（对应代码在仓库根 04-agent-build-docker-deploy/ 中）。

**互动提示**

- 让学员尝试描述“一次规划请求在系统中经历的步骤”。
- 留出 2 分钟讨论问题：如果需要新增服务（如航班信息），该放在哪一层？

------

### 3. Agent运行底座：环境变量与配置管理实操

**教学准备**：确保已克隆项目。使用终端命令准备演示。
**讲解结构**

1. 依赖与初始化脚本（10 分钟）

   - 本目录（03-agent-multi-role/langgraph）本地入门：
     - 安装依赖：`pip install -r 03-agent-multi-role/langgraph/requirements.txt`
     - 运行 Notebook：`jupyter notebook` 并打开 `03-agent-multi-role/langgraph/1-Base/01-simple-graph.ipynb`
   - 后端与前端（仓库根 04-agent-build-docker-deploy/）：
     - 讲解 `04-agent-build-docker-deploy/backend/requirements.txt` 与 `04-agent-build-docker-deploy/frontend/requirements.txt` 的关键包（LangGraph、LangChain、ChatOpenAI、Streamlit、FastAPI 等）。
     - 演示 `setup_environment.sh`：安装依赖、复制 `.env` 模板、创建 `results/`。解释脚本中每一步的意义。

2. 环境变量详解（10 分钟）

   - 在仓库根 `04-agent-build-docker-deploy/` 中使用 `.env` 管理变量，示例：
     - `OPENAI_API_KEY`/`OPENAI_BASE_URL`/`OPENAI_MODEL`
     - `QWEATHER_*`、`AMAP_*`、`EXCHANGE_RATE_*`
   - 说明使用 `.env` 的原因以及安全注意事项。

3. 动手配置（10 分钟）

   - 现场示范：在 `04-agent-build-docker-deploy/` 复制 `.env`，填入测试密钥（可用占位符），运行脚本，确认没有报错。
   - 提醒学员检查依赖安装结果、`.env` 是否正确加载。

**互动练习**

- 学员在指导下完成 .env 配置并运行脚本。
- 老师巡回解答常见配置错误（如缺少 Python 版本、网络超时等）。

------

### 4. Agent语言大脑：LangGraphConfig 与 ChatOpenAI 接入

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/config/langgraph_config.py`、`04-agent-build-docker-deploy/backend/agents/langgraph_agents.py`、`04-agent-build-docker-deploy/backend/agents/simple_travel_agent.py`。
**讲解结构**

1. 配置类结构解析（10 分钟）
   - 讲解 LangGraphConfig 类：加载环境变量、设置 LLM 参数、DuckDuckGo 搜索配置、模型生成参数。
   - 说明 get_llm_config()、get_search_config() 返回的字典如何被其他模块使用。
2. 环境校验机制（5 分钟）
   - 阅读 validate_config()，解释导入时检查 OPENAI_API_KEY 的逻辑及提示信息。
   - 强调在缺少关键配置时及早失败的好处。
3. LLM 初始化场景（10 分钟）
   - 在 langgraph_agents.py 和 simple_travel_agent.py 中寻找 ChatOpenAI(**llm_config)，讲解如何复用配置。
   - 指出 temperature, max_tokens, top_p 的意义，讨论实际调优策略。

**互动提示**

- 问学员如何更换模型（例如改用 deepseek-chat），需要修改哪些配置。
- 布置课后练习：将温度调高/调低，观察生成行程的差异。

------

### 5. Agent基础设定：AppConfig 与业务常量管理

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/config/app_config.py`，同时准备 `04-agent-build-docker-deploy/backend/modules` 中引用它的文件。
**讲解结构**

1. 常量与默认值（10 分钟）
   - 逐条说明默认货币、预算范围、行程天数限制、团队人数限制、缓存设置、展示设置、成本估算参数等。
   - 强调这些常量如何保证系统在没有特殊配置时能够提供合理体验。
2. AppConfig 包装（5 分钟）
   - 解释为何使用类封装常量（便于导入与 IDE 自动提示）。
3. 实际引用场景（10 分钟）
   - 在 modules/attraction_finder.py, modules/hotel_estimator.py, modules/itinerary_planner.py, api_server.py 等文件中查找 app_config 的使用，说明参数的影响。

**互动提示**

- 让学员尝试修改 DEFAULT_TRIP_DURATION 或 MAX_ATTRACTIONS，并预测对结果的影响。
- 讨论如何根据不同客户群体（预算/行程长短）自定义常量。

------

### 6. Agent服务联通：外部数据源 API 接入策略

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/config/api_config.py` 和各业务模块文件。
**讲解结构**

1. 配置载入与状态检测（5 分钟）
   - 讲解 api_config.py 如何读取环境变量、暴露 api_config 实例、提供 get_api_status()。
2. 和风天气接入（10 分钟）
   - 逐段讲解 modules/weather_service.py 的 _resolve_location, get_current_weather, get_weather_forecast。
   - 强调请求头的密钥、超时处理、异常回退。
3. 高德地图接入（10 分钟）
   - 分析 modules/attraction_finder.py：请求参数、类型编码、评分/费用解析、模拟数据备选。
   - 同样讲解 modules/hotel_estimator.py 的酒店搜索、价格推算。
4. 汇率服务接入（10 分钟）
   - 阅读 modules/currency_converter.py：缓存机制、接口兼容处理（rates vs conversion_rates）、回退汇率与格式化。

**互动提示**

- 让学员在课堂上找出每个 API 调用的认证方式及失败日志输出。
- 提问：如果某个 API 返回错误，系统有什么退路？（模拟数据/回退汇率）。

------

### 7. Agent大脑建模：LangGraph 多智能体编排

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/agents/langgraph_agents.py`，并可对照 `03-agent-multi-role/langgraph/4-BuildYourAssiant/*.ipynb` 的并行与子图示例，准备投影或绘制状态图。
**讲解结构**

1. TravelPlanState 分析（10 分钟）
   - 详细讲解每个字段用途：messages（对话历史）、agent_outputs（各专家结果）、final_plan、iteration_count 等。
   - 强调添加字段时需在 state 类型、初始值、流程中保持一致。
2. 图结构构建（15 分钟）
   - 讲解 StateGraph(TravelPlanState)、add_node、set_entry_point；
   - 逐个介绍节点函数（旅行顾问、天气分析师、预算优化师等）及返回的状态变化；
   - 解释 add_conditional_edges 中路由逻辑。
3. 工具节点与外部调用（10 分钟）
   - _tool_executor_node 如何调用 travel_tools.ALL_TOOLS；
   - 说明工具返回结果如何通过状态传递给下一个 Agent。

**互动提示**

- 引导学员在白板上画出整个状态机：协调员、各专家、工具节点、END。
- 思考题：如要加入“安全提醒”节点，需要修改哪些函数？

------

### 8. Agent分身体系：传统多智能体与角色能力库

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/agents/multi_agent_orchestrator.py`、`04-agent-build-docker-deploy/backend/agents/travel_agents.py`。
**讲解结构**

1. 基础设施说明（10 分钟）
   - 介绍消息类型 MessageType、实体 Message、通信中心 AgentCommunicationHub。
   - 分析 BaseAgent 的设计，为角色扩展提供统一接口。
2. 角色功能解析（10 分钟）
   - 逐个讲解旅行顾问、预算优化师、天气分析师、当地专家、行程规划师、协调员如何处理消息和生成响应。
   - 对比 LangGraph 节点与这些角色的职责一致性。
3. 决策引擎与 orchestrator（10 分钟）
   - 讲解 MultiAgentTravelOrchestrator 五阶段流程：准备上下文、协调规划、并行咨询、协作决策、生成输出。
   - 比较与 LangGraph 编排的差异：传统方式通过消息队列和决策规则，灵活但管理复杂；LangGraph 通过状态图更直观。

**互动提示**

- 问学员：如果没有 LangGraph，传统 orchestrator 如何处理冲突的建议？
- 鼓励学员思考如何在实际项目中选择合适的编排方式。

------

### 9. Agent业务骨架：功能模块与工具库串讲

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/modules` 各文件、`04-agent-build-docker-deploy/backend/tools/travel_tools.py`、`04-agent-build-docker-deploy/backend/utils/helpers.py`。
**讲解结构**

1. 模块概览（5 分钟）
   - 介绍这些模块如何构成旅行规划的业务层：需求处理、景点/酒店推荐、天气查询、预算计算、行程编排、总结输出等。
2. 深入解析（20 分钟）
   - 选取几个模块做详细分析：
     - itinerary_planner.py: 分配景点/餐厅/活动到每日日程、根据天气调整安排、估算交通与费用。
     - trip_summary.py: 生成总结文本、保存文件 JSON。
     - expense_calculator.py: 计算总预算、应急基金、税费。
   - 说明这些模块如何彼此协同。
3. 工具集成（10 分钟）
   - 讲解 `travel_tools.py` 中的搜索工具函数（如目的地信息、天气信息等），强调 LangChain 的 `@tool` 装饰器和 `ALL_TOOLS` 列表。
   - 辅助工具函数（`utils/helpers.py`）如何在多处复用（货币格式化、文本截断等）。

**互动提示**

- 布置练习：让学员在 itinerary_planner.py 中找到决定上午/下午/晚上活动安排的逻辑。
- 提问：如果要新增“当地购物推荐”，应该添加在哪个模块？

------

### 10. Agent服务层：FastAPI 调度与任务管理

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/api_server.py`，准备流程图工具。
**讲解结构**

1. 应用初始化（5 分钟）
   - app = FastAPI(...)、CORS 设置、全局 planning_tasks 字典、持久化文件 tasks_state.json。
2. API 路由（10 分钟）
   - /: 返回系统信息；
   - /health: 校验 OPENAI_API_KEY、统计系统资源；
   - /planning: 任务创建、状态查询、结果返回，了解 Pydantic 模型 TravelRequest, PlanningResponse, PlanningStatus。
3. 任务执行流程（15 分钟）
   - 分析 run_planning_task: 任务状态更新 → 构造 langgraph_request → 调用 LangGraph 智能体 → 更新进度日志 → 保存结果。
   - 强调异步执行 (asyncio.sleep 模拟阶段) 与状态持久化的设计。

**互动提示**

- 让学员画出任务状态从 pending -> processing -> completed/failed 的流程。
- 讨论：如果任务执行时间很长，如何调整轮询策略或提供用户提示？

------

### 11. Agent界面体验：Streamlit 前端与联调技巧

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/frontend/streamlit_app.py`，准备终端运行 Streamlit。
**讲解结构**

1. 界面布局（10 分钟）
   - 展示标题、简介、智能体团队介绍、表单字段（目的地、日期、预算、兴趣等）。
   - 提醒学员注意表单默认值与校验。
2. 交互流程（10 分钟）
   - submit 后如何调用后端 /planning 创建任务并记录 task_id；
   - poll_planning_status 如何循环查询结果、展示进度条、处理超时。
3. 结果展示与错误处理（5 分钟）
   - 行程计划、智能体输出、预算详情如何展示；
   - 如果后端返回错误，如何通过 st.error 提示用户。

**互动提示**

- 现场演示一次完整交互。
- 布置练习：修改界面，让用户可以选择“使用简化版 Agent 或 LangGraph Agent”。

------

### 12. Agent容器化部署：构建生产可交付体

**教学准备**：切换到仓库根并打开 `04-agent-build-docker-deploy/backend/Dockerfile`、`04-agent-build-docker-deploy/frontend/Dockerfile`、`04-agent-build-docker-deploy/docker-compose.yml`、相关启动脚本，准备 Docker 环境。
**讲解结构**

1. 后端镜像构建（10 分钟）
   - 逐句讲解 Dockerfile：基础镜像、工作目录、复制依赖、安装、复制代码、暴露端口、启动命令。
   - 说明如何优化镜像大小（pip 缓存、.dockerignore 等）。
2. 前端镜像构建（5 分钟）
   - 分析前端 Dockerfile，解释为何禁用 Streamlit 使用数据收集、指定端口 8501。
3. Docker Compose 编排（10 分钟）
   - 讲解 docker/docker-compose.yml 中 backend 与 frontend 服务的配置：环境变量注入、端口映射、健康检查、依赖关系。
   - 提醒注意 .env 在 Compose 中的加载方式。
4. 启动脚本与实操（10 分钟）
   - 讲解 start_backend.sh、start_frontend.sh 在开发阶段的用途。
   - 现场运行 docker compose up --build，观察日志、验证健康检查状态。

**互动提示**

- 布置练习：让学员在本地跑通容器化版本，记录遇到的问题。
- 讨论：在云平台部署时，需要注意哪些环境变量和安全性问题？

------

### 13. Agent总结回顾：提炼实战经验与扩展方向

**教学准备**：整理整个项目的 checklist，准备白板或共享文档。
**讲解结构**

1. 知识回顾（10 分钟）
   - 按流程回顾：
     1. 环境配置 → 2. LangGraph LLM 设置 → 3. API 接入 → 4. 多智能体编排 → 5. 业务模块 → 6. FastAPI 服务 → 7. Streamlit 前端 → 8. Docker 部署。
   - 重申每一步的关键文件与注意事项。
2. 经验总结（5 分钟）
   - 请学员分享遇到的挑战及解决方式。
   - 强调常见实战心得：配置管理、日志与测试的重要性。
3. 扩展方向（5 分钟）
   - 提出扩展建议：
     - 增加测试覆盖率（pytest）；
     - 引入更多外部 API（航班、签证、保险）；
     - 利用 LangGraph 的高级特性（断点、回滚、观测）。
   - 鼓励学员将项目部署到云端或与团队协作版本控制。

**互动提示**

- 小组交流：下一步想做什么强化练习？
- 建议学员撰写学习笔记或博客，巩固所学。

------

### 课程实施建议

- 讲解时始终指引学员在编辑器中打开对应文件，边讲边看代码。
- 将重要命令、密钥配置、调试技巧写在板书或共享文档上，方便学员课后复习。
- 根据学员进度灵活调整演示与练习时间，关键概念可以多次重复。
- 鼓励学员课后将项目克隆到自己的仓库，进行个性化修改与扩展。