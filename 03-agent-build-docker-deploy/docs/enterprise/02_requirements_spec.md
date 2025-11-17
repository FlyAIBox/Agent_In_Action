# AI 旅行规划智能体 - 需求规格说明书

## 1. 文档目的
在企业真实应用场景中，明确 AI 旅行规划智能体的功能、非功能和集成需求，为技术设计、实现与测试提供可追溯依据。

## 2. 术语
- **Agent**：指 LangGraphTravelAgents 为核心的多智能体协作系统。
- **Task**：一次旅行规划请求的生命周期，从创建到完成/失败。
- **POI**：Point of Interest，包括景点、餐饮、活动等。

## 3. 需求概览
| 编号 | 需求类型 | 描述 |
| ---- | -------- | ---- |
| FR-01 | 功能 | 用户可提交旅行规划请求（表单或自然语言），系统生成任务并返回 `task_id`。 |
| FR-02 | 功能 | 系统异步执行多智能体规划，生成行程、预算、天气等建议。 |
| FR-03 | 功能 | 用户可查询任务状态、查看进度与结果。 |
| FR-04 | 功能 | 用户可下载结果 JSON，用于后续人工编辑或归档。 |
| FR-05 | 功能 | 支持简化模式（SimpleTravelAgent）和模拟模式（MockTravelAgent）作为回退。 |
| FR-06 | 功能 | 集成 DuckDuckGo、QWeather提供实时数据。 |
| FR-07 | 功能 | 支持任务列表检索，便于运营与审计。 |
| FR-08 | 功能 | **支持自然语言交互，用户可用对话方式描述旅行需求，AI自动提取关键信息并创建任务。** |
| NFR-01 | 非功能 | 关键接口响应时间（非规划过程）≤ 1s。 |
| NFR-02 | 非功能 | 规划任务超时时间默认 5 分钟，超时需自动降级。 |
| NFR-03 | 非功能 | 系统需提供健康检查 `/health`，返回配置可用性与系统资源信息。 |
| NFR-04 | 非功能 | 支持容器化部署、无状态扩缩，任务状态保存在共享存储或数据库。 |
| NFR-05 | 非功能 | 日志与任务结果需可追溯，保留至少 30 天（可配置）。 |
| NFR-06 | 非功能 | 访问外部 API 失败时需重试或使用回退数据，保证 99% 成功率。 |
| INT-01 | 集成 | 环境变量管理（`OPENAI_API_KEY`、`QWEATHER_API_KEY` 等）遵循安全规范，不写死在代码。 |
| INT-02 | 集成 | 提供 JSON 接口，便于 ERP/CRM 等系统二次集成。 |

## 4. 详细功能需求
### 4.1 旅行规划请求（FR-01）
- 输入：`TravelRequest`（目的地、日期、预算、兴趣等）。
- 校验规则：
  - `destination` 必填，非空字符串。
  - `start_date`、`end_date` 格式为 `YYYY-MM-DD`，且 `start_date <= end_date`。
  - `group_size` >= 1，若为 0 系统默认按 1 人处理（现有代码已做回退）。
- 处理：创建任务对象，写入 `planning_tasks`，保存至 `tasks_state.json`。
- 输出：`PlanningResponse`（包含 `task_id` 和初始状态）。

### 4.2 多智能体规划（FR-02）
- 调用 `LangGraphTravelAgents.run_planning`，流程包括：
  1. 协调员分析需求并确定调用顺序。
  2. 旅行顾问、天气分析师、预算优化师、当地专家、行程规划师依次处理。
  3. 工具节点通过 `travel_tools.ALL_TOOLS` 调用 DuckDuckGo 搜索。
- 输出：综合的旅行计划字典，写入任务状态 `result` 字段并保存 JSON。

### 4.3 任务状态查询（FR-03）
- 输入：`task_id`。
- 逻辑：从 `planning_tasks` 获取状态，返回进度、当前执行节点、消息、结果摘要。
- 错误处理：任务不存在返回 404；内部错误返回 500。

### 4.4 结果下载（FR-04）
- 根据 `task_id` 查找 `results/` 目录下的 JSON 文件，返回 `FileResponse`。
- 文件命名：`旅行计划_{destination}_{timestamp}.json`。

### 4.5 回退/模拟模式（FR-05）
- `/simple-plan`: 使用 `SimpleTravelAgent` 同步生成计划，适合快速响应或回退。
- `/mock-plan`: 返回 `MockTravelAgent` 的固定格式结果，用于测试与接口联调。

### 4.6 外部服务集成（FR-06）
- **DuckDuckGo 搜索**：无需 Key，通过 `ddgs` 库调用，需注意节流。
- **QWeather**：可选配置 `QWEATHER_API_KEY`，通过MCP天气服务器提供结构化天气数据，无配置时回退到DuckDuckGo搜索。
- **DuckDuckGo搜索**：主要数据源，无需API密钥，提供目的地、景点、酒店、餐厅等信息。
- **MCP天气服务器**：集成QWeather API，提供专业天气预报数据。
- 失败处理：任一服务异常时，模块需捕获异常并提供合理回退（如模拟数据）。

