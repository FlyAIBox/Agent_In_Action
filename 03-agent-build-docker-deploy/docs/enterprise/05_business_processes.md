# AI 旅行规划智能体 - 关键业务流程文档

## 1. 旅行规划端到端流程

### 1.1 传统表单模式流程
```mermaid
flowchart TD
    A[用户提交表单\nStreamlit] --> B[POST /plan]
    B --> C[FastAPI 校验 & 生成 task_id]
    C --> D[写入 planning_tasks + save_tasks_state]
    D --> E[后台任务 run_planning_task]
    E --> F{LangGraph 执行成功?}
    F -- 是 --> G[合并结果\nTripSummary]
    F -- 超时/异常 --> H[调用 SimpleTravelAgent / 构建快速计划]
    G --> I[保存 results JSON]
    H --> I
    I --> J[更新任务状态为完成]
    J --> K[用户轮询 /status]
    K --> L[查看结果或下载 JSON]
```

### 1.2 自然语言交互模式流程（新增）
```mermaid
flowchart TD
    A[用户输入自然语言\nStreamlit聊天界面] --> B[POST /chat]
    B --> C[LLM 解析意图\n提取旅行信息]
    C --> D{信息完整度判断}
    
    D -- 完整\n置信度>0.6 --> E[自动生成 TravelRequest]
    E --> F[创建 task_id & 后台任务]
    F --> G[返回 ChatResponse\ncan_proceed=true]
    G --> H[前端自动跳转\n显示规划进度]
    
    D -- 不完整 --> I[返回 ChatResponse\ncan_proceed=false]
    I --> J[前端显示\n已识别+缺失信息]
    J --> K[用户补充信息]
    K --> A
    
    H --> L[LangGraph 执行规划]
    L --> M[轮询状态 & 下载结果]
```

## 2. LangGraph 节点执行流程
```mermaid
stateDiagram-v2
    [*] --> Coordinator
    Coordinator --> TravelAdvisor : 判断需求
    TravelAdvisor --> Tools : 需要实时资讯?
    Tools --> Coordinator
    Coordinator --> WeatherAnalyst
    WeatherAnalyst --> Coordinator
    Coordinator --> BudgetOptimizer
    BudgetOptimizer --> Coordinator
    Coordinator --> LocalExpert
    LocalExpert --> Coordinator
    Coordinator --> ItineraryPlanner
    ItineraryPlanner --> Coordinator
    Coordinator --> END : 已满足输出条件
```

## 3. 任务状态生命周期
```mermaid
stateDiagram-v2
    [*] --> Started
    Started --> Processing : run_planning_task 执行中
    Processing --> Completed : LangGraph 成功或简化方案
    Processing --> Failed : 异常且无法回退
    Completed --> Downloaded : 用户下载（逻辑上可能多次）
    Failed --> [*]
    Completed --> [*]
```

## 4. 外部数据服务调用流程
```mermaid
sequenceDiagram
    participant Modules
    participant QWeather
    participant AMap
    participant ExRate
    participant DuckDuckGo

    Modules->>QWeather: 获取天气/预警
    QWeather-->>Modules: JSON | 错误
    Modules->>AMap: 搜索景点/酒店
    AMap-->>Modules: JSON | 错误
    Modules->>ExRate: 获取汇率
    ExRate-->>Modules: JSON | 错误
    Modules->>DuckDuckGo: 搜索实时资讯
    DuckDuckGo-->>Modules: 列表 | 错误
    Modules-->>LangGraph: 汇总结构化数据，若失败则使用回退
```

## 5. 运维与异常处理流程
```mermaid
flowchart LR
    A[健康检查失败/报警] --> B{问题定位}
    B -- 配置缺失 --> C[检查 .env / Secrets]
    B -- 外部 API 异常 --> D[查看供应商状态 & 重试策略]
    B -- LangGraph 超时 --> E[确认资源或降级策略]
    B -- 代码异常 --> F[查看 logs /results]
    F --> G[修复后重新部署]
    E --> G
    D --> G
    C --> G
```

## 6. 运营关注流程
- **任务审计**：通过 `/tasks` 获取任务列表，筛选异常或长时间未完成的任务。
- **日志分析**：结合 Uvicorn/FastAPI 日志与结果文件，定位问题或优化内容。
- **人工干预**：若生成计划不符合客户需求，可根据 JSON 结果二次编辑或重新提交。
- **自然语言质量监控**：
  - 统计意图识别准确率（extracted vs. missing info）；
  - 分析常见失败模式，优化 LLM prompt；
  - 收集用户反馈，改进澄清问题的表达；
  - 监控自动创建任务的成功率与用户满意度。

## 7. SLA 与告警建议
- **SLA 指标**：
  - 任务成功率 ≥ 99%
  - 平均规划时长 ≤ 3 分钟
  - 超时回退比例 ≤ 5%
  - **自然语言意图识别准确率 ≥ 85%**
  - **自动创建任务成功率 ≥ 80%**
- **告警场景**：
  - `/health` 返回 warning/error。
  - 外部 API 连续 5 次失败。
  - 任务队列长度超过阈值（可通过 Redis/队列扩展实现）。
  - **LLM 解析连续失败 3 次以上**。
  - **意图识别置信度持续低于阈值**。

---

> 本文档面向运营、业务与技术团队，梳理旅行规划 Agent 在企业环境下的关键业务流程与异常处理路线。结合系统设计与部署文档，可构建完整的运维体系。

