"""
LangGraph智能体工具集

这个模块包含了AI旅行规划智能体使用的所有搜索工具，包括：
- 目的地信息搜索
- 天气信息查询
- 景点发现
- 酒店搜索
- 餐厅查找
- 当地贴士获取
- 预算信息分析

适用于大模型技术初级用户：
这个模块展示了如何为AI智能体创建专门的工具，
每个工具都有特定的功能和搜索策略，通过DuckDuckGo
搜索引擎获取实时信息。
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from langchain_core.tools import tool
from duckduckgo_search import DDGS
import json
import re
from datetime import datetime
from .weather_client_mcp import fetch_forecast_via_mcp

# 配置详细日志记录器
def setup_travel_logger():
    """设置日志记录器"""
    logger = logging.getLogger('travel_tools')
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # 确保日志目录存在
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # 创建文件处理器
        file_handler = logging.FileHandler('logs/backend.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 设置详细日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
    
    return logger

# 创建全局日志记录器
travel_logger = setup_travel_logger()

# 直接定义工具函数，不使用类包装
@tool
def search_destination_info(query: str) -> str:
    """
    使用DuckDuckGo搜索目的地信息

    这个工具专门用于搜索旅行目的地的综合信息，
    包括景点、旅游指南、文化背景等。

    参数：
    - query: 搜索查询字符串（目的地名称）

    返回：格式化的搜索结果字符串

    功能说明：
    1. 构建专门的搜索查询
    2. 使用DuckDuckGo进行搜索
    3. 格式化结果供智能体理解
    4. 处理搜索错误和异常情况
    """
    travel_logger.info(f"调用目的地信息搜索工具 - 查询: {query}")
    
    try:
        # 使用DuckDuckGo搜索引擎
        search_query = query + " 旅游目的地指南景点"
        travel_logger.info(f"构建搜索查询: {search_query}")
        
        with DDGS() as ddgs:
            # 构建搜索查询，添加旅游相关关键词
            results = list(ddgs.text(
                search_query,  # 中文搜索关键词
                max_results=5,  # 最大结果数
                region="cn-zh",            # 搜索区域
                safesearch="moderate"     # 安全搜索级别
            ))

            travel_logger.info(f"DuckDuckGo 搜索返回 {len(results)} 个结果")

            # 检查是否有搜索结果
            if not results:
                error_msg = f"未找到目的地搜索结果: {query}"
                travel_logger.warning(error_msg)
                return error_msg

            # 格式化结果供智能体使用
            formatted_results = []
            for i, result in enumerate(results[:5], 1):  # 取前5个结果
                title = result.get('title', '无标题')
                body = result.get('body', '无描述')
                href = result.get('href', '无URL')
                
                formatted_results.append(
                    f"{i}. {title}\n"
                    f"   {body}\n"
                    f"   来源: {href}\n"
                )
                
                travel_logger.debug(f"结果 {i}: {title[:50]}...")

            result_text = "\n".join(formatted_results)
            travel_logger.info(f"目的地信息搜索成功，返回 {len(formatted_results)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索目的地信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
async def search_weather_info(destination: str, dates: str = "") -> str:
    """
    搜索目的地天气信息

    这个工具专门用于搜索特定目的地的天气预报信息，
    包括气候条件、最佳旅行时间等。

    参数：
    - destination: 目的地名称
    - dates: 日期信息（可选）

    返回：格式化的天气信息字符串
    """
    travel_logger.info(f"调用天气信息搜索工具 - 目的地: {destination}, 日期: {dates}")
    
    # First try MCP weather server (structured forecast)
    try:
        travel_logger.info("尝试使用 MCP 天气服务器获取天气预报")
        
        # Simple heuristic to map dates string to forecast days
        days = 7
        text = dates.lower()
        if any(k in text for k in ["7天", "七天", "7d", "一周", "week"]):
            days = 7
        elif any(k in text for k in ["10天", "十天", "10d"]):
            days = 10
        elif any(k in text for k in ["15天", "十五天", "15d"]):
            days = 15
        elif any(k in text for k in ["30天", "三十天", "30d", "一个月"]):
            days = 30

        travel_logger.info(f"MCP 调用参数 - 位置: {destination}, 天数: {days}")

        forecast = await fetch_forecast_via_mcp(location=destination, days=days)
        if forecast and isinstance(forecast, str) and forecast.strip():
            travel_logger.info(f"MCP 天气服务器调用成功，返回数据长度: {len(forecast)} 字符")
            result = f"{destination}的天气预报（MCP）：\n{forecast}"
            travel_logger.info("天气信息工具使用 MCP 数据返回成功")
            return result
        else:
            travel_logger.warning("MCP 返回数据为空，回退到 DuckDuckGo 搜索")
            
    except Exception as e:
        travel_logger.warning(f"MCP 天气服务器调用失败: {str(e)}，回退到 DuckDuckGo 搜索")

    # Fallback: DuckDuckGo search
    try:
        travel_logger.info("使用 DuckDuckGo 搜索获取天气信息")
        weather_query = f"{destination} 天气预报 {dates} 旅行气候"
        travel_logger.info(f"DuckDuckGo 搜索查询: {weather_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                weather_query,
                max_results=5,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"DuckDuckGo 天气搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的天气信息"
                travel_logger.warning(error_msg)
                return error_msg

            weather_info = []
            for i, result in enumerate(results[:3], 1):
                title = result.get('title', '天气信息')
                body = result.get('body', '无详细信息')
                
                weather_info.append(
                    f"• {title}\n"
                    f"  {body}\n"
                )
                
                travel_logger.debug(f"天气搜索结果 {i}: {title[:50]}...")

            result_text = f"{destination}的天气信息:\n" + "\n".join(weather_info)
            travel_logger.info(f"DuckDuckGo 天气搜索成功，返回 {len(weather_info)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索天气信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
def search_attractions(destination: str, interests: str = "") -> str:
    """
    搜索目的地景点和活动

    这个工具专门用于搜索特定目的地的热门景点、
    活动和必游之地，可以根据兴趣进行筛选。

    参数：
    - destination: 目的地名称
    - interests: 兴趣关键词（可选）

    返回：格式化的景点信息字符串
    """
    travel_logger.info(f"调用景点搜索工具 - 目的地: {destination}, 兴趣: {interests}")
    
    try:
        attraction_query = f"{destination} 热门景点 活动 {interests} 必游之地"
        travel_logger.info(f"景点搜索查询: {attraction_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                attraction_query,
                max_results=8,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"景点搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的景点信息"
                travel_logger.warning(error_msg)
                return error_msg

            attractions = []
            for i, result in enumerate(results[:6], 1):
                title = result.get('title', '景点')
                body = result.get('body', '无描述')[:200]
                
                attractions.append(
                    f"{i}. {title}\n"
                    f"   {body}...\n"
                )
                
                travel_logger.debug(f"景点结果 {i}: {title[:50]}...")

            result_text = f"{destination}的热门景点:\n" + "\n".join(attractions)
            travel_logger.info(f"景点搜索成功，返回 {len(attractions)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索景点信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
def search_hotels(destination: str, budget: str = "中等预算") -> str:
    """
    搜索酒店信息和价格

    这个工具专门用于搜索特定目的地的酒店选择，
    包括住宿选项、价格信息和最佳住宿地点。

    参数：
    - destination: 目的地名称
    - budget: 预算范围（默认“中等预算”）

    返回：格式化的酒店信息字符串
    """
    travel_logger.info(f"调用酒店搜索工具 - 目的地: {destination}, 预算: {budget}")
    
    try:
        hotel_query = f"{destination} 酒店 {budget} 最佳住宿 住宿推荐"
        travel_logger.info(f"酒店搜索查询: {hotel_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                hotel_query,
                max_results=6,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"酒店搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的酒店信息"
                travel_logger.warning(error_msg)
                return error_msg

            hotels = []
            for i, result in enumerate(results[:4], 1):
                title = result.get('title', '酒店')
                body = result.get('body', '无详细信息')[:180]
                
                hotels.append(
                    f"{i}. {title}\n"
                    f"   {body}...\n"
                )
                
                travel_logger.debug(f"酒店结果 {i}: {title[:50]}...")

            result_text = f"{destination}的酒店选择 ({budget}预算):\n" + "\n".join(hotels)
            travel_logger.info(f"酒店搜索成功，返回 {len(hotels)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索酒店信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
def search_restaurants(destination: str, cuisine: str = "") -> str:
    """
    搜索餐厅和用餐选择

    这个工具专门用于搜索特定目的地的餐厅推荐，
    包括当地美食、特色菜系和用餐地点。

    参数：
    - destination: 目的地名称
    - cuisine: 菜系类型（可选）

    返回：格式化的餐厅推荐字符串
    """
    travel_logger.info(f"调用餐厅搜索工具 - 目的地: {destination}, 菜系: {cuisine}")
    
    try:
        restaurant_query = f"{destination} 最佳餐厅 {cuisine} 当地美食 用餐推荐"
        travel_logger.info(f"餐厅搜索查询: {restaurant_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                restaurant_query,
                max_results=6,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"餐厅搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的餐厅信息"
                travel_logger.warning(error_msg)
                return error_msg

            restaurants = []
            for i, result in enumerate(results[:4], 1):
                title = result.get('title', '餐厅')
                body = result.get('body', '无详细信息')[:180]
                
                restaurants.append(
                    f"{i}. {title}\n"
                    f"   {body}...\n"
                )
                
                travel_logger.debug(f"餐厅结果 {i}: {title[:50]}...")

            result_text = f"{destination}的餐厅推荐:\n" + "\n".join(restaurants)
            travel_logger.info(f"餐厅搜索成功，返回 {len(restaurants)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索餐厅信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
def search_local_tips(destination: str) -> str:
    """
    搜索当地贴士、文化和内部信息

    这个工具专门用于搜索目的地的当地文化、
    礼仪习俗和内部旅行贴士。

    参数：
    - destination: 目的地名称

    返回：格式化的当地贴士字符串
    """
    travel_logger.info(f"调用当地贴士搜索工具 - 目的地: {destination}")
    
    try:
        tips_query = f"{destination} 当地贴士 旅行指南 文化礼仪 注意事项"
        travel_logger.info(f"当地贴士搜索查询: {tips_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                tips_query,
                max_results=5,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"当地贴士搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的当地贴士"
                travel_logger.warning(error_msg)
                return error_msg

            tips = []
            for i, result in enumerate(results[:3], 1):
                title = result.get('title', '当地贴士')
                body = result.get('body', '无详细信息')[:200]
                
                tips.append(
                    f"• {title}\n"
                    f"  {body}...\n"
                )
                
                travel_logger.debug(f"当地贴士结果 {i}: {title[:50]}...")

            result_text = f"{destination}的当地贴士:\n" + "\n".join(tips)
            travel_logger.info(f"当地贴士搜索成功，返回 {len(tips)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索当地贴士时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

@tool
def search_budget_info(destination: str, duration: str = "") -> str:
    """
    搜索预算和费用信息

    这个工具专门用于搜索目的地的旅行预算、
    日常开销和费用估算信息。

    参数：
    - destination: 目的地名称
    - duration: 旅行时长（可选）

    返回：格式化的预算信息字符串
    """
    travel_logger.info(f"调用预算信息搜索工具 - 目的地: {destination}, 时长: {duration}")
    
    try:
        budget_query = f"{destination} 旅行预算 费用 日常开销 {duration} 花费"
        travel_logger.info(f"预算信息搜索查询: {budget_query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(
                budget_query,
                max_results=5,
                region="cn-zh",
                safesearch="moderate"
            ))

            travel_logger.info(f"预算信息搜索返回 {len(results)} 个结果")

            if not results:
                error_msg = f"未找到{destination}的预算信息"
                travel_logger.warning(error_msg)
                return error_msg

            budget_info = []
            for i, result in enumerate(results[:3], 1):
                title = result.get('title', '预算信息')
                body = result.get('body', '无详细信息')[:200]
                
                budget_info.append(
                    f"• {title}\n"
                    f"  {body}...\n"
                )
                
                travel_logger.debug(f"预算信息结果 {i}: {title[:50]}...")

            result_text = f"{destination}的预算信息:\n" + "\n".join(budget_info)
            travel_logger.info(f"预算信息搜索成功，返回 {len(budget_info)} 个格式化结果")
            return result_text
            
    except Exception as e:
        error_msg = f"搜索预算信息时出错: {str(e)}"
        travel_logger.error(error_msg)
        return error_msg

# List of all available tools
ALL_TOOLS = [
    search_destination_info,
    search_weather_info,
    search_attractions,
    search_hotels,
    search_restaurants,
    search_local_tips,
    search_budget_info
]
