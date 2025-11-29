"""
LangGraph旅行规划智能体系统

这个模块实现了基于LangGraph框架的多智能体旅行规划系统。
它使用 OpenAI 兼容的大语言模型，通过多个专业智能体
的协作来生成全面的旅行计划。

主要组件：
1. TravelPlanState - 定义智能体间共享的状态结构
2. LangGraphTravelAgents - 主要的多智能体系统类
3. 各种专业智能体方法 - 每个智能体负责特定的规划任务

适用于大模型技术初级用户：
- LangGraph是一个用于构建多智能体系统的框架
- StateGraph管理智能体间的状态流转
- 每个智能体都是一个专门的函数，处理特定的任务
- 智能体通过共享状态进行通信和协作
"""

from typing import Dict, Any, List, Optional, TypedDict, Annotated
import logging
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import json
from datetime import datetime

import sys
import os
# 添加backend目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.langgraph_config import langgraph_config as config

# --------------------------- 日志配置 ---------------------------
def setup_agents_logger():
    logger = logging.getLogger('langgraph_agents')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        fh = logging.FileHandler('logs/backend.log', encoding='utf-8')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

agents_logger = setup_agents_logger()

# 定义多智能体系统的状态结构
class TravelPlanState(TypedDict):
    """
    旅行规划状态类

    这个类定义了所有智能体共享的状态结构，包含了
    旅行规划过程中需要的所有信息。

    属性说明：
    - messages: 智能体间的消息历史
    - destination: 目的地
    - duration: 旅行天数
    - budget_range: 预算范围
    - interests: 兴趣爱好列表
    - group_size: 团队人数
    - travel_dates: 旅行日期
    - current_agent: 当前活跃的智能体
    - agent_outputs: 各智能体的输出结果
    - final_plan: 最终的旅行计划
    - iteration_count: 迭代次数
    """
    messages: Annotated[List[HumanMessage | AIMessage | SystemMessage], add_messages]
    destination: str
    duration: int
    budget_range: str
    interests: List[str]
    group_size: int
    travel_dates: str
    current_agent: str
    agent_outputs: Dict[str, Any]
    final_plan: Dict[str, Any]
    iteration_count: int

class LangGraphTravelAgents:
    """
    基于LangGraph的多智能体旅行规划系统

    这个类是整个多智能体系统的核心，它：
    1. 初始化 OpenAI 兼容大语言模型
    2. 创建和管理智能体工作流图
    3. 协调各个专业智能体的工作
    4. 处理智能体间的状态传递和消息通信

    适用于大模型技术初级用户：
    这个类展示了如何使用LangGraph框架构建复杂的
    多智能体系统，每个智能体都有专门的职责。
    """

    def __init__(self):
        """
        初始化LangGraph旅行智能体系统

        配置 OpenAI 兼容大语言模型并创建智能体工作流图
        """
        # 初始化 OpenAI 兼容大语言模型
        llm_config = config.get_llm_config()
        self.llm = ChatOpenAI(**llm_config)

        # 初始化智能体工作流图
        self.graph = self._create_agent_graph()

    def _create_agent_graph(self) -> StateGraph:
        """
        创建LangGraph多智能体工作流图

        解释：
        该方法负责构建整个多智能体系统的工作流图（StateGraph）。
        在LangGraph框架中，StateGraph用于定义各个智能体节点（如旅行顾问、天气分析师等）以及它们之间的连接关系和执行顺序。
        通过添加节点和设置条件边缘，可以灵活地控制智能体之间的协作流程，实现复杂的多智能体任务分工与协作。

        这个方法构建了智能体间的工作流程图，定义了：
        1. 各个智能体节点
        2. 智能体间的连接关系
        3. 工作流的执行顺序

        返回：配置好的StateGraph工作流对象
        """

        # 定义工作流图
        workflow = StateGraph(TravelPlanState)

        # 添加智能体节点
        workflow.add_node("travel_advisor", self._travel_advisor_agent)    # 旅行顾问
        workflow.add_node("weather_analyst", self._weather_analyst_agent)  # 天气分析师
        workflow.add_node("budget_optimizer", self._budget_optimizer_agent) # 预算优化师
        workflow.add_node("local_expert", self._local_expert_agent)        # 当地专家
        workflow.add_node("itinerary_planner", self._itinerary_planner_agent) # 行程规划师
        workflow.add_node("coordinator", self._coordinator_agent)             # 协调员
        workflow.add_node("tools", self._tool_executor_node)                  # 工具执行器

        # 定义工作流边缘（智能体间的连接）
        workflow.set_entry_point("coordinator")  # 设置协调员为入口点

        # 协调员决定调用哪些智能体
        workflow.add_conditional_edges(
            "coordinator",                    # 从协调员开始
            self._coordinator_router,         # 使用协调员路由器决定下一步
            {
                "travel_advisor": "travel_advisor",      # 可以转到旅行顾问
                "weather_analyst": "weather_analyst",    # 可以转到天气分析师
                "budget_optimizer": "budget_optimizer",  # 可以转到预算优化师
                "local_expert": "local_expert",          # 可以转到当地专家
                "itinerary_planner": "itinerary_planner", # 可以转到行程规划师
                "tools": "tools",                        # 可以转到工具执行器
                "end": END                               # 可以结束流程
            }
        )

        # 每个智能体都可以使用工具或返回协调员
        for agent in ["travel_advisor", "weather_analyst", "budget_optimizer", "local_expert", "itinerary_planner"]:
            workflow.add_conditional_edges(
                agent,                        # 从各个智能体
                self._agent_router,           # 使用智能体路由器决定下一步
                {
                    "tools": "tools",         # 可以转到工具执行器
                    "coordinator": "coordinator", # 可以返回协调员
                    "end": END               # 可以结束流程
                }
            )

        # 工具执行器总是返回协调员
        workflow.add_edge("tools", "coordinator")

        # 编译并返回工作流
        return workflow.compile()

    def _coordinator_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        协调员智能体 - 编排多智能体工作流

        协调员是整个系统的"大脑"，负责：
        1. 分析当前状态和需求
        2. 决定下一步需要哪个智能体工作
        3. 综合各智能体的输出
        4. 判断是否需要更多信息或可以结束

        参数：
        - state: 当前的旅行规划状态

        返回：更新后的状态
        """

        system_prompt = f"""您是多智能体旅行规划系统的协调员智能体。

