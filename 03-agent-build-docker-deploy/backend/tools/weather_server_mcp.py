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
import logging
from pathlib import Path
import asyncio
import httpx
import os
from urllib.parse import urljoin
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from pathlib import Path
from pypinyin import lazy_pinyin, Style

# 加载 .env 文件中的环境变量
dotenv_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(dotenv_path)

# 初始化日志
def setup_weather_server_logger():
    ws_logger = logging.getLogger('weather_server')
    ws_logger.setLevel(logging.INFO)
    if not ws_logger.handlers:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        fh = logging.FileHandler('logs/backend.log', encoding='utf-8')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        ws_logger.addHandler(fh)
    return ws_logger

ws_logger = setup_weather_server_logger()

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
        ws_logger.error("QWEATHER_API_BASE 未正确配置，已跳过请求。")
        return None

    if not QWEATHER_API_KEY:
        ws_logger.error("QWEATHER_API_KEY 未设置，已跳过请求。")
        return None

    safe_endpoint = endpoint.lstrip("/")
    url = urljoin(_QWEATHER_BASE_URL, safe_endpoint)

    # 使用 Header 方式认证（和风天气的新版本API）
    headers = {
        "X-QW-Api-Key": QWEATHER_API_KEY
    }
    
    async with httpx.AsyncClient() as client:
        try:
            ws_logger.info(f"QWeather请求: url={url}, params={params}")
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            ws_logger.info(f"QWeather响应状态: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            ws_logger.info(f"QWeather响应内容大小: {len(str(result))} 字符")
            return result
        except httpx.HTTPStatusError as e:
            ws_logger.error(f"HTTP 状态错误: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            ws_logger.error(f"API 请求错误: {type(e).__name__}: {e}")
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
        location (str): 位置信息，支持以下格式：
                       - 中文城市名（如"北京"、"西宁"等，会自动转换为拼音再查找城市ID）
                       - 城市拼音（如"xining"表示西宁，会自动转换为城市ID）
                       - 城市ID（如"101010100"表示北京）  
                       - 经纬度坐标（如"116.41,39.92"）
        
    返回:
        格式化的预警信息字符串
    """
    # 解析 location 为城市ID或经纬度
    async def _resolve_location(raw: Union[str, int]) -> str:
        text = str(raw).strip()
        # 经纬度直接透传
        if "," in text:
            ws_logger.info(f"[预警]检测到经纬度，直接使用: {text}")
            return text
        # 数字ID直接透传
        if text.isdigit():
            ws_logger.info(f"[预警]检测到城市ID，直接使用: {text}")
            return text
        # 中文 → 拼音
        if any('\u4e00' <= ch <= '\u9fff' for ch in text):
            py = _convert_chinese_to_pinyin(text)
            ws_logger.info(f"[预警]中文转拼音: {text} → {py}")
            lookup = await make_qweather_request("geo/v2/city/lookup", {"location": py, "lang": "zh"})
        # 拼音
        elif text.isalpha() and text.islower():
            py = text
            ws_logger.info(f"[预警]检测到拼音，开始查找: {py}")
            lookup = await make_qweather_request("geo/v2/city/lookup", {"location": py, "lang": "zh"})
        else:
            ws_logger.info(f"[预警]未识别的格式，原样使用: {text}")
            return text

        if not lookup or lookup.get("code") != "200":
            ws_logger.warning(f"[预警]城市查找失败，回退原值: {text}")
            return text
        locations = lookup.get("location", [])
        if not locations:
            ws_logger.info(f"[预警]无匹配结果，回退原值: {text}")
            return text
        chosen = next((loc for loc in locations if loc.get("type") == "city"), locations[0])
        city_id = chosen.get("id") or text
        ws_logger.info(f"[预警]解析完成: {text} → {city_id}")
        return city_id

    resolved = await _resolve_location(location)

    params = {
        "location": resolved,
        "lang": "zh"
    }
    
    ws_logger.info(f"调用 get_weather_warning | params={params}")
    data = await make_qweather_request("v7/warning/now", params)
    
    if not data:
        ws_logger.warning("get_weather_warning 返回空或失败")
        return "无法获取预警信息或API请求失败。"
    
    if data.get("code") != "200":
        ws_logger.error(f"get_weather_warning API错误: {data.get('code')}")
        return f"API 返回错误: {data.get('code')}"
    
    warnings = data.get("warning", [])
    
    if not warnings:
        ws_logger.info(f"get_weather_warning 无活动预警 | location={location}")
        return f"当前位置 {location} 没有活动预警。"
    
    formatted_warnings = [format_warning(warning) for warning in warnings]
    joined = "\n---\n".join(formatted_warnings)
    ws_logger.info(f"get_weather_warning 返回长度: {len(joined)} 字符")
    return joined

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
        location (str): 位置信息，支持以下格式：
                       - 中文城市名（如"北京"、"西宁"等，会自动转换为拼音再查找城市ID）
                       - 城市拼音（如"xining"表示西宁，会自动转换为城市ID）
                       - 城市ID（如"101010100"表示北京）  
                       - 经纬度坐标（如"116.41,39.92"）
        days (int): 预报天数，可选值为 3、7、10、15、30，默认为 3
        
    返回:
        格式化的天气预报字符串
    """
    # 解析 location 为城市ID或经纬度
    async def _resolve_location(raw: Union[str, int]) -> str:
        text = str(raw).strip()
        if "," in text:
            ws_logger.info(f"[预报]检测到经纬度，直接使用: {text}")
            return text
        if text.isdigit():
            ws_logger.info(f"[预报]检测到城市ID，直接使用: {text}")
            return text
        if any('\u4e00' <= ch <= '\u9fff' for ch in text):
            py = _convert_chinese_to_pinyin(text)
            ws_logger.info(f"[预报]中文转拼音: {text} → {py}")
            lookup = await make_qweather_request("geo/v2/city/lookup", {"location": py, "lang": "zh"})
        elif text.isalpha() and text.islower():
            py = text
            ws_logger.info(f"[预报]检测到拼音，开始查找: {py}")
            lookup = await make_qweather_request("geo/v2/city/lookup", {"location": py, "lang": "zh"})
        else:
            ws_logger.info(f"[预报]未识别的格式，原样使用: {text}")
            return text

        if not lookup or lookup.get("code") != "200":
            ws_logger.warning(f"[预报]城市查找失败，回退原值: {text}")
            return text
        locations = lookup.get("location", [])
        if not locations:
            ws_logger.info(f"[预报]无匹配结果，回退原值: {text}")
            return text
        chosen = next((loc for loc in locations if loc.get("type") == "city"), locations[0])
        city_id = chosen.get("id") or text
        ws_logger.info(f"[预报]解析完成: {text} → {city_id}")
        return city_id

    resolved = await _resolve_location(location)
    
    # 确保 days 参数有效
    valid_days = [3, 7, 10, 15, 30]
    if days not in valid_days:
        days = 3  # 默认使用3天预报
    
    params = {
        "location": resolved,
        "lang": "zh"
    }
    # 和风天气API文档 https://dev.qweather.com/docs/api/weather/weather-daily-forecast/
    endpoint = f"v7/weather/{days}d"
    ws_logger.info(f"调用 get_daily_forecast | endpoint={endpoint}, params={params}")
    data = await make_qweather_request(endpoint, params)
    
    if not data:
        ws_logger.warning("get_daily_forecast 返回空或失败")
        return "无法获取天气预报或API请求失败。"
    
    if data.get("code") != "200":
        ws_logger.error(f"get_daily_forecast API错误: {data.get('code')}")
        return f"API 返回错误: {data.get('code')}"
    
    daily_forecasts = data.get("daily", [])
    
    if not daily_forecasts:
        ws_logger.warning(f"get_daily_forecast 无数据 | location={location}")
        return f"无法获取 {location} 的天气预报数据。"
    
    formatted_forecasts = [format_daily_forecast(daily) for daily in daily_forecasts]
    joined = "\n---\n".join(formatted_forecasts)
    ws_logger.info(f"get_daily_forecast 返回长度: {len(joined)} 字符")
    return joined


def _convert_chinese_to_pinyin(chinese_text: str) -> str:
    """
    将中文城市名转换为拼音（全拼）
    
    Args:
        chinese_text: 中文城市名，如 "西宁"
        
    Returns:
        str: 拼音全拼，如 "xining"
    """
    try:
        # 使用 pypinyin 将中文转换为拼音
        pinyin_list = lazy_pinyin(chinese_text, style=Style.NORMAL)
        pinyin = ''.join(pinyin_list)
        ws_logger.info(f"中文转拼音: {chinese_text} → {pinyin}")
        return pinyin
    except Exception as e:
        ws_logger.error(f"中文转拼音失败: {chinese_text} - {str(e)}")
        return chinese_text  # 转换失败时返回原文本


async def lookup_city_id_by_pinyin(pinyin: str) -> str:
    """
    根据城市名称的拼音（全拼）查找城市ID。

    参数:
        pinyin: 城市名称的拼音（全拼），如 "xining"

    返回:
        若成功，返回匹配城市对象的精简 JSON 字符串（包含 name、id、lat、lon、adm1 等字段）；
        若失败或未找到，返回说明文本。
    """
    params = {
        "location": pinyin,
        "lang": "zh"
    }

    endpoint = "geo/v2/city/lookup"
    ws_logger.info(f"调用 [查找城市ID]| endpoint={endpoint}, params={params}")
    data = await make_qweather_request(endpoint, params)

    if not data:
        ws_logger.warning("[查找城市ID]返回空或失败")
        return "无法查询城市ID或API请求失败。"

    if data.get("code") != "200":
        ws_logger.error(f"[查找城市ID]API错误: {data.get('code')}")
        return f"API 返回错误: {data.get('code')}"

    locations = data.get("location", [])
    if not locations:
        ws_logger.info(f"[查找城市ID]无匹配结果 | pinyin={pinyin}")
        return f"未找到与 {pinyin} 匹配的城市。"

    # 优先选择 type == "city" 的主城市，否则回退第一个
    chosen = None
    for loc in locations:
        if loc.get("type") == "city":
            chosen = loc
            break
    if chosen is None:
        chosen = locations[0]

    # 仅返回常用字段，避免冗余
    result = {
        "name": chosen.get("name"),
        "id": chosen.get("id"),
        "lat": chosen.get("lat"),
        "lon": chosen.get("lon"),
        "adm2": chosen.get("adm2"),
        "adm1": chosen.get("adm1"),
        "country": chosen.get("country"),
        "type": chosen.get("type"),
        "rank": chosen.get("rank"),
        "fxLink": chosen.get("fxLink"),
    }

    ws_logger.info(
        f"[查找城市ID]命中: name={result['name']}, id={result['id']}"
    )

    # 以紧凑 JSON 字符串形式返回
    try:
        import json as _json
        return _json.dumps(result, ensure_ascii=False)
    except Exception:
        # 兜底为可读字符串
        return f"{result}"

if __name__ == "__main__":
    ws_logger.info("正在启动 MCP 天气服务器…")
    ws_logger.info("提供工具: get_weather_warning, get_daily_forecast")
    ws_logger.info("请确保环境变量 QWEATHER_API_KEY 已设置")
    ws_logger.info("使用 Ctrl+C 停止服务器")
    
    # 初始化并运行服务器
    mcp.run(transport='stdio') 
