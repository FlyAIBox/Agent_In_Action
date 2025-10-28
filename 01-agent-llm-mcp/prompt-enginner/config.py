#!/usr/bin/env python3
"""
OpenAI API 配置管理模块

🎯 主要功能：
- 多源配置管理：环境变量 → IPython存储 → 默认值
- 一键环境设置：自动配置OpenAI客户端和便捷函数
- 安全密钥处理：脱敏显示、占位符检测
- 智能环境检测：支持Jupyter notebook和普通Python环境

🔧 核心特性：
- 配置优先级：环境变量 > IPython存储 > 默认值
- 自动依赖安装：检测并安装缺失的依赖包
- 优雅错误处理：详细的配置指导和错误提示
- 模块化设计：每个函数职责单一，易于维护和扩展

🚀 使用场景：
- 学习环境：Jupyter notebook交互式配置
- 开发环境：.env文件本地配置
- 生产环境：环境变量安全配置
- 代理服务：支持国内API代理服务

📋 支持的配置方式：
1. 环境变量：OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL
2. .env文件：项目根目录或模块目录的.env文件
3. IPython存储：%store API_KEY, %store MODEL_NAME
4. 默认值：gpt-4o模型作为兜底配置
"""

import os
import warnings
from pathlib import Path
from typing import Optional, Tuple


_DOTENV_LOADED = False


def _load_env_file() -> None:
    """Load .env from CWD first, then module directory, once, without overriding."""
    global _DOTENV_LOADED

    if _DOTENV_LOADED:
        return

    # Determine candidate .env locations (CWD first, then module directory)
    candidate_paths = []
    cwd_dotenv = Path.cwd() / ".env"
    if cwd_dotenv.is_file():
        candidate_paths.append(cwd_dotenv)

    module_dotenv = Path(__file__).resolve().parent / ".env"
    if module_dotenv.is_file() and module_dotenv not in candidate_paths:
        candidate_paths.append(module_dotenv)

    if not candidate_paths:
        _DOTENV_LOADED = True
        return

    try:
        from dotenv import load_dotenv
    except ImportError:
        warnings.warn(
            "python-dotenv 未安装，无法自动读取 .env 文件。"
            "请通过 `pip install python-dotenv` 进行安装，或手动设置环境变量。"
        )
        _DOTENV_LOADED = True
        return

    # Load found .env files in order; do not override already-set variables
    for path in candidate_paths:
        load_dotenv(dotenv_path=path, override=False)

    _DOTENV_LOADED = True


