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
    page_title="AI旅行规划智能体",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API基础URL
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

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
    st.title("🌍 AI旅行规划智能体")
    st.markdown("---")

    # 检查API健康状态
    is_healthy, health_info = check_api_health()

    if not is_healthy:
        st.error("🚨 后端服务连接失败")
        st.error(health_info.get("error", "未知错误"))

        with st.expander("🔧 后端服务启动指南", expanded=True):
            st.markdown("""
            ### 启动后端服务

            请在终端中执行以下命令：

            ```bash
            # 方法1: 使用启动脚本
            ./start_backend.sh

            # 方法2: 手动启动
            cd backend
            python api_server.py
            ```

            ### 检查服务状态

            启动后，您可以访问以下地址检查服务状态：
            - 健康检查: http://localhost:8080/health
            - API文档: http://localhost:8080/docs

            ### 常见问题

            1. **端口被占用**: 检查是否有其他程序使用8080端口
            2. **依赖缺失**: 确保已安装所有依赖 `pip install -r backend/requirements.txt`
            3. **环境变量**: 确保设置了必要的API密钥
            """)

        # 仍然允许用户使用手动查询功能
        st.info("💡 如果您之前有完成的任务，可以使用下面的手动查询功能")
    else:
        st.success("✅ 后端服务连接正常")

    # 侧边栏 - 旅行规划表单
    with st.sidebar:
        st.header("📝 旅行规划表单")

        # 基本信息
        destination = st.text_input("🎯 目的地", placeholder="例如：北京、上海、成都")

        # 日期选择
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("📅 出发日期", value=date.today() + timedelta(days=7))
        with col2:
            end_date = st.date_input("📅 返回日期", value=date.today() + timedelta(days=10))

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
        st.markdown("🎨 **兴趣爱好**")
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

        col1, col2 = st.columns([3, 1])
        with col1:
            manual_task_id = st.text_input("输入任务ID", placeholder="例如: task_20250807_123456")
        with col2:
            if st.button("查询结果", type="secondary"):
                if manual_task_id:
                    with st.spinner("正在查询结果..."):
                        result = get_planning_result(manual_task_id)
                        if result:
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
                        else:
                            st.error("❌ 未找到该任务的结果")
                else:
                    st.warning("请输入任务ID")

    # 主内容区域
    if hasattr(st.session_state, 'planning_started') and st.session_state.planning_started:
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
        # 显示欢迎信息
        st.markdown("""
        ## 🎉 欢迎使用AI旅行规划智能体！

        ### ✨ 功能特色
        - 🤖 **多智能体协作**: 6个专业AI智能体为您服务
        - 🎯 **个性化规划**: 根据您的兴趣和预算定制
        - 📊 **实时进度**: 查看规划过程的每一步
        - 📄 **专业报告**: 生成详细的旅行规划文档

        ### 🚀 开始使用
        1. 在左侧填写旅行需求
        2. 点击"开始规划"按钮
        3. 等待AI智能体完成规划
        4. 下载您的专属旅行指南

        ### 🤖 智能体团队
        - 🏛️ **旅行顾问**: 提供目的地概览和建议
        - 🌤️ **天气分析师**: 分析天气状况和穿衣建议
        - 💰 **预算优化师**: 制定合理的预算分配
        - 🏠 **当地专家**: 推荐地道的体验和美食
        - 📅 **行程规划师**: 安排详细的日程计划
        """)

if __name__ == "__main__":
    main()
