#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP 客户端示例

用于与 MCP 服务器交互，调用工具并处理结果

Author: FlyAIBox
Date: 2025.10.11
"""

import asyncio
import json
import os
import subprocess
import sys
from typing import Dict, Any, List, Optional
from contextlib import AsyncExitStack

# 使用正确的 MCP 导入
from mcp import ClientSession, StdioServerParameters, Tool
from mcp.client.stdio import stdio_client

class SimpleClientApp:
    """简单的 MCP 客户端应用"""
    
    def __init__(self, server_command: List[str]):
        """
        初始化 MCP 客户端应用
        
        参数:
            server_command: 启动服务器的命令列表
        """
        self.server_command = server_command
        self.server_process = None
        self.client = None
        self.tool_definitions = []
        self.exit_stack = AsyncExitStack()
    
    async def start(self):
        """启动 MCP 客户端并连接到服务器"""
        print("启动 MCP 服务器进程...")
        
        # 配置服务器参数
        server_params = StdioServerParameters(
            command=self.server_command[0],
            args=self.server_command[1:],
            env=None  # 使用默认环境变量
        )
        
        # 启动服务器并获取通信流
        # 通过 stdio_client 协程，以异步方式建立与服务器进程的标准输入/输出通道
        # enter_async_context 可以确保后续资源能自动释放（类似 try...finally）
        # stdio_client(server_params) 会启动子进程并返回 (reader, writer) 的元组
        read_write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        # 解包得到 reader（读取服务器输出）、writer（写入服务器输入），用于后续通信
        # read_write 是一个包含两个元素的元组，分别对应于与服务器通信的 “读取” (reader) 和 “写入” (writer) 流对象。
        read, write = read_write
        
        # 创建 MCP 客户端会话
        self.client = await self.exit_stack.enter_async_context(ClientSession(read, write))
        
        # 初始化连接
        await self.client.initialize()
        
        # 获取工具定义
        response = await self.client.list_tools()
        self.tool_definitions = response.tools
        
        print(f"已连接到服务器，可用工具: {len(self.tool_definitions)}")
        
        for tool in self.tool_definitions:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n使用 'help' 查看帮助，使用 'exit' 退出")
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Optional[str]:
        """
        执行工具调用
        
        参数:
            tool_name: 要调用的工具名称
            params: 工具参数字典
            
        返回:
            工具执行结果或错误消息
        """
        # 检查工具是否存在
        # 遍历工具定义列表，查找名称与 tool_name 匹配的工具对象
        # next() 用于返回第一个匹配的工具（如未找到则返回 None）
        tool_def = next((t for t in self.tool_definitions if t.name == tool_name), None)
        if not tool_def:
            return f"错误: 未找到工具 '{tool_name}'"
        
        try:
            # 调用工具并等待结果
            result = await self.client.call_tool(tool_name, arguments=params)
            
            # 处理结果
            if result and hasattr(result, 'content'):
                return result.content
            else:
                return "工具执行未返回任何结果"
        
        except Exception as e:
            return f"执行过程中出错: {str(e)}"
    
    async def stop(self):
        """停止客户端和服务器"""
        print("正在关闭 MCP 客户端...")
        await self.exit_stack.aclose()
        print("已关闭")
    
    def print_help(self):
        """打印帮助信息"""
        print("\n可用命令:")
        print("  help - 显示此帮助信息")
        print("  list - 列出可用工具")
        print("  call <工具名> <参数JSON> - 调用工具")
        print("  exit - 退出程序")
        print("\n示例:")
        print("  call get_weather_warning {\"location\": \"101010100\"}")
        print("  call get_daily_forecast 116.41,39.92")
        print("  call get_daily_forecast 101010100 7")
    
    def print_tools(self):
        """打印工具列表和描述"""
        print("\n可用工具:")
        for tool in self.tool_definitions:
            print(f"  {tool.name} - {tool.description}")
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print("    参数:")
                props = tool.inputSchema.get('properties', {})
                for param_name, param_info in props.items():
                    param_type = param_info.get('type', 'unknown')
                    param_desc = param_info.get('description', '')
                    print(f"      {param_name} ({param_type}): {param_desc}")

async def main():
    """主函数"""
    # 确定服务器路径
    server_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "server",
        "weather_server.py"
    )
    
    # 检查服务器文件是否存在
    if not os.path.exists(server_path):
        print(f"错误: 服务器文件不存在: {server_path}")
        return
    
    # 创建客户端应用
    app = SimpleClientApp(["python", server_path])
    
    try:
        # 启动客户端
        await app.start()
        
        # 主循环
        while True:
            try:
                # 获取用户输入
                command = input("\n> ").strip()
                
                # 处理命令
                if command == "exit":
                    break
                
                elif command == "help":
                    app.print_help()
                
                elif command == "list":
                    app.print_tools()
                
                elif command.startswith("call "):
                    # 解析命令
                    parts = command[5:].strip().split(" ", 1)
                    if len(parts) < 1:
                        print("错误: 缺少工具名")
                        continue
                    
                    tool_name = parts[0]
                    
                    # 解析参数
                    params = {}
                    if len(parts) > 1:
                        params_str = parts[1]
                        
                        # 尝试解析为 JSON
                        try:
                            params = json.loads(params_str)
                        except json.JSONDecodeError:
                            # 如果不是 JSON，尝试简单解析
                            try:
                                # 对于 get_weather_warning，只需要一个位置参数
                                if tool_name == "get_weather_warning":
                                    params = {"location": params_str}
                                
                                # 对于 get_daily_forecast，需要位置和可选的天数
                                elif tool_name == "get_daily_forecast":
                                    forecast_args = params_str.split()
                                    if len(forecast_args) < 1:
                                        print("错误: get_daily_forecast 至少需要一个位置参数")
                                        continue
                                    
                                    params = {"location": forecast_args[0]}
                                    
                                    # 如果提供了天数参数
                                    if len(forecast_args) > 1:
                                        try:
                                            params["days"] = int(forecast_args[1])
                                        except ValueError:
                                            print("错误: days 参数必须是整数")
                                            continue
                                else:
                                    print(f"错误: 无法解析 {tool_name} 的参数")
                                    continue
                            
                            except Exception as e:
                                print(f"参数解析错误: {str(e)}")
                                continue
                    
                    # 执行工具调用
                    print("正在调用工具...")
                    result = await app.execute_tool(tool_name, params)
                    print("\n结果:")
                    print(result)
                
                else:
                    print(f"未知命令: {command}")
                    print("使用 'help' 查看可用命令")
            
            except KeyboardInterrupt:
                print("\n操作被中断")
                break
            
            except Exception as e:
                print(f"错误: {str(e)}")
    
    except Exception as e:
        print(f"客户端错误: {str(e)}")
    
    finally:
        # 停止客户端
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被中断")
        sys.exit(0) 