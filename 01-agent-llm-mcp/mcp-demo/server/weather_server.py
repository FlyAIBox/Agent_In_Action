#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP 服务器可以提供三种主要类型的功能：

资源：客户端可以读取的类似文件的数据（例如 API 响应或文件内容）
工具：可由 LLM 调用的函数（经用户批准）
提示：预先编写的模板，帮助用户完成特定任务

######################################

MCP 天气服务器

提供两个工具：
1. get_weather_warning: 获取指定城市ID或经纬度的天气灾害预警
2. get_daily_forecast: 获取指定城市ID或经纬度的天气预报

Author: FlyAIBox
Date: 2025.10.11
"""

from typing import Any, Dict, List, Optional, Union
import asyncio
import httpx
import os
from urllib.parse import urljoin
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pathlib import Path

# 加载 .env 文件中的环境变量
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)

# 初始化 FastMCP 服务器
mcp = FastMCP("weather",  # 服务器名称
              debug=True,  # 启用调试模式，会输出详细日志
              host="0.0.0.0") # 监听所有网络接口，允许远程连接

# 从环境变量中读取常量
QWEATHER_API_BASE = os.getenv("QWEATHER_API_BASE")
QWEATHER_API_KEY = os.getenv("QWEATHER_API_KEY")

def _normalize_base_url(raw_base: Optional[str]) -> str:
    """
    确保基础 URL 包含协议并以单个斜杠结尾，兼容 .env 中未写协议的情况
    """
    if not raw_base:
        raise RuntimeError("未配置 QWEATHER_API_BASE 环境变量")

    base = raw_base.strip()
    if not base.startswith(("http://", "https://")):
        base = f"https://{base.lstrip('/')}"

    # urljoin 要求目录风格以斜杠结尾，避免 'v7/weather/7d' 被覆盖
    if not base.endswith("/"):
        base = f"{base}/"

    return base

try:
    _QWEATHER_BASE_URL = _normalize_base_url(QWEATHER_API_BASE)
except RuntimeError as err:
    print(f"[配置错误] {err}")
    _QWEATHER_BASE_URL = None

async def make_qweather_request(endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    向和风天气 API 发送请求
    
    参数:
        endpoint: API 端点路径（不包含基础 URL）
        params: API 请求的参数
        
    返回:
        成功时返回 JSON 响应，失败时返回 None
    """
    if not _QWEATHER_BASE_URL:
        print("QWEATHER_API_BASE 未正确配置，已跳过请求。")
        return None

    if not QWEATHER_API_KEY:
        print("QWEATHER_API_KEY 未设置，已跳过请求。")
        return None

    safe_endpoint = endpoint.lstrip("/")
    url = urljoin(_QWEATHER_BASE_URL, safe_endpoint)

    # 使用 Header 方式认证（和风天气的新版本API）
    headers = {
        "X-QW-Api-Key": QWEATHER_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            print(f"请求 URL: {url}")
            print(f"请求参数: {params}")
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            print(f"响应状态码: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            print(f"响应内容: {result}")
            return result
        except httpx.HTTPStatusError as e:
            print(f"HTTP 状态错误: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"API 请求错误: {type(e).__name__}: {e}")
            return None

def format_warning(warning: Dict[str, Any]) -> str:
    """
    将天气预警数据格式化为可读字符串
    
    参数:
        warning: 天气预警数据对象
        
    返回:
        格式化后的预警信息
    """
    return f"""
预警ID: {warning.get('id', '未知')}
标题: {warning.get('title', '未知')}
发布时间: {warning.get('pubTime', '未知')}
开始时间: {warning.get('startTime', '未知')}
结束时间: {warning.get('endTime', '未知')}
预警类型: {warning.get('typeName', '未知')}
预警等级: {warning.get('severity', '未知')} ({warning.get('severityColor', '未知')})
发布单位: {warning.get('sender', '未知')}
状态: {warning.get('status', '未知')}
详细信息: {warning.get('text', '无详细信息')}
"""

@mcp.tool()
async def get_weather_warning(location: Union[str, int]) -> str:
    """
    获取指定位置的天气灾害预警
    
    参数:
        location: 城市ID或经纬度坐标（经度,纬度）
                例如：'101010100'（北京）或 '116.41,39.92'
                也可以直接传入数字ID，如 101010100
        
    返回:
        格式化的预警信息字符串
    """
    # 确保 location 为字符串类型
    location = str(location)
    
    params = {
        "location": location,
        "lang": "zh"
    }
    
    data = await make_qweather_request("v7/warning/now", params)
    
    if not data:
        return "无法获取预警信息或API请求失败。"
    
    if data.get("code") != "200":
        return f"API 返回错误: {data.get('code')}"
    
    warnings = data.get("warning", [])
    
    if not warnings:
        return f"当前位置 {location} 没有活动预警。"
    
    formatted_warnings = [format_warning(warning) for warning in warnings]
    return "\n---\n".join(formatted_warnings)

def format_daily_forecast(daily: Dict[str, Any]) -> str:
    """
    将天气预报数据格式化为可读字符串
    
    参数:
        daily: 天气预报数据对象
        
    返回:
        格式化后的预报信息
    """
    return f"""
日期: {daily.get('fxDate', '未知')}
日出: {daily.get('sunrise', '未知')}  日落: {daily.get('sunset', '未知')}
最高温度: {daily.get('tempMax', '未知')}°C  最低温度: {daily.get('tempMin', '未知')}°C
白天天气: {daily.get('textDay', '未知')}  夜间天气: {daily.get('textNight', '未知')}
白天风向: {daily.get('windDirDay', '未知')} {daily.get('windScaleDay', '未知')}级 ({daily.get('windSpeedDay', '未知')}km/h)
夜间风向: {daily.get('windDirNight', '未知')} {daily.get('windScaleNight', '未知')}级 ({daily.get('windSpeedNight', '未知')}km/h)
相对湿度: {daily.get('humidity', '未知')}%
降水量: {daily.get('precip', '未知')}mm
紫外线指数: {daily.get('uvIndex', '未知')}
能见度: {daily.get('vis', '未知')}km
"""

@mcp.tool()
async def get_daily_forecast(location: Union[str, int], days: int = 3) -> str:
    """
    获取指定位置的天气预报
    
    参数:
        location: 城市ID或经纬度坐标（经度,纬度）
                例如：'101010100'（北京）或 '116.41,39.92'
                也可以直接传入数字ID，如 101010100
        days: 预报天数，可选值为 3、7、10、15、30，默认为 3
        
    返回:
        格式化的天气预报字符串
    """
    # 确保 location 为字符串类型
    location = str(location)
    
    # 确保 days 参数有效
    valid_days = [3, 7, 10, 15, 30]
    if days not in valid_days:
        days = 3  # 默认使用3天预报
    
    params = {
        "location": location,
        "lang": "zh"
    }
    # 和风天气API文档 https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
    endpoint = f"v7/weather/{days}d"
    data = await make_qweather_request(endpoint, params)
    
    if not data:
        return "无法获取天气预报或API请求失败。"
    
    if data.get("code") != "200":
        return f"API 返回错误: {data.get('code')}"
    
    daily_forecasts = data.get("daily", [])
    
    if not daily_forecasts:
        return f"无法获取 {location} 的天气预报数据。"
    
    formatted_forecasts = [format_daily_forecast(daily) for daily in daily_forecasts]
    return "\n---\n".join(formatted_forecasts)

if __name__ == "__main__":
    print("正在启动 MCP 天气服务器...")
    print("提供工具: get_weather_warning, get_daily_forecast")
    print("请确保环境变量 QWEATHER_API_KEY 已设置")
    print("使用 Ctrl+C 停止服务器")
    
    # 初始化并运行服务器
    mcp.run(transport='stdio') 