def get_openai_config() -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    获取OpenAI API配置，按优先级顺序：
    1. 环境变量 (最高优先级)
    2. IPython存储变量 (中等优先级)  
    3. 默认值 (兜底配置)
    
    特性：
    - 自动加载.env文件（如果存在）
    - 支持多种环境变量名（兼容性处理）
    - 智能IPython环境检测
    - 安全的默认值设置
    
    返回:
        Tuple[api_key, model_name, base_url]: API密钥、模型名称、API基础URL
        
    示例:
        >>> api_key, model, base_url = get_openai_config()
        >>> print(f"使用模型: {model}")
    """
    _load_env_file()

    api_key = None
    model_name = None
    base_url = None
    
    # 1. 优先从环境变量读取
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        # 兼容其他常见的环境变量名
        api_key = os.getenv('API_KEY')
    
    model_name = os.getenv('OPENAI_MODEL', os.getenv('MODEL_NAME'))
    
    # 检查自定义API地址（国内代理等）
    base_url = os.getenv('OPENAI_API_BASE') or os.getenv('OPENAI_BASE_URL')
    
    # 2. 如果环境变量中没有，尝试从IPython存储读取
    if not api_key or not model_name:
        try:
            from IPython import get_ipython
            ipython = get_ipython()
            
            if ipython is not None:
                # 尝试从IPython存储中恢复变量
                if not api_key:
                    try:
                        ipython.magic('store -r API_KEY')
                        api_key = ipython.user_ns.get('API_KEY')
                    except:
                        pass
                
                if not model_name:
                    try:
                        ipython.magic('store -r MODEL_NAME')
                        model_name = ipython.user_ns.get('MODEL_NAME')
                    except:
                        pass
        except ImportError:
            # 不在IPython环境中
            pass
    
    # 3. 设置默认值
    if not model_name:
        model_name = "gpt-4o"  # 默认使用gpt-4o模型
    
    return api_key, model_name, base_url


def setup_openai_client():
    """
    设置OpenAI客户端，处理环境变量和IPython存储的配置
    
    功能：
    - 自动获取配置信息
    - 验证API密钥有效性
    - 创建OpenAI客户端实例
    - 支持自定义API地址（代理服务）
    - 提供详细的配置来源信息
    
    返回:
        tuple: (client, model_name, config_source)
            - client: 配置好的OpenAI客户端
            - model_name: 使用的模型名称
            - config_source: 配置来源描述
            
    异常:
        ValueError: 当API密钥无效或缺失时抛出
        
    示例:
        >>> client, model, source = setup_openai_client()
        >>> print(f"配置来源: {source}")
    """
    import openai
    
    api_key, model_name, base_url = get_openai_config()
    
    # 检查API密钥是否可用
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "❌ 未找到有效的OpenAI API密钥！\n\n"
            "请通过以下方式之一设置API密钥：\n\n"
            "方式一：环境变量（推荐）\n"
            "export OPENAI_API_KEY='sk-your-api-key-here'\n\n"
            "方式二：在Jupyter notebook中设置\n"
            "API_KEY = 'sk-your-api-key-here'\n"
            "%store API_KEY\n\n"
            "获取API密钥：\n"
            "- OpenAI: https://platform.openai.com/api-keys\n"
            "- DeepSeek: https://platform.deepseek.com/api-keys\n"
            "- 国内代理: https://www.apiyi.com/register/?aff_code=we80"
        )
    
    # 确定配置来源
    config_source = []
    if os.getenv('OPENAI_API_KEY') or os.getenv('API_KEY'):
        config_source.append("环境变量")
    else:
        config_source.append("IPython存储")
    
    # 创建OpenAI客户端
    client_kwargs = {'api_key': api_key}
    if base_url:
        client_kwargs['base_url'] = base_url
        config_source.append(f"自定义API地址: {base_url}")
    
    client = openai.OpenAI(**client_kwargs)
    
    return client, model_name, " + ".join(config_source)


def get_completion_with_config(prompt: str, system_prompt: str = "", **kwargs):
    """
    使用自动配置的客户端获取GPT完成响应
    
    参数:
        prompt (str): 用户提示
        system_prompt (str): 系统提示（可选）
        **kwargs: 其他OpenAI API参数
    
    返回:
        str: GPT的响应文本
    """
    client, model_name, config_source = setup_openai_client()
    
    # 构建消息列表
    messages = []
    
    # 如果有系统提示，添加系统消息
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # 添加用户消息
    messages.append({"role": "user", "content": prompt})
    
    # 设置默认参数
    api_params = {
        'model': model_name,
        'messages': messages,
        'max_tokens': 2000,
        'temperature': 0.0
    }
    
    # 更新用户提供的参数
    api_params.update(kwargs)
    
    # 调用OpenAI API
    response = client.chat.completions.create(**api_params)
    
    return response.choices[0].message.content


def print_config_info():
    """
    打印当前配置信息
    """
    try:
        api_key, model_name, base_url = get_openai_config()
        client, model_name, config_source = setup_openai_client()
        
        print("🔧 OpenAI API 配置信息:")
        print(f"  📡 配置来源: {config_source}")
        print(f"  🤖 模型: {model_name}")
        if base_url:
            print(f"  🌐 API地址: {base_url}")
        print(f"  🔑 API密钥: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else '****'}")
        print()
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")


def setup_notebook_environment():
    """
    为notebook环境设置完整的OpenAI配置
    
    主要功能：
    - 自动检测并安装OpenAI依赖包
    - 配置OpenAI客户端
    - 创建便捷的get_completion函数
    - 显示配置信息和状态
    - 提供完整的错误处理
    
    特性：
    - 一键式环境设置
    - 智能依赖管理
    - 用户友好的状态反馈
    - 支持系统提示和预填充功能
    
    返回:
        tuple: (client, get_completion函数)
            - client: 配置好的OpenAI客户端
            - get_completion: 便捷的API调用函数
            
    使用示例:
        >>> client, get_completion = setup_notebook_environment()
        >>> response = get_completion("你好，请介绍一下自己")
        >>> print(response)
    """
    # 安装依赖
    try:
        import openai
    except ImportError:
        print("📦 正在安装OpenAI库...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==1.107.0"])
        import openai
    
    # 设置客户端
    client, model_name, config_source = setup_openai_client()
    
    print("✅ OpenAI环境设置完成!")
    print_config_info()
    
    # 创建get_completion函数
    def get_completion(prompt: str, system_prompt: str = "", prefill: str = ""):
        """
        获取GPT的完成响应 - 便捷的API调用函数
        
        功能特性：
        - 简化的API调用接口
        - 支持系统提示设置AI行为
        - 支持预填充文本引导响应
        - 自动处理消息格式和参数
        
        参数:
            prompt (str): 用户提示内容
            system_prompt (str): 系统提示（可选），用于设置AI的角色和行为
            prefill (str): 预填充文本（可选），用于引导GPT的响应开始
        
        返回:
            str: GPT的响应文本
            
        使用示例:
            >>> # 基础使用
            >>> response = get_completion("解释什么是机器学习")
            
            >>> # 带系统提示
            >>> response = get_completion(
            ...     "写一个Python函数", 
            ...     system_prompt="你是一个专业的Python编程助手"
            ... )
            
            >>> # 带预填充
            >>> response = get_completion(
            ...     "继续完成这个句子", 
            ...     prefill="Python是一种"
            ... )
        """
        # 构建消息列表
        messages = []
        
        # 如果有系统提示，添加系统消息
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # 添加用户消息
        messages.append({"role": "user", "content": prompt})
        
        # 如果有预填充内容，添加助手消息来模拟预填充效果
        if prefill:
            messages.append({"role": "assistant", "content": prefill})
            # 再添加一个用户消息请求继续
            messages.append({"role": "user", "content": "请继续完成响应。"})
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model=model_name,              # 模型名称 (gpt-4o 或 deepseek-r1)
            messages=messages,             # 消息列表
            max_tokens=2000,              # 最大token数
            temperature=0.0               # 温度参数，0表示更确定性
        )
        
        # 如果有预填充内容，将其与生成的内容组合
        if prefill:
            return prefill + response.choices[0].message.content
        else:
            return response.choices[0].message.content
    
    return client, get_completion


# 主要配置检查函数
def validate_config():
    """
    验证OpenAI API配置是否正确和完整
    
    验证项目：
    - 检查API密钥是否存在
    - 验证API密钥不是占位符
    - 确保配置格式正确
    - 提供详细的验证结果
    
    返回:
        bool: 配置验证结果
            - True: 配置有效
            - False: 配置无效或缺失
            
    功能：
    - 自动检测配置问题
    - 提供友好的错误提示
    - 支持配置状态检查
    
    使用示例:
        >>> if validate_config():
        ...     print("配置验证通过，可以开始使用")
        ... else:
        ...     print("需要配置API密钥")
    """
    try:
        api_key, model_name, base_url = get_openai_config()
        
        if not api_key:
            print("⚠️  警告: 未设置API密钥")
            return False
            
        if api_key == "your_api_key_here":
            print("⚠️  警告: 请替换默认的API密钥占位符")
            return False
            
        print("✅ 配置验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        return False


if __name__ == "__main__":
    print("🔧 OpenAI API 配置管理模块")
    print("=" * 50)
    print_config_info()
    validate_config() 
