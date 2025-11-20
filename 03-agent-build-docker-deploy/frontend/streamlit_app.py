#!/usr/bin/env python3
"""
AI旅行规划智能体 - Streamlit前端

这个模块提供基于Streamlit的Web前端界面，用户可以通过浏览器
与LangGraph多智能体旅行规划系统进行交互。

主要功能：
1. 用户友好的旅行规划表单
2. 实时显示规划进度
3. 展示多智能体协作结果
4. 下载规划报告
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="旅小智 - 您的智能旅行规划助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
def inject_custom_css():
    """注入自定义CSS样式"""
    st.markdown("""
    <style>
    /* 主背景 - 使用浅色渐变 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        background-attachment: fixed;
    }
    
    /* 自然风光背景图层（更淡的透明度） */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920');
        background-size: cover;
        background-position: center;
        opacity: 0.08;
        z-index: 0;
        pointer-events: none;
    }
    
    /* 主内容区域 */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        position: relative;
        z-index: 1;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    
    /* 侧边栏样式 - 更浅的背景 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.55) 0%, rgba(118, 75, 162, 0.55) 100%);
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    /* 侧边栏标签文字 - 更大字体 */
    section[data-testid="stSidebar"] label {
        color: white !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        line-height: 1.6;
    }
    
    /* 侧边栏输入框样式 - 更大字体 */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select {
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
        border-radius: 10px;
        font-size: 1.2rem !important;
        padding: 0.7rem !important;
        font-weight: 500;
    }
    
    /* 侧边栏数字输入框 */
    section[data-testid="stSidebar"] input[type="number"] {
        font-size: 1.2rem !important;
    }
    
    /* 侧边栏选择框选项 */
    section[data-testid="stSidebar"] select option {
        font-size: 1.1rem !important;
    }
    
    /* 侧边栏checkbox标签 */
    section[data-testid="stSidebar"] .stCheckbox label {
        font-size: 1.1rem !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.15);
    }
    
    /* 侧边栏所有文本 */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        font-size: 1.1rem !important;
    }
    
    /* 侧边栏help文本 */
    section[data-testid="stSidebar"] small {
        font-size: 1rem !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* 侧边栏按钮 - 更大字体 */
    section[data-testid="stSidebar"] .stButton > button {
        background: white !important;
        color: #667eea !important;
        font-weight: 700;
        font-size: 1.3rem !important;
        padding: 0.9rem 1.8rem !important;
        border-radius: 12px;
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #764ba2 !important;
        transform: translateY(-2px);
    }
    
    /* 标题样式 */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 1rem;
    }
    
    /* 主内容区标题 - 使用深色提高对比度 */
    .main h2 {
        color: #2d3748 !important;
        font-weight: 700;
    }
    
    .main h3 {
        color: #4a5568 !important;
        font-weight: 600;
    }
    
    /* Hero区域标题保持渐变色 */
    .hero-section h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* 卡片样式 */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    /* 图片画廊样式 */
    .gallery-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .gallery-item {
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        height: 200px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .gallery-item:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .gallery-item img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .gallery-caption {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
        color: white;
        padding: 1rem;
        font-weight: 600;
    }
    
    /* 成功/错误消息样式 */
    .stSuccess {
        background-color: rgba(40, 167, 69, 0.1);
        border-left: 4px solid #28a745;
        border-radius: 8px;
    }
    
    .stError {
        background-color: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #dc3545;
        border-radius: 8px;
    }
    
    /* 进度条样式 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 输入框焦点样式 */
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* 页脚样式 */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        font-size: 0.9rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* 旅小智AI形象样式 - 超大超可爱 */
    .ai-avatar {
        font-size: 8rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: float 3s ease-in-out infinite, wobble 4s ease-in-out infinite;
        filter: drop-shadow(0 6px 12px rgba(102, 126, 234, 0.4));
        transform-origin: center;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-15px) rotate(-5deg); }
        50% { transform: translateY(-20px) rotate(0deg); }
        75% { transform: translateY(-15px) rotate(5deg); }
    }
    
    @keyframes wobble {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(-3deg); }
        75% { transform: rotate(3deg); }
    }
    
    /* 侧边栏旅小智logo - 超大超萌 */
    .sidebar-logo {
        font-size: 5rem !important;
        animation: pulse 2s ease-in-out infinite;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
        display: inline-block;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }
    
    /* 自然语言输入框样式 */
    .chat-input-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        border: 2px solid rgba(102, 126, 234, 0.2);
        margin: 2rem 0;
        transition: all 0.3s ease;
    }
    
    .chat-input-container:hover {
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .chat-input-container input,
    .chat-input-container textarea {
        border: none !important;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .chat-input-container input:focus,
    .chat-input-container textarea:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* 增强textarea样式 */
    .stTextArea textarea {
        font-size: 1.2rem !important;
        line-height: 1.8 !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #999 !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* 快捷示例按钮 */
    .example-chips {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        justify-content: center;
        margin: 2rem 0 3rem 0;
    }
    
    .example-chip {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    .example-chip:hover {
        background: rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Hero区域样式 */
    .hero-section {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #4a5568;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# API基础URL
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://192.168.172.128:8080")

def check_api_health():
    """检查API服务状态"""
    try:
        # 增加超时时间到15秒
        response = requests.get(f"{API_BASE_URL}/health", timeout=15)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, {"error": f"API服务返回错误状态: {response.status_code}"}
    except requests.exceptions.Timeout:
        return False, {"error": "API请求超时，后端服务可能正在启动中，请稍等片刻后刷新页面"}
    except requests.exceptions.ConnectionError:
        return False, {"error": "无法连接到API服务器，请确保后端服务已启动 (运行: ./start_backend.sh)"}
    except Exception as e:
        return False, {"error": f"连接错误: {str(e)}"}

def create_travel_plan(travel_data: Dict[str, Any]) -> Optional[str]:
    """创建旅行规划任务"""
    try:
        # 增加超时时间到60秒
        response = requests.post(f"{API_BASE_URL}/plan", json=travel_data, timeout=60)
        if response.status_code == 200:
            return response.json()["task_id"]
        else:
            st.error(f"创建任务失败: {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("创建任务超时，请稍后重试")
        return None
    except requests.exceptions.ConnectionError:
        st.error("无法连接到API服务器，请确保后端服务已启动")
        return None
    except Exception as e:
        st.error(f"API请求失败: {str(e)}")
        return None

def get_planning_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划状态"""
    max_retries = 3
    for retry in range(max_retries):
        try:
            # 增加超时时间到15秒
            response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                st.error("任务不存在")
                return None
            else:
                st.warning(f"状态查询返回 {response.status_code}，正在重试...")
                continue
        except requests.exceptions.Timeout:
            if retry < max_retries - 1:
                st.warning(f"状态查询超时，正在重试 ({retry + 1}/{max_retries})...")
                time.sleep(2)  # 等待2秒后重试
                continue
            else:
                st.warning("状态查询超时，但任务可能仍在处理中...")
                return None
        except requests.exceptions.ConnectionError:
            st.error("无法连接到API服务器，请确保后端服务已启动")
            return None
        except Exception as e:
            if retry < max_retries - 1:
                st.warning(f"状态查询失败，正在重试: {str(e)}")
                time.sleep(1)
                continue
            else:
                st.error(f"获取状态失败: {str(e)}")
                return None
    return None

def display_header():
    """显示页面标题"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🌍 AI旅行规划智能体</h1>
        <p style="font-size: 1.2rem; color: #666;">
            🤖 由OpenAI兼容大模型（ChatOpenAI）和DuckDuckGo搜索驱动的智能旅行规划系统
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_agent_info():
    """显示智能体团队信息"""
    st.markdown("### 🎯 AI智能体团队")
    
    agents = [
        ("🎯", "协调员智能体", "工作流编排与决策综合"),
        ("✈️", "旅行顾问", "目的地专业知识与实时搜索"),
        ("💰", "预算优化师", "成本分析与实时定价"),
        ("🌤️", "天气分析师", "天气情报与当前数据"),
        ("🏠", "当地专家", "内部知识与实时本地信息"),
        ("📅", "行程规划师", "日程优化与物流安排")
    ]
    
    cols = st.columns(3)
    for i, (icon, name, desc) in enumerate(agents):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                <h4>{icon} {name}</h4>
                <p style="font-size: 0.9rem; color: #666;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def create_travel_form():
    """创建旅行规划表单"""
    st.markdown("### 📋 旅行规划表单")
    
    with st.form("travel_planning_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📍 基本信息")
            destination = st.text_input(
                "目的地城市",
                placeholder="例如: 北京, 上海, 成都...",
                help="请输入您想要前往的城市名称"
            )
            
            start_date = st.date_input(
                "开始日期",
                value=date.today() + timedelta(days=7),
                min_value=date.today()
            )
            
            end_date = st.date_input(
                "结束日期",
                value=date.today() + timedelta(days=14),
                min_value=start_date if 'start_date' in locals() else date.today()
            )
            
            group_size = st.number_input(
                "旅行人数",
                min_value=1,
                max_value=20,
                value=2,
                help="包括您自己在内的总人数"
            )
            
        with col2:
            st.markdown("#### 💰 预算与偏好")
            budget_range = st.selectbox(
                "预算范围",
                ["经济型", "中等预算", "豪华型"],
                help="选择适合您的预算类型"
            )
            
            currency = st.selectbox(
                "货币类型",
                ["CNY", "USD", "EUR", "GBP", "JPY", "CAD", "AUD"],
                help="选择您偏好的货币单位"
            )
            
            activity_level = st.selectbox(
                "活动强度",
                ["轻松", "适中", "活跃"],
                index=1,
                help="选择您偏好的旅行节奏"
            )
            
            travel_style = st.selectbox(
                "旅行风格",
                ["观光客", "探索者", "当地人"],
                index=1,
                help="选择您的旅行体验偏好"
            )
        
        st.markdown("#### 🎯 兴趣爱好")
        interests = st.multiselect(
            "选择您的兴趣爱好",
            ["历史", "文化", "美食", "艺术", "自然风光", "购物", "夜生活", 
             "博物馆", "建筑", "摄影", "音乐", "体育", "冒险活动"],
            default=["历史", "美食"],
            help="选择您感兴趣的活动类型"
        )
        
        col3, col4 = st.columns(2)
        with col3:
            dietary_restrictions = st.text_input(
                "饮食限制/偏好",
                placeholder="例如: 素食, 清真, 无麸质...",
                help="如有特殊饮食要求请填写"
            )
            
            transportation_preference = st.selectbox(
                "交通偏好",
                ["公共交通", "混合交通", "私人交通"],
                help="选择您偏好的交通方式"
            )
            
        with col4:
            accommodation_preference = st.text_input(
                "住宿偏好",
                placeholder="例如: 酒店, 民宿, 青旅...",
                help="描述您偏好的住宿类型"
            )
            
            special_requirements = st.text_area(
                "特殊要求",
                placeholder="其他特殊需求或要求...",
                help="任何其他需要考虑的特殊要求"
            )
        
        submitted = st.form_submit_button("🚀 开始AI智能规划", use_container_width=True)
        
        if submitted:
            # 验证输入
            if not destination:
                st.error("请输入目的地城市")
                return None
                
            if start_date >= end_date:
                st.error("结束日期必须晚于开始日期")
                return None
            
            # 构建请求数据
            travel_data = {
                "destination": destination,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "budget_range": budget_range,
                "group_size": group_size,
                "interests": interests,
                "dietary_restrictions": dietary_restrictions,
                "activity_level": activity_level,
                "travel_style": travel_style,
                "transportation_preference": transportation_preference,
                "accommodation_preference": accommodation_preference,
                "special_requirements": special_requirements,
                "currency": currency
            }
            
            return travel_data
    
    return None

def display_planning_progress(task_id: str):
    """显示规划进度"""
    st.markdown("### 🔄 规划进度")

    progress_container = st.container()
    status_container = st.container()
    debug_container = st.container()

    # 创建进度条和状态显示
    progress_bar = progress_container.progress(0)
    status_text = status_container.empty()
    debug_text = debug_container.empty()
    
    # 轮询状态更新
    max_attempts = 360  # 最多等待6分钟（每秒轮询一次）
    attempt = 0
    
    last_known_status = None
    consecutive_failures = 0

    while attempt < max_attempts:
        status = get_planning_status(task_id)

        if status:
            # 重置失败计数
            consecutive_failures = 0
            last_known_status = status

            progress = status.get("progress", 0)
            current_status = status.get("status", "unknown")
            message = status.get("message", "处理中...")
            current_agent = status.get("current_agent", "")

            # 更新进度条
            progress_bar.progress(progress / 100)

            # 更新状态文本
            status_text.markdown(f"""
            **状态**: {current_status}
            **当前智能体**: {current_agent}
            **消息**: {message}
            **进度**: {progress}%
            """)

            # 检查是否完成
            if current_status == "completed":
                st.success("🎉 旅行规划完成！")
                return status.get("result")
            elif current_status == "failed":
                st.error(f"❌ 规划失败: {message}")
                return None

        else:
            # 状态查询失败，但继续尝试
            consecutive_failures += 1
            if last_known_status:
                # 显示最后已知状态
                progress = last_known_status.get("progress", 0)
                current_status = last_known_status.get("status", "unknown")
                message = f"连接中断，正在重试... (失败次数: {consecutive_failures})"
                current_agent = last_known_status.get("current_agent", "")

                status_text.markdown(f"""
                **状态**: {current_status} (连接中断)
                **当前智能体**: {current_agent}
                **消息**: {message}
                **进度**: {progress}%
                """)

            # 如果连续失败太多次，提示用户
            if consecutive_failures >= 10:
                st.warning("⚠️ 网络连接不稳定，但任务可能仍在后台处理中...")

        # 显示调试信息
        debug_text.markdown(f"""
        <details>
        <summary>🔍 调试信息</summary>

        - **任务ID**: {task_id}
        - **尝试次数**: {attempt + 1}/{max_attempts}
        - **连续失败**: {consecutive_failures}
        - **API地址**: {API_BASE_URL}
        - **当前时间**: {time.strftime('%H:%M:%S')}
        </details>
        """, unsafe_allow_html=True)

        time.sleep(1)
        attempt += 1
    
    # 超时后提供手动检查选项
    st.warning("⏰ 自动监控已超时，但任务可能仍在处理中")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 手动检查状态"):
            final_status = get_planning_status(task_id)
            if final_status:
                if final_status.get("status") == "completed":
                    st.success("🎉 任务已完成！")
                    return final_status.get("result")
                else:
                    st.info(f"任务状态: {final_status.get('status')} - {final_status.get('message')}")
            else:
                st.error("无法获取任务状态")

    with col2:
        if st.button("📥 尝试下载结果"):
            try:
                download_url = f"{API_BASE_URL}/download/{task_id}"
                response = requests.get(download_url, timeout=10)
                if response.status_code == 200:
                    st.success("✅ 结果文件可用")
                    st.download_button(
                        label="下载规划结果",
                        data=response.content,
                        file_name=f"travel_plan_{task_id[:8]}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("结果文件暂不可用")
            except Exception as e:
                st.error(f"下载失败: {str(e)}")

    return None

def generate_markdown_report(result: Dict[str, Any], task_id: str) -> str:
    """生成Markdown格式的旅行规划报告"""
    if not result:
        return "# 旅行规划报告\n\n无可用数据"

    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})

    # 获取基本信息
    destination = travel_plan.get("destination", "未知")
    duration = travel_plan.get("duration", 0)
    group_size = travel_plan.get("group_size", 0)
    budget_range = travel_plan.get("budget_range", "未知")
    interests = travel_plan.get("interests", [])
    travel_dates = travel_plan.get("travel_dates", "未知")

    # 生成Markdown内容
    markdown_content = f"""# 🌍 {destination}旅行规划报告

## 📋 规划概览

| 项目 | 详情 |
|------|------|
| 🎯 目的地 | {destination} |
| 📅 旅行时间 | {travel_dates} |
| ⏰ 行程天数 | {duration}天 |
| 👥 团队人数 | {group_size}人 |
| 💰 预算类型 | {budget_range} |
| 🎨 兴趣爱好 | {', '.join(interests) if interests else '无特殊偏好'} |

---

## 🤖 AI智能体专业建议

"""

    # 智能体名称映射
    agent_names_cn = {
        'travel_advisor': '🏛️ 旅行顾问',
        'weather_analyst': '🌤️ 天气分析师',
        'budget_optimizer': '💰 预算优化师',
        'local_expert': '🏠 当地专家',
        'itinerary_planner': '📅 行程规划师'
    }

    # 添加各智能体的建议
    for agent_name, output in agent_outputs.items():
        agent_display_name = agent_names_cn.get(agent_name, agent_name)
        status = output.get('status', '未知')
        response = output.get('response', '无输出')
        timestamp = output.get('timestamp', '')

        markdown_content += f"""### {agent_display_name}

**状态**: {status.upper()}
**完成时间**: {timestamp[:19] if timestamp else '未知'}

{response}

---

"""

    # 添加生成信息
    from datetime import datetime
    markdown_content += f"""## 📄 报告信息

- **任务ID**: `{task_id}`
- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **生成方式**: LangGraph多智能体AI系统
- **报告格式**: Markdown

---

*本报告由AI旅行规划智能体自动生成*
"""

    return markdown_content



def get_planning_status(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划状态"""
    max_retries = 2  # 减少重试次数，避免过长等待
    for retry in range(max_retries):
        try:
            # 增加超时时间到30秒
            response = requests.get(f"{API_BASE_URL}/status/{task_id}", timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                st.warning(f"任务 {task_id} 不存在")
                return None
            else:
                if retry < max_retries - 1:
                    st.warning(f"获取状态失败: HTTP {response.status_code}，正在重试...")
                    time.sleep(3)
                else:
                    st.error(f"获取状态失败: HTTP {response.status_code}")
                    return None
        except requests.exceptions.Timeout:
            if retry < max_retries - 1:
                # st.warning(f"任务执行中 ({retry + 1}/{max_retries})...")
                time.sleep(3)
            else:
                st.warning("⏰ 后端正在处理中，请稍后手动刷新页面查看结果")
                return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 无法连接到后端服务，请确保后端服务已启动")
            return None
        except Exception as e:
            if retry < max_retries - 1:
                st.warning(f"请求失败，正在重试 ({retry + 1}/{max_retries}): {str(e)}")
                time.sleep(3)
            else:
                st.error(f"获取状态失败: {str(e)}")
                return None
    return None

def get_planning_result(task_id: str) -> Optional[Dict[str, Any]]:
    """获取规划结果 - 从状态查询中获取结果"""
    try:
        # 从状态查询中获取结果
        status_info = get_planning_status(task_id)
        if status_info and status_info.get("result"):
            return status_info["result"]
        else:
            st.warning("结果尚未准备好或任务未完成")
            return None
    except Exception as e:
        st.error(f"获取结果失败: {str(e)}")
        return None

def save_report_to_results(content: str, filename: str) -> str:
    """保存Markdown报告到results目录"""
    import os

    # 确保results目录存在
    results_dir = "../results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # 生成完整文件路径
    file_path = os.path.join(results_dir, filename)

    try:
        # 保存markdown文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    except Exception as e:
        st.error(f"保存文件失败: {str(e)}")
        return None

def display_hero_section():
    """显示Hero区域 - 旅小智"""
    st.markdown("""
    <div class="hero-section">
        <div class="ai-avatar"><img src="https://raw.githubusercontent.com/FlyAIBox/Agent_In_Action/main/03-agent-build-docker-deploy/frontend/logo.png" alt="Agent in Action Logo" width="500"></div>
        <h1 class="hero-title">旅小智 - 您的智能旅行规划助手</h1>
        <p class="hero-subtitle">
            只需一句话，AI多智能体团队为您规划完美旅程<br/>
            从预算优化到行程安排，让旅行变得更简单
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_chat_interface():
    """显示自然语言交互界面"""
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown("## 💬 告诉旅小智你的旅行想法")
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # 创建输入框（使用text_area提供更大的输入区域）
    user_input = st.text_area(
        "自然语言输入",
        placeholder="例如：我想下周去北京玩3天，预算3000元，喜欢历史文化...\n\n您可以详细描述您的旅行需求，包括：\n- 目的地和时间\n- 预算范围\n- 同行人数\n- 兴趣偏好（美食、历史、自然风光等）",
        key="chat_input",
        height=400,
        label_visibility="collapsed",
        help="💡 用自然语言描述您的旅行需求，旅小智会自动为您规划"
    )
    
    # 快捷示例按钮
    st.markdown('<div class="example-chips">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    examples = [
        "北京3日游，历史文化",
        "杭州周末游，2人，预算中等",
        "成都美食之旅，5天",
        "上海亲子游，一家三口"
    ]
    
    clicked_example = None
    
    with col1:
        if st.button(examples[0], key="ex1", use_container_width=True):
            clicked_example = examples[0]
    with col2:
        if st.button(examples[1], key="ex2", use_container_width=True):
            clicked_example = examples[1]
    with col3:
        if st.button(examples[2], key="ex3", use_container_width=True):
            clicked_example = examples[2]
    with col4:
        if st.button(examples[3], key="ex4", use_container_width=True):
            clicked_example = examples[3]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 处理输入
    input_to_process = clicked_example if clicked_example else user_input
    
    if input_to_process:
        with st.spinner("🤖 旅小智正在理解您的需求..."):
            try:
                # 调用后端聊天接口
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"message": input_to_process},
                    timeout=30
                )
                
                if response.status_code == 200:
                    chat_response = response.json()
                    
                    # 显示旅小智的回复
                    st.markdown("### 🤖 旅小智回复")
                    st.info(chat_response["clarification"])
                    
                    # 如果可以直接创建任务
                    if chat_response["can_proceed"] and chat_response.get("task_id"):
                        task_id = chat_response["task_id"]
                        st.success(f"✅ 任务已创建！任务ID: {task_id}")
                        
                        # 保存任务ID到session state
                        st.session_state.current_task_id = task_id
                        st.session_state.planning_started = True
                        st.rerun()
                    
                    # 显示提取的信息
                    if chat_response["extracted_info"]:
                        with st.expander("📋 已识别的信息"):
                            for key, value in chat_response["extracted_info"].items():
                                st.write(f"**{key}**: {value}")
                    
                    # 显示缺失的信息
                    if chat_response["missing_info"]:
                        with st.expander("❓ 还需要补充的信息"):
                            for item in chat_response["missing_info"]:
                                st.write(f"- {item}")
                else:
                    st.error(f"请求失败: {response.status_code}")
                    
            except requests.exceptions.Timeout:
               st.info("⏰ 任务创建中... 请稍候...")
            except Exception as e:
                st.error(f"❌ 发生错误: {str(e)}")

def display_features_section():
    """显示功能特色区域"""
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown("## ✨ 为什么选择我们？")
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2 style="text-align: center; font-size: 3rem;">🤖</h2>
            <h3 style="text-align: center; color: #2d3748;">AI多智能体</h3>
            <p style="text-align: center; color: #666;">
                6个专业AI智能体协同工作，为您提供全方位的旅行规划服务
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 style="text-align: center; font-size: 3rem;">🎯</h2>
            <h3 style="text-align: center; color: #2d3748;">个性化定制</h3>
            <p style="text-align: center; color: #666;">
                根据您的兴趣、预算和偏好，量身定制专属旅行方案
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2 style="text-align: center; font-size: 3rem;">⚡</h2>
            <h3 style="text-align: center; color: #2d3748;">快速高效</h3>
            <p style="text-align: center; color: #666;">
                几分钟内完成专业旅行规划，节省您的宝贵时间
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h2 style="text-align: center; font-size: 3rem;">📄</h2>
            <h3 style="text-align: center; color: #2d3748;">专业报告</h3>
            <p style="text-align: center; color: #666;">
                生成详细的旅行规划报告，随时下载和分享
            </p>
        </div>
        """, unsafe_allow_html=True)

def display_world_gallery():
    """显示世界各地风光画廊"""
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown("## 🌏 探索世界之美")
    st.markdown("让AI带您发现世界各地的精彩")
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # 使用Unsplash的高质量旅行图片
    destinations = [
        {
            "name": "🗼 巴黎·浪漫之都",
            "url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=600&h=400&fit=crop",
        },
        {
            "name": "🗻 日本·富士山",
            "url": "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=600&h=400&fit=crop",
        },
        {
            "name": "🏰 希腊·圣托里尼",
            "url": "https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=600&h=400&fit=crop",
        },
        {
            "name": "🏔️ 瑞士·阿尔卑斯",
            "url": "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=600&h=400&fit=crop",
        },
        {
            "name": "🏖️ 马尔代夫·海岛",
            "url": "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=600&h=400&fit=crop",
        },
        {
            "name": "🌆 纽约·都市风光",
            "url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600&h=400&fit=crop",
        },
        {
            "name": "🏛️ 罗马·古城遗迹",
            "url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=600&h=400&fit=crop",
        },
        {
            "name": "🌴 巴厘岛·热带天堂",
            "url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600&h=400&fit=crop",
        },
    ]
    
    # 使用Streamlit原生列布局 - 第一行（4张图片）
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[0]['url']}" alt="{destinations[0]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[0]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[1]['url']}" alt="{destinations[1]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[1]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[2]['url']}" alt="{destinations[2]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[2]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[3]['url']}" alt="{destinations[3]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[3]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # 第二行（4张图片）
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[4]['url']}" alt="{destinations[4]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[4]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[5]['url']}" alt="{destinations[5]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[5]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col7:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[6]['url']}" alt="{destinations[6]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[6]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col8:
        st.markdown(f"""
        <div style="position: relative; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s ease;">
            <img src="{destinations[7]['url']}" alt="{destinations[7]['name']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); color: white; padding: 1rem; font-weight: 600; font-size: 0.9rem;">
                {destinations[7]['name']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_footer():
    """显示页脚"""
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    st.markdown("""
    <div class="footer">
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">
            🤖 <strong>旅小智</strong> - 您的智能旅行规划助手
        </p>
        <p style="color: #999;">
            由 <strong>LangGraph 多智能体系统</strong> 驱动 | 
            采用 <strong>OpenAI兼容大模型</strong> 和 <strong>DuckDuckGo实时搜索</strong>
        </p>
        <p style="color: #999; margin-top: 1rem;">
            © 2025 旅小智 Travel AI | 技术架构: FastAPI + Streamlit + LangGraph
        </p>
        <p style="color: #aaa; font-size: 0.85rem; margin-top: 0.5rem;">
            💡 支持自然语言和表单交互 
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_planning_result(result: Dict[str, Any]):
    """显示规划结果"""
    if not result:
        return

    st.markdown("### 📋 规划结果")

    travel_plan = result.get("travel_plan", {})
    agent_outputs = result.get("agent_outputs", {})

    # 显示基本信息
    if travel_plan:
        st.markdown("#### 🎯 规划概览")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("目的地", travel_plan.get("destination", "未知"))
            st.metric("行程天数", f"{travel_plan.get('duration', 0)}天")
        with col2:
            st.metric("团队人数", f"{travel_plan.get('group_size', 0)}人")
            st.metric("预算类型", travel_plan.get("budget_range", "未知"))
        with col3:
            interests = travel_plan.get("interests", [])
            st.metric("兴趣爱好", f"{len(interests)}项")
            if interests:
                st.write("、".join(interests))

    # 显示智能体输出
    if agent_outputs:
        st.markdown("#### 🤖 AI智能体建议")

        # 智能体名称映射
        agent_names_cn = {
            'travel_advisor': '🏛️ 旅行顾问',
            'weather_analyst': '🌤️ 天气分析师',
            'budget_optimizer': '💰 预算优化师',
            'local_expert': '🏠 当地专家',
            'itinerary_planner': '📅 行程规划师',
            'simple_agent': '🤖 AI规划师',
            'mock_agent': '🎭 模拟规划师'
        }

        for agent_name, output in agent_outputs.items():
            agent_display_name = agent_names_cn.get(agent_name, agent_name)
            status = output.get('status', '未知')
            response = output.get('response', '无输出')

            # 使用expander显示每个智能体的建议
            with st.expander(f"{agent_display_name} (状态: {status.upper()})", expanded=True):
                st.text_area("智能体建议", value=response, height=200, disabled=True,
                           key=f"agent_{agent_name}", label_visibility="collapsed")

def main():
    """主函数"""
    # 注入自定义CSS样式
    inject_custom_css()
    
    # 显示Hero区域
    display_hero_section()
    
    st.markdown("---")
    
    # 显示自然语言交互界面
    display_chat_interface()

    # 检查API健康状态
    # is_healthy, health_info = check_api_health()

    # if not is_healthy:
    #     st.error("🚨 后端服务连接失败，请检查后端服务是否启动")
    # else:
    #     st.success("✅ 后端服务连接正常")

    # 侧边栏 - 旅行规划表单
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem 0;">
            <div class="sidebar-logo"><img src="https://raw.githubusercontent.com/FlyAIBox/Agent_In_Action/main/03-agent-build-docker-deploy/frontend/logo.png" alt="Logo"></div>
            <h1 style="color: white; font-size: 2.3rem; margin: 1rem 0 0.5rem 0; text-shadow: 0 3px 6px rgba(0,0,0,0.3); font-weight: 800;">旅小智</h1>
            
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")

        # 基本信息
        destination = st.text_input("🎯 目的地", placeholder="例如：北京、上海、成都")

        # 日期选择
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("📅 出发日期", value=date.today() + timedelta(days=1))
        with col2:
            end_date = st.date_input("📅 返回日期", value=date.today() + timedelta(days=8))

        # 团队信息
        group_size = st.number_input("👥 团队人数", min_value=1, max_value=20, value=2)

        # 预算范围
        budget_range = st.selectbox("💰 预算范围", [
            "经济型 (300-800元/天)",
            "舒适型 (800-1500元/天)",
            "中等预算 (1500-3000元/天)",
            "高端旅行 (3000-6000元/天)",
            "奢华体验 (6000元以上/天)"
        ])

        # 住宿偏好
        accommodation = st.selectbox("🏨 住宿偏好", [
            "经济型酒店/青旅",
            "商务酒店",
            "精品酒店",
            "民宿/客栈",
            "度假村",
            "奢华酒店"
        ])

        # 交通偏好
        transportation = st.selectbox("🚗 交通偏好", [
            "公共交通为主",
            "混合交通方式",
            "租车自驾",
            "包车/专车",
            "高铁/飞机"
        ])

        # 兴趣爱好
        st.markdown('<p style="color: white; font-size: 1.3rem; font-weight: 700;  margin-bottom: 0.8rem;">🎨 兴趣爱好</p>', unsafe_allow_html=True)
        interests = []

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.checkbox("🏛️ 历史文化"):
                interests.append("历史文化")
            if st.checkbox("🍽️ 美食体验"):
                interests.append("美食体验")
            if st.checkbox("🏞️ 自然风光"):
                interests.append("自然风光")
            if st.checkbox("🎭 艺术表演"):
                interests.append("艺术表演")
            if st.checkbox("🏖️ 海滨度假"):
                interests.append("海滨度假")

        with col2:
            if st.checkbox("🛍️ 购物娱乐"):
                interests.append("购物娱乐")
            if st.checkbox("🏃 运动健身"):
                interests.append("运动健身")
            if st.checkbox("📸 摄影打卡"):
                interests.append("摄影打卡")
            if st.checkbox("🧘 休闲放松"):
                interests.append("休闲放松")
            if st.checkbox("🎪 主题乐园"):
                interests.append("主题乐园")

        with col3:
            if st.checkbox("🏔️ 登山徒步"):
                interests.append("登山徒步")
            if st.checkbox("🎨 文艺创作"):
                interests.append("文艺创作")
            if st.checkbox("🍷 品酒美食"):
                interests.append("品酒美食")
            if st.checkbox("🏛️ 博物馆"):
                interests.append("博物馆")
            if st.checkbox("🌃 夜生活"):
                interests.append("夜生活")

        # 提交按钮
        if st.button("🚀 开始规划", type="primary", use_container_width=True):
            if not destination:
                st.error("请输入目的地")
            elif start_date >= end_date:
                st.error("返回日期必须晚于出发日期")
            else:
                # 创建旅行规划请求
                travel_data = {
                    "destination": destination,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "group_size": group_size,
                    "budget_range": budget_range,
                    "interests": interests,
                    "accommodation": accommodation,
                    "transportation": transportation,
                    "duration": (end_date - start_date).days,
                    "travel_dates": f"{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}"
                }

                # 存储到session state
                st.session_state.travel_data = travel_data
                st.session_state.planning_started = True

    # 手动查询结果功能
    with st.expander("🔍 手动查询任务结果", expanded=False):
        st.markdown("如果之前的规划任务超时，您可以在这里手动查询结果：")

        # 使用居中布局
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            manual_task_id = st.text_input("输入任务ID", placeholder="例如: task_20250807_123456")
            if st.button("查询结果", type="secondary", use_container_width=True):
                if manual_task_id:
                    # 将结果展示移到expander外层，使用完整宽度居中显示
                    st.session_state.manual_query_task_id = manual_task_id
                    st.session_state.show_manual_result = True
                else:
                    st.warning("请输入任务ID")
    
    # 在expander外部显示查询结果（居中对齐）
    if hasattr(st.session_state, 'show_manual_result') and st.session_state.show_manual_result:
        manual_task_id = st.session_state.manual_query_task_id
        
        # 创建居中容器
        st.markdown("---")
        st.markdown("<br/>", unsafe_allow_html=True)
        
        with st.spinner("正在查询结果..."):
            result = get_planning_result(manual_task_id)
            if result:
                # 使用居中布局显示结果
                _, result_col, _ = st.columns([0.5, 3, 0.5])
                with result_col:
                    st.success("✅ 找到结果！")
                    display_planning_result(result)

                    # 显示下载选项
                    st.markdown("### 📥 下载报告")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("#### 📄 原始数据")
                        download_url = f"{API_BASE_URL}/download/{manual_task_id}"
                        st.markdown(f"[📊 JSON格式数据]({download_url})")
                        st.caption("包含完整的AI分析数据")

                    with col2:
                        st.markdown("#### 📝 Markdown报告")

                        travel_plan = result.get("travel_plan", {})
                        destination = travel_plan.get("destination", "未知目的地").replace("/", "-").replace("\\", "-")
                        group_size = travel_plan.get("group_size", 1)
                        filename_base = f"{destination}-{group_size}人-旅行规划指南"

                        markdown_content = generate_markdown_report(result, manual_task_id)
                        md_filename = f"{filename_base}.md"
                        saved_md_path = save_report_to_results(markdown_content, md_filename)

                        st.download_button(
                            label="📥 下载Markdown报告",
                            data=markdown_content,
                            file_name=md_filename,
                            mime="text/markdown",
                            help="推荐格式，支持所有设备查看"
                        )

                        if saved_md_path:
                            st.success(f"✅ 报告已保存到: {saved_md_path}")
                    
                    # 添加关闭按钮
                    if st.button("❌ 关闭结果", use_container_width=True):
                        st.session_state.show_manual_result = False
                        st.rerun()
            else:
                _, error_col, _ = st.columns([1, 2, 1])
                with error_col:
                    st.error("❌ 未找到该任务的结果")
                    if st.button("重新查询", use_container_width=True):
                        st.session_state.show_manual_result = False
                        st.rerun()

    # 主内容区域
    if hasattr(st.session_state, 'planning_started') and st.session_state.planning_started:
        # 检查是否从聊天接口创建的任务
        if hasattr(st.session_state, 'current_task_id'):
            task_id = st.session_state.current_task_id
        else:
            travel_data = st.session_state.travel_data

            st.markdown("### 🎯 规划请求")
            st.json(travel_data)

            # 创建规划任务
            with st.spinner("正在创建规划任务..."):
                task_id = create_travel_plan(travel_data)

        if task_id:
            st.success(f"✅ 规划任务已创建，任务ID: {task_id}")

            # 显示进度
            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            # 轮询任务状态
            max_attempts = 60  # 最多等待5分钟，每次等待5秒
            attempt = 0
            last_progress = 0

            while attempt < max_attempts:
                status_info = get_planning_status(task_id)

                if status_info:
                    status = status_info.get("status", "unknown")
                    progress = status_info.get("progress", 0)
                    message = status_info.get("message", "处理中...")
                    current_agent = status_info.get("current_agent", "")

                    # 更新进度条
                    progress_placeholder.progress(progress / 100, text=f"进度: {progress}%")

                    # 更新状态信息
                    if current_agent:
                        status_placeholder.info(f"🤖 当前智能体: {current_agent} | {message}")
                    else:
                        status_placeholder.info(f"📋 状态: {message}")

                    # 如果进度有更新，重置计数器
                    if progress > last_progress:
                        last_progress = progress
                        attempt = 0  # 重置计数器

                    if status == "completed":
                        progress_placeholder.progress(1.0, text="进度: 100% - 完成!")
                        status_placeholder.success("🎉 规划完成！")

                        # 从状态信息中直接获取结果
                        result = status_info.get("result")
                        if result:
                            # 显示结果
                            display_planning_result(result)

                            # 生成和下载报告
                            st.markdown("### 📥 下载报告")

                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("#### 📄 原始数据")
                                # 下载JSON格式
                                download_url = f"{API_BASE_URL}/download/{task_id}"
                                st.markdown(f"[📊 JSON格式数据]({download_url})")
                                st.caption("包含完整的AI分析数据")

                            with col2:
                                st.markdown("#### 📝 Markdown报告")

                                # 生成文件名
                                travel_plan = result.get("travel_plan", {})
                                destination = travel_plan.get("destination", "未知目的地").replace("/", "-").replace("\\", "-")
                                group_size = travel_plan.get("group_size", 1)
                                filename_base = f"{destination}-{group_size}人-旅行规划指南"

                                # Markdown报告
                                markdown_content = generate_markdown_report(result, task_id)

                                # 保存到results目录
                                md_filename = f"{filename_base}.md"
                                saved_md_path = save_report_to_results(markdown_content, md_filename)

                                st.download_button(
                                    label="📥 下载Markdown报告",
                                    data=markdown_content,
                                    file_name=md_filename,
                                    mime="text/markdown",
                                    help="推荐格式，支持所有设备查看"
                                )

                                if saved_md_path:
                                    st.success(f"✅ 报告已保存到: {saved_md_path}")

                                st.info("💡 Markdown格式兼容性最好，支持所有设备查看")

                        break

                    elif status == "failed":
                        error_msg = status_info.get("error", "未知错误")
                        progress_placeholder.empty()
                        status_placeholder.error(f"❌ 规划失败: {error_msg}")
                        st.error("规划过程中出现错误，请重新尝试")
                        break

                    elif status in ["processing", "running", "pending"]:
                        # 继续等待
                        time.sleep(5)
                        attempt += 1

                    else:
                        # 未知状态，继续等待
                        time.sleep(5)
                        attempt += 1
                else:
                    # 无法获取状态，可能是网络问题
                    attempt += 1
                    if attempt < max_attempts:
                        status_placeholder.warning(f"任务正在执行中... ({attempt}/{max_attempts})")
                        time.sleep(5)
                    else:
                        status_placeholder.error("❌ 无法获取任务状态")
                        break

            if attempt >= max_attempts:
                progress_placeholder.empty()
                status_placeholder.warning("⏰ 规划超时，后端可能仍在处理中")
                st.info("💡 您可以稍后刷新页面查看结果，或重新提交规划请求")
        else:
            st.error("❌ 创建规划任务失败")

    else:
        # 显示功能特色区域
        display_features_section()
        
        st.markdown("---")
        
        # 显示智能体团队介绍
        st.markdown("<br/><br/>", unsafe_allow_html=True)
        st.markdown("## 🤖 专业AI智能体团队")
        st.markdown("6位专业AI智能体协同工作，为您提供全方位旅行规划服务")
        st.markdown("<br/>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">🏛️ 旅行顾问</h3>
                <p style="color: #666;">
                    提供目的地概览、景点推荐和旅行建议，确保您不错过任何精彩
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">🌤️ 天气分析师</h3>
                <p style="color: #666;">
                    分析目的地天气状况，提供穿衣指南和最佳出行时间建议
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">💰 预算优化师</h3>
                <p style="color: #666;">
                    制定合理的预算分配方案，确保每一分钱都花得物有所值
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">🏠 当地专家</h3>
                <p style="color: #666;">
                    推荐地道的餐厅、体验和隐藏景点，让您像当地人一样旅行
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">📅 行程规划师</h3>
                <p style="color: #666;">
                    安排详细的日程计划，优化路线，确保旅行顺畅高效
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card">
                <h3 style="color: #2d3748;">🎯 协调员</h3>
                <p style="color: #666;">
                    统筹协调各智能体工作，整合信息，提供最优旅行方案
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 显示使用指南
        st.markdown("## 🚀 三步开启智能旅行规划")
        
        guide_col1, guide_col2, guide_col3 = st.columns(3)
        
        with guide_col1:
            st.markdown("""
            <div class="feature-card" style="text-align: center;">
                <h2 style="font-size: 4rem; margin: 0;">1️⃣</h2>
                <h3 style="color: #2d3748;">填写需求</h3>
                <p style="color: #666;">
                    在左侧表单中填写您的旅行目的地、日期、预算和兴趣偏好
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with guide_col2:
            st.markdown("""
            <div class="feature-card" style="text-align: center;">
                <h2 style="font-size: 4rem; margin: 0;">2️⃣</h2>
                <h3 style="color: #2d3748;">AI智能规划</h3>
                <p style="color: #666;">
                    点击"开始规划"，AI智能体团队将在几分钟内为您生成专属方案
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with guide_col3:
            st.markdown("""
            <div class="feature-card" style="text-align: center;">
                <h2 style="font-size: 4rem; margin: 0;">3️⃣</h2>
                <h3 style="color: #2d3748;">下载报告</h3>
                <p style="color: #666;">
                    获取详细的旅行规划报告，支持Markdown和JSON格式下载
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 显示世界风光画廊
        display_world_gallery()
    
    # 显示页脚
    st.markdown("---")
    display_footer()

if __name__ == "__main__":
    main()