### 4.7 任务列表（FR-07）
- 输出任务概要：`task_id`、状态、创建时间、目的地。
- 用途：运营监控与人工修正。

### 4.8 自然语言交互（FR-08）
- **输入**：用户自然语言描述（如"我想下周去北京玩3天，预算3000元，喜欢历史文化"）。
- **AI解析流程**：
  1. 使用 LLM 分析用户输入，识别关键要素（目的地、时间、预算、人数、兴趣等）；
  2. 提取结构化信息，生成 `ChatResponse`（包含已识别和缺失信息）；
  3. 判断信息完整度：
     - 若关键信息齐全（目的地+时间信息）且置信度>0.6，自动创建规划任务；
     - 若信息不足，返回澄清问题，引导用户补充；
  4. 自动填充默认值（如未指定人数默认2人，未指定预算默认"中等预算"）。
- **校验规则**：
  - 必须包含目的地（destination）；
  - 必须包含时间信息（start_date/end_date/duration 至少一个）；
  - 置信度阈值 ≥ 0.6 才可自动创建任务。
- **输出**：
  - `understood`: 是否理解用户意图；
  - `extracted_info`: 已提取的旅行信息字典；
  - `missing_info`: 缺失的信息列表；
  - `clarification`: 友好的反馈文本；
  - `can_proceed`: 是否可直接创建任务；
  - `task_id`: 如成功创建则返回任务ID。
- **用户体验增强**：
  - 提供快捷示例按钮（如"北京3日游"），点击自动填充；
  - 大型文本输入框（400px高度），支持详细描述；
  - 实时显示AI理解的信息和需要补充的内容；
  - 自动跳转到规划进度页面。
- **错误处理**：
  - LLM 解析失败时，返回友好提示，引导用户重新描述；
  - 自动创建任务失败时，降级为手动表单模式。

## 5. 非功能需求细化
### 5.1 性能
- FastAPI 接口应保持无状态，多实例部署时 `planning_tasks` 可迁移至 Redis/数据库。
- 任务执行使用协程 + 线程池，避免主线程阻塞。

### 5.2 可用性
- `save_tasks_state`、`load_tasks_state` 对存储失败需记录日志并允许空状态运行。
- LangGraph 超时后调用简化版智能体，确保计划可用。

### 5.3 安全
- 配置文件 `.env` 不提交；敏感字段通过 Secrets Manager 注入。
- 接口需在生产环境部署于 HTTPS，支持身份鉴权（后续扩展）。

### 5.4 可维护性
- 代码模块化：Agents、Modules、Tools 分层清晰。
- 注释和文档完整，方便新成员理解（参考 `backend/data/models.py`、`backend/api_server.py` 的中文注释）。

## 6. 环境与依赖
- Python 3.10+
- FastAPI, Uvicorn, LangGraph, LangChain-Core, DuckDuckGo Search, httpx, requests。
- 需访问外部 API（QWeather、AMap、Exchangerate-API）。
- Docker & Docker Compose 用于部署。

## 7. 约束与假设
- 假设部署地区网络可访问上述外部服务；如受限需配置代理。
- 假设用户提供的时间范围、预算、兴趣合理；极端值时系统执行会更慢或输出空结果。
- `tasks_state.json` 为默认持久化方案；在生产环境应替换为可靠存储（如数据库）。

## 8. 需求追踪矩阵（示例）
| 需求 | 实现模块/文件 | 测试方式 |
| ---- | ------------- | -------- |
| FR-01 | `backend/api_server.py:create_travel_plan` + `chat_with_ai` | API 集成测试 |
| FR-02 | `backend/agents/langgraph_agents.py` + `modules/` | 自动化脚本 + 人工验证 |
| FR-03 | `backend/api_server.py:get_planning_status` | API 集成测试 |
| FR-04 | `backend/api_server.py:download_result` | API 集成测试 |
| FR-05 | `backend/api_server.py:simple_travel_plan/mock_travel_plan` | 单元测试 + 集成测试 |
| FR-06 | `modules/` + `tools/travel_tools.py` | API Mock 测试 |
| FR-07 | `backend/api_server.py:list_tasks` | API 集成测试 |
| FR-08 | `backend/api_server.py:chat_with_ai` + `frontend/streamlit_app.py:display_chat_interface` | 自然语言理解测试 + 端到端测试 |
| NFR-01 | FastAPI + Uvicorn 配置 | 性能压测 |
| NFR-02 | `run_planning_task` 超时策略 | 人工模拟超时场景 |
| NFR-03 | `/health` 路由 | 功能测试 |

---

> 本说明书适用于实际企业应用的需求评审与验收，可与日志、监控和安全策略结合进一步扩展。详细技术设计和部署计划见 `03_system_design.md`、`06_deployment_and_operations.md`。