您的职责是：
1. 分析旅行规划请求
2. 确定需要哪些专业智能体参与
3. 协调智能体间的工作流程
4. 综合最终建议

当前请求：
- 目的地: {state.get('destination', '未指定')}
- 时长: {state.get('duration', '未指定')} 天
- 预算: {state.get('budget_range', '未指定')}
- 兴趣: {', '.join(state.get('interests', []))}
- 团队人数: {state.get('group_size', 1)}
- 旅行日期: {state.get('travel_dates', '未指定')}

可用智能体：
- travel_advisor: 目的地专业知识和景点推荐
- weather_analyst: 天气预报和活动规划
- budget_optimizer: 成本分析和省钱策略
- local_expert: 本地洞察和文化贴士
- itinerary_planner: 日程优化和物流安排

目前智能体输出: {json.dumps(state.get('agent_outputs', {}), indent=2)}

根据当前状态，决定下一步行动：
1. 如果需要更多信息，指定下一个应该工作的智能体
2. 如果从所有相关智能体获得了足够信息，综合最终计划
3. 回应智能体名称或'FINAL_PLAN'（如果准备结束）

您的响应应该是以下之一：
- 下一个要调用的智能体名称 (travel_advisor, weather_analyst, budget_optimizer, local_expert, itinerary_planner)
- 'FINAL_PLAN' 如果准备创建综合旅行计划
- 'SEARCH' 如果需要先搜索信息
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-3:])  # Keep recent context
        
        response = self.llm.invoke(messages)
        
        # Update state
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "coordinator"
        new_state["iteration_count"] = state.get("iteration_count", 0) + 1
        
        return new_state
    
    def _travel_advisor_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        旅行顾问智能体，具有目的地专业知识

        这个智能体专门负责提供目的地相关的专业建议，
        包括景点推荐、文化洞察等。
        """

        system_prompt = f"""您是旅行顾问智能体，专门从事目的地专业知识和推荐服务。

您的专业领域包括：
- 目的地知识和亮点
- 景点推荐
- 文化洞察和贴士
- 旅行者优秀做法

当前规划请求：
- 目的地: {state.get('destination')}
- 时长: {state.get('duration')} 天
- 兴趣: {', '.join(state.get('interests', []))}
- 团队人数: {state.get('group_size')}

您的任务：提供全面的目的地建议，包括：
1. 顶级景点和必游之地
2. 文化洞察和礼仪贴士
3. 最佳住宿和探索区域
4. 基于兴趣的活动推荐

如果您需要搜索关于目的地的当前信息，请回复 'NEED_SEARCH: [搜索查询]'
否则，请基于您的知识提供专家建议。
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["travel_advisor"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "travel_advisor"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _weather_analyst_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        天气分析师智能体，专门进行气候和天气规划

        这个智能体专门负责天气情报分析和基于气候的
        活动规划建议。
        """

        system_prompt = f"""您是天气分析师智能体，专门从事天气情报和气候感知规划。

        您的专业领域包括：
        - 天气模式分析
        - 季节性旅行推荐
        - 基于天气条件的活动规划
        - 目的地气候考虑因素

        当前规划请求：
        - 目的地: {state.get('destination')}
        - 旅行日期: {state.get('travel_dates')}
        - 时长: {state.get('duration')} 天
        - 计划活动: {', '.join(state.get('interests', []))}

        ⚠️ 重要工作流程：
        1. 【强制要求】您必须首先调用天气搜索工具获取实时准确的天气数据
        2. 请立即回复：'NEED_SEARCH: {state.get('destination')} {state.get('travel_dates')} 天气预报'
        3. 获取天气数据后，再基于实际天气信息提供专业分析

        您的最终任务（在获取天气数据后）：
        1. 分析旅行日期期间的实际天气条件
        2. 基于真实天气数据推荐户外活动的最佳时间段
        3. 根据天气情况提供适合的活动建议
        4. 提供基于实际气候的打包建议

        注意：必须先获取实时天气数据，不要仅凭经验或历史气候知识进行推测。
        """
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["weather_analyst"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "weather_analyst"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _budget_optimizer_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        预算优化师智能体，专门进行成本分析和优化

        这个智能体专门负责旅行预算的分析和优化，
        提供省钱策略和成本效益建议。
        """

        system_prompt = f"""您是预算优化师智能体，专门从事成本分析和省钱策略。

您的专业领域包括：
- 旅行成本分析和预算制定
- 省钱贴士和策略
- 预算分配建议
- 经济实惠的替代方案

当前规划请求：
- 目的地: {state.get('destination')}
- 时长: {state.get('duration')} 天
- 预算范围: {state.get('budget_range')}
- 团队人数: {state.get('group_size')}

您的任务：提供预算优化建议，包括：
1. 估算每日和总费用
2. 按类别分解预算（住宿、餐饮、活动、交通）
3. 省钱贴士和策略
4. 昂贵活动的经济实惠替代方案

如果您需要当前价格信息，请回复 'NEED_SEARCH: [预算搜索查询]'
否则，请提供您的预算分析和建议。
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["budget_optimizer"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "budget_optimizer"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _local_expert_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        当地专家智能体，具有内部知识和本地洞察

        这个智能体专门提供只有当地人才知道的内部信息，
        包括小众景点、文化习俗和实用贴士。
        """

        system_prompt = f"""您是当地专家智能体，专门从事内部知识和本地洞察。

您的专业领域包括：
- 当地习俗和文化细节
- 小众景点和小众推荐
- 本地餐饮和娱乐场所
- 实用的本地贴士和建议

当前规划请求：
- 目的地: {state.get('destination')}
- 兴趣: {', '.join(state.get('interests', []))}
- 时长: {state.get('duration')} 天

您的任务：提供当地专家洞察，包括：
1. 小众景点和当地人喜爱的地方
2. 文化礼仪和习俗
3. 本地餐饮推荐
4. 出行和省钱的内部贴士

如果您需要当前本地信息，请回复 'NEED_SEARCH: [本地贴士搜索查询]'
否则，请提供您的本地专业知识和洞察。
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["local_expert"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "local_expert"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _itinerary_planner_agent(self, state: TravelPlanState) -> TravelPlanState:
        """
        行程规划师智能体，专门进行日程优化和物流安排

        这个智能体专门负责创建优化的日程安排，
        协调交通和活动的时间安排。
        """

        system_prompt = f"""您是行程规划师智能体，专门从事日程优化和物流安排。

您的专业领域包括：
- 每日行程规划和优化
- 交通和物流协调
- 时间管理和日程安排
- 活动排序和路线规划

当前规划请求：
- 目的地: {state.get('destination')}
- 时长: {state.get('duration')} 天
- 团队人数: {state.get('group_size')}
- 可用智能体洞察: {list(state.get('agent_outputs', {}).keys())}

您的任务：创建优化的行程安排，包括：
1. 逐日日程推荐
2. 活动的最佳时间安排
3. 地点间的交通建议
4. 休息时间和用餐安排

在创建行程时请考虑其他智能体的建议。
提供结构化的每日计划，最大化旅行体验。
"""
        
        messages = [SystemMessage(content=system_prompt)]
        if state.get("messages"):
            messages.extend(state["messages"][-2:])
        
        response = self.llm.invoke(messages)
        
        # Store agent output
        agent_outputs = state.get("agent_outputs", {})
        agent_outputs["itinerary_planner"] = {
            "response": response.content,
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        
        new_state = state.copy()
        new_state["messages"] = state.get("messages", []) + [response]
        new_state["current_agent"] = "itinerary_planner"
        new_state["agent_outputs"] = agent_outputs
        
        return new_state
    
    def _tool_executor_node(self, state: TravelPlanState) -> TravelPlanState:
        """
        工具执行节点，根据智能体请求执行工具

        这个节点负责解析智能体的工具请求，
        并执行相应的搜索工具来获取实时信息。
        """

        last_message = state["messages"][-1] if state.get("messages") else None
        if not last_message:
            return state

        # 检查最后一条消息是否请求搜索
        content = last_message.content
        if "NEED_SEARCH:" in content:
            search_query = content.split("NEED_SEARCH:")[-1].strip()

            # 根据当前智能体和查询确定使用哪个工具
            current_agent = state.get("current_agent", "")
            agents_logger.info(f"[ToolExecutor] 解析到搜索需求 | 当前智能体: {current_agent} | 查询: {search_query}")
            
            try:
                # 智能工具选择：根据查询内容和当前智能体选择最合适的搜索工具
                selected_tool = ""
                if "weather" in search_query.lower() or "天气" in search_query or current_agent == "weather_analyst":
                    selected_tool = "search_weather_info"
                    # 天气相关查询：使用天气信息搜索工具
                    from tools.travel_tools import search_weather_info
                    tool_params = {"destination": state.get("destination", ""),
                                   "dates": state.get("travel_dates", "")}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    # 该工具为异步工具，需使用 ainvoke 在独立事件循环中执行
                    import asyncio
                    loop = asyncio.new_event_loop()
                    try:
                        asyncio.set_event_loop(loop)
                        tool_result = loop.run_until_complete(search_weather_info.ainvoke(tool_params))
                    finally:
                        loop.close()
                        try:
                            asyncio.set_event_loop(None)
                        except Exception:
                            pass
                elif "attraction" in search_query.lower() or "activity" in search_query.lower() or "景点" in search_query or "活动" in search_query:
                    selected_tool = "search_attractions"
                    # 景点活动查询：使用景点搜索工具
                    from tools.travel_tools import search_attractions
                    tool_params = {"destination": state.get("destination", ""),
                                   "interests": " ".join(state.get("interests", []))}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_attractions.invoke(tool_params)
                elif "budget" in search_query.lower() or "cost" in search_query.lower() or "预算" in search_query or "费用" in search_query:
                    selected_tool = "search_budget_info"
                     # 预算费用查询：使用预算信息搜索工具
                    from tools.travel_tools import search_budget_info
                    tool_params = {"destination": state.get("destination", ""),
                                   "duration": str(state.get("duration", ""))}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_budget_info.invoke(tool_params)
                elif "hotel" in search_query.lower() or "accommodation" in search_query.lower() or "酒店" in search_query or "住宿" in search_query:
                    selected_tool = "search_hotels"
                    # 住宿查询：使用酒店搜索工具
                    from tools.travel_tools import search_hotels
                    tool_params = {"destination": state.get("destination", ""),
                                   "budget": state.get("budget_range", "mid-range")}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_hotels.invoke(tool_params)
                elif "restaurant" in search_query.lower() or "food" in search_query.lower() or "餐厅" in search_query or "美食" in search_query:
                    selected_tool = "search_restaurants"
                     # 餐饮查询：使用餐厅搜索工具
                    from tools.travel_tools import search_restaurants
                    tool_params = {"destination": state.get("destination", "")}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_restaurants.invoke(tool_params)
                elif "local" in search_query.lower() or "tip" in search_query.lower() or "本地" in search_query or "贴士" in search_query:
                    selected_tool = "search_local_tips"
                    # 本地贴士查询：使用本地贴士搜索工具
                    from tools.travel_tools import search_local_tips
                    tool_params = {"destination": state.get("destination", "")}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_local_tips.invoke(tool_params)
                else:
                    selected_tool = "search_destination_info"
                    # 默认选择：使用目的地信息搜索工具
                    from tools.travel_tools import search_destination_info
                    tool_params = {"query": state.get("destination", "")}
                    agents_logger.info(f"[ToolExecutor] 调用工具: {selected_tool} | 参数: {tool_params}")
                    tool_result = search_destination_info.invoke(tool_params)

                # 记录工具返回结果大小（避免日志过大）
                result_str = str(tool_result)
                agents_logger.info(f"[ToolExecutor] 工具返回: {selected_tool} | 长度: {len(result_str)} 字符")

                # 将工具执行结果添加到消息历史中
                tool_message = AIMessage(content=f"搜索结果: {tool_result}")
                new_state = state.copy()
                new_state["messages"] = state.get("messages", []) + [tool_message]
                return new_state

            except Exception as e:
                agents_logger.error(f"[ToolExecutor] 工具执行错误: {str(e)}")
                # 工具执行失败时添加错误消息
                error_message = AIMessage(content=f"工具执行错误: {str(e)}")
                new_state = state.copy()
                new_state["messages"] = state.get("messages", []) + [error_message]
                return new_state

        return state

    def _coordinator_router(self, state: TravelPlanState) -> str:
        """
        协调员路由器：从协调员决定下一步流程

        这个方法分析协调员的输出，决定下一步应该调用哪个智能体
        或执行哪个操作。这是LangGraph工作流的核心路由逻辑。

        参数：
        - state: 当前的旅行规划状态

        返回：下一个要执行的节点名称

        适用于大模型技术初级用户：
        这个路由器展示了如何在复杂的AI系统中实现智能决策，
        根据上下文动态选择下一步的执行路径。
        """

        last_message = state.get("messages", [])[-1] if state.get("messages") else None
        if not last_message:
            agents_logger.info("[CoordinatorRouter] 无最近消息，结束流程")
            return "end"

        content = last_message.content.lower()

        # 路由决策逻辑：根据协调员的输出内容决定下一步行动
        agents_logger.info(f"[CoordinatorRouter] 协调员输出: {content}")

        # 检查协调员是否需要搜索工具
        if "search" in content or "need_search" in content or "搜索" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 进入工具执行节点")
            return "tools"

        # 检查协调员是否请求特定的智能体
        if "travel_advisor" in content or "旅行顾问" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 跳转 travel_advisor")
            return "travel_advisor"
        elif "weather_analyst" in content or "天气分析师" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 跳转 weather_analyst")
            return "weather_analyst"
        elif "budget_optimizer" in content or "预算优化师" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 跳转 budget_optimizer")
            return "budget_optimizer"
        elif "local_expert" in content or "当地专家" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 跳转 local_expert")
            return "local_expert"
        elif "itinerary_planner" in content or "行程规划师" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 跳转 itinerary_planner")
            return "itinerary_planner"
        elif "final_plan" in content or "最终计划" in content:
            agents_logger.info("[CoordinatorRouter] 决策: 结束流程")
            return "end"

        # 默认策略：检查哪些智能体还没有参与工作
        agent_outputs = state.get("agent_outputs", {})
        required_agents = ["travel_advisor", "weather_analyst", "budget_optimizer", "local_expert", "itinerary_planner"]

        # 按优先级顺序调用尚未参与的智能体
        for agent in required_agents:
            if agent not in agent_outputs:
                agents_logger.info(f"[CoordinatorRouter] 决策: 跳转 {agent} (尚未参与)")
                return agent

        # 如果所有智能体都已参与，结束流程
        agents_logger.info("[CoordinatorRouter] 决策: 所有智能体已参与，结束流程")
        return "end"
    
    def _agent_router(self, state: TravelPlanState) -> str:
        """
        智能体路由器：从智能体决定下一步流程

        这个方法处理各个专业智能体完成工作后的路由决策，
        决定是返回协调员还是执行工具搜索。

        参数：
        - state: 当前的旅行规划状态

        返回：下一个要执行的节点名称

        适用于大模型技术初级用户：
        这展示了多智能体系统中的反馈循环机制，
        智能体可以请求更多信息或将控制权交还给协调员。
        """

        last_message = state.get("messages", [])[-1] if state.get("messages") else None
        if not last_message:
            agents_logger.info("[AgentRouter] 无最近消息，返回协调员")
            return "coordinator"

        content = last_message.content

        # 检查智能体是否需要搜索更多信息
        if "NEED_SEARCH:" in content:
            agents_logger.info("[AgentRouter] 检测到搜索需求，跳转工具节点")
            return "tools"

        # 否则返回协调员进行下一步决策
        agents_logger.info("[AgentRouter] 返回协调员继续决策")
        return "coordinator"
    
    def run_travel_planning(self, travel_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行完整的多智能体旅行规划工作流

        这是整个AI旅行规划智能体的主入口方法，
        它初始化状态、执行工作流并返回最终的旅行计划。

        参数：
        - travel_request: 包含旅行需求的字典

        返回：包含旅行计划和执行结果的字典

        适用于大模型技术初级用户：
        这个方法展示了如何将复杂的AI系统封装成简单的API，
        用户只需提供需求，系统就能自动协调多个智能体完成规划。
        """

        # 初始化系统状态
        initial_state = TravelPlanState(
            messages=[HumanMessage(content=f"根据以下需求规划旅行: {json.dumps(travel_request, ensure_ascii=False)}")],
            destination=travel_request.get("destination", ""),
            duration=travel_request.get("duration", 3),
            budget_range=travel_request.get("budget_range", "中等预算"),
            interests=travel_request.get("interests", []),
            group_size=travel_request.get("group_size", 1),
            travel_dates=travel_request.get("travel_dates", ""),
            current_agent="",
            agent_outputs={},
            final_plan={},
            iteration_count=0
        )

        # 执行多智能体工作流
        try:
            # 调用LangGraph工作流图，开始多智能体协作
            final_state = self.graph.invoke(initial_state)

            # 编译最终的旅行计划
            final_plan = self._compile_final_plan(final_state)

            # 返回成功结果
            return {
                "success": True,                                           # 执行成功标志
                "travel_plan": final_plan,                                # 完整的旅行计划
                "agent_outputs": final_state.get("agent_outputs", {}),   # 各智能体的输出
                "total_iterations": final_state.get("iteration_count", 0), # 总迭代次数
                "planning_complete": True                                  # 规划完成标志
            }

        except Exception as e:
            # 错误处理：返回失败结果和错误信息
            return {
                "success": False,                    # 执行失败标志
                "error": f"规划过程中出现错误: {str(e)}", # 错误信息
                "travel_plan": {},                   # 空的旅行计划
                "agent_outputs": {},                 # 空的智能体输出
                "total_iterations": 0,               # 迭代次数为0
                "planning_complete": False           # 规划未完成
            }
    
    def _compile_final_plan(self, state: TravelPlanState) -> Dict[str, Any]:
        """
        从所有智能体输出编译最终旅行计划

        这个方法整合所有专业智能体的建议和分析，
        生成一个完整、结构化的旅行计划。

        参数：
        - state: 包含所有智能体输出的最终状态

        返回：完整的旅行计划字典

        适用于大模型技术初级用户：
        这个方法展示了如何将多个AI智能体的输出
        整合成一个统一、有用的最终产品。
        """

        agent_outputs = state.get("agent_outputs", {})

        # 构建基础旅行计划结构
        final_plan = {
            "destination": state.get("destination"),                      # 目的地
            "duration": state.get("duration"),                           # 旅行时长
            "travel_dates": state.get("travel_dates"),                   # 旅行日期
            "group_size": state.get("group_size"),                       # 团队人数
            "budget_range": state.get("budget_range"),                   # 预算范围
            "interests": state.get("interests"),                         # 兴趣爱好
            "planning_method": "LangGraph多智能体协作",                   # 规划方法
            "agent_contributions": {},                                    # 智能体贡献
            "recommendations": {},                                        # 推荐建议
            "summary": "使用LangGraph框架的多智能体协作生成的旅行计划"      # 计划摘要
        }

        # 从每个智能体提取关键信息
        for agent_name, output in agent_outputs.items():
            agent_name_cn = {
                'travel_advisor': '旅行顾问',
                'weather_analyst': '天气分析师',
                'budget_optimizer': '预算优化师',
                'local_expert': '当地专家',
                'itinerary_planner': '行程规划师'
            }.get(agent_name, agent_name)

            final_plan["agent_contributions"][agent_name_cn] = {
                "contribution": output.get("response", ""),               # 智能体的具体建议
                "timestamp": output.get("timestamp", ""),                 # 生成时间戳
                "status": output.get("status", "")                       # 执行状态
            }

        # 生成总结性推荐
        if agent_outputs:
            final_plan["recommendations"] = {
                "destination_highlights": "查看旅行顾问推荐",
                "weather_considerations": "查看天气分析师洞察",
                "budget_breakdown": "查看预算优化师分析",
                "local_insights": "遵循当地专家贴士",
                "daily_itinerary": "使用行程规划师日程"
            }

        return final_plan
