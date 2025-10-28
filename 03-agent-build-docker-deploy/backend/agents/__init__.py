"""
__init__.py 文件在 Python 包管理中扮演着至关重要的角色，它的核心作用是：

告诉 Python 解释器，包含它的目录是一个包。

执行包初始化代码，可以在导入包时自动运行。

简化导入路径，让用户更方便地访问包内的模块和函数。

控制 from ... import * 的行为，通过 __all__ 列表来明确暴露哪些内容。
"""
"""
多智能体旅行规划系统的基础智能体框架

这个模块定义了传统多智能体系统的核心组件，包括：
- 智能体角色定义和枚举
- 消息类型和通信协议
- 基础智能体抽象类
- 智能体通信中心
- 协作决策引擎

适用于大模型技术初级用户：
这个模块展示了如何设计一个完整的多智能体系统架构，
包含通信机制、协作模式和决策流程。
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum

class AgentRole(Enum):
    """
    定义不同的智能体角色

    这个枚举类定义了系统中所有智能体的角色类型，
    每个角色都有特定的职责和专业领域。

    适用于大模型技术初级用户：
    枚举类是一种定义常量集合的优雅方式，
    确保角色名称的一致性和类型安全。
    """
    COORDINATOR = "coordinator"           # 协调员：总体协调和决策
    TRAVEL_ADVISOR = "travel_advisor"     # 旅行顾问：目的地专业知识
    BUDGET_OPTIMIZER = "budget_optimizer" # 预算优化师：成本控制和优化
    WEATHER_ANALYST = "weather_analyst"   # 天气分析师：天气情报和建议
    LOCAL_EXPERT = "local_expert"         # 当地专家：本地知识和文化
    ITINERARY_PLANNER = "itinerary_planner" # 行程规划师：日程安排和物流

class MessageType(Enum):
    """
    智能体可以发送的消息类型

    定义了智能体间通信的不同消息类型，
    每种类型都有特定的用途和处理方式。

    适用于大模型技术初级用户：
    通过定义消息类型，系统可以更好地处理
    不同类型的智能体交互和协作。
    """
    REQUEST = "request"               # 请求：向其他智能体请求信息或服务
    RESPONSE = "response"             # 响应：对请求的回复
    BROADCAST = "broadcast"           # 广播：向所有智能体发送信息
    QUERY = "query"                   # 查询：询问特定信息
    RECOMMENDATION = "recommendation" # 推荐：提供建议或推荐

class Message:
    """
    智能体通信的消息结构

    这个类定义了智能体间通信的标准消息格式，
    包含发送者、接收者、消息类型和内容等信息。

    适用于大模型技术初级用户：
    这个类展示了如何设计一个完整的消息系统，
    包含元数据管理和序列化功能。
    """

    def __init__(self, sender: str, receiver: str, msg_type: MessageType,
                 content: Dict[str, Any], timestamp: datetime = None):
        """
        初始化消息对象

        参数：
        - sender: 发送者ID
        - receiver: 接收者ID
        - msg_type: 消息类型
        - content: 消息内容
        - timestamp: 时间戳（可选）
        """
        self.sender = sender                                    # 发送者
        self.receiver = receiver                                # 接收者
        self.msg_type = msg_type                               # 消息类型
        self.content = content                                 # 消息内容
        self.timestamp = timestamp or datetime.now()          # 时间戳
        self.id = f"{sender}_{receiver}_{int(time.time() * 1000)}" # 唯一ID

    def to_dict(self) -> Dict[str, Any]:
        """
        将消息转换为字典格式

        用于消息的序列化和存储，
        便于日志记录和调试。

        返回：消息的字典表示
        """
        return {
            'id': self.id,
            'sender': self.sender,
            'receiver': self.receiver,
            'type': self.msg_type.value,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }

class BaseAgent(ABC):
    """
    所有智能体的抽象基类

    面向大模型技术初学者：
    - 这是所有具体智能体的共同父类，规定了最基本的行为接口（如处理消息、生成建议）。
    - 任何新的智能体都应继承此类，并实现 `process_message` 与 `generate_recommendation` 两个抽象方法。
    - 该基类还内置了消息队列、知识库、协作网络等通用能力，帮助你快速构建可协同工作的智能体。
    """
    
    def __init__(self, agent_id: str, role: AgentRole, capabilities: List[str]):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.message_queue: List[Message] = []
        self.knowledge_base: Dict[str, Any] = {}
        self.is_active = True
        self.collaboration_network: Dict[str, 'BaseAgent'] = {}
        
    @abstractmethod
    def process_message(self, message: Message) -> Optional[Message]:
        """
        处理收到的单条消息，并在需要时返回一条响应消息

        参数：
        - message: 收到的 `Message` 对象

        返回：
        - 可选的 `Message` 响应；若无需回复则返回 None

        初学者提示：
        - 在具体智能体中实现时，通常会根据 `message.type` 与 `message.content` 决定如何处理。
        - 如需异步或批量处理，也可以只入队，随后由 `process_message_queue` 统一处理。
        """
        pass
    
    @abstractmethod
    def generate_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于上下文生成该智能体的结构化建议

        参数：
        - context: 决策/任务上下文字典，例如用户偏好、预算关注点、天气约束等

        返回：
        - 字典形式的建议结果。建议包含关键结论、理由与可选的替代方案，便于后续协同决策引擎综合。
        """
        pass
    
    def send_message(self, receiver: str, msg_type: MessageType, content: Dict[str, Any]) -> bool:
        """
        发送消息给另一位已连接的智能体

        参数：
        - receiver: 接收方智能体的 ID
        - msg_type: 消息类型（见 `MessageType`）
        - content: 消息内容（任意结构化字典）

        返回：
        - 若接收方存在于协作网络并成功入队，返回 True；否则返回 False
        """
        if receiver in self.collaboration_network:
            message = Message(self.agent_id, receiver, msg_type, content)
            self.collaboration_network[receiver].receive_message(message)
            return True
        return False
    
    def receive_message(self, message: Message):
        """
        接收一条消息并加入本地消息队列，等待后续处理
        """
        self.message_queue.append(message)
    
    def process_message_queue(self) -> List[Message]:
        """
        处理消息队列中的所有消息

        执行流程：
        - 从队列头部逐条取出消息
        - 调用 `process_message` 进行处理
        - 若有回复消息则收集到结果列表

        返回：
        - 所有需要发送的回复消息列表（可能为空）
        """
        responses = []
        while self.message_queue:
            message = self.message_queue.pop(0)
            response = self.process_message(message)
            if response:
                responses.append(response)
        return responses
    
    def connect_agent(self, agent: 'BaseAgent'):
        """
        将另一个智能体与当前智能体建立双向协作连接

        提示：
        - 连接后，双方会互相出现在对方的 `collaboration_network` 中。
        - 只有建立连接的智能体之间才能直接互发消息。
        """
        self.collaboration_network[agent.agent_id] = agent
        agent.collaboration_network[self.agent_id] = self
    
    def update_knowledge(self, key: str, value: Any):
        """
        更新智能体的本地知识库条目

        用途：
        - 用于缓存跨消息/多轮对话可复用的信息，例如用户偏好、历史查询结果等。
        """
        self.knowledge_base[key] = value
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取当前智能体的运行状态快照（便于监控与可视化）
        """
        return {
            'agent_id': self.agent_id,
            'role': self.role.value,
            'capabilities': self.capabilities,
            'is_active': self.is_active,
            'messages_queued': len(self.message_queue),
            'connected_agents': list(self.collaboration_network.keys()),
            'knowledge_items': len(self.knowledge_base)
        }

class AgentCommunicationHub:
    """
    智能体通信与协调的中央枢纽

    面向初学者：
    - 负责注册智能体、建立全网互联、广播消息以及统一推进各智能体的消息处理。
    - 可视为一个简化的“消息总线 + 注册中心”。
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_log: List[Message] = []
        
    def register_agent(self, agent: BaseAgent):
        """
        将智能体注册到通信枢纽中
        """
        self.agents[agent.agent_id] = agent
        
    def connect_all_agents(self):
        """
        将已注册的所有智能体两两互联，形成全连接协作网络
        """
        agent_list = list(self.agents.values())
        for i, agent1 in enumerate(agent_list):
            for j, agent2 in enumerate(agent_list):
                if i != j:
                    agent1.connect_agent(agent2)
    
    def broadcast_message(self, sender_id: str, content: Dict[str, Any]) -> List[Message]:
        """
        将某个智能体的广播消息分发给除其自身外的所有智能体

        说明：
        - 本方法负责投递与记录广播消息；实际回复由各智能体在其消息循环中产生。
        - 当前实现返回值为占位的响应列表（保持接口一致性）。
        """
        responses = []
        if sender_id in self.agents:
            sender = self.agents[sender_id]
            for agent_id, agent in self.agents.items():
                if agent_id != sender_id:
                    message = Message(sender_id, agent_id, MessageType.BROADCAST, content)
                    agent.receive_message(message)
                    self.message_log.append(message)
        return responses
    
    def process_all_agents(self) -> Dict[str, List[Message]]:
        """
        触发所有已注册智能体处理其消息队列，并汇总产生的回复

        返回：
        - 字典，键为 `agent_id`，值为该智能体产生的回复消息列表
        """
        all_responses = {}
        for agent_id, agent in self.agents.items():
            responses = agent.process_message_queue()
            if responses:
                all_responses[agent_id] = responses
        return all_responses
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[BaseAgent]:
        """
        按角色检索已注册的智能体实例
        """
        for agent in self.agents.values():
            if agent.role == role:
                return agent
        return None
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        获取系统级运行状态概览，用于监控与调试
        """
        return {
            'total_agents': len(self.agents),
            'active_agents': len([a for a in self.agents.values() if a.is_active]),
            'total_messages': len(self.message_log),
            'agents': {aid: agent.get_status() for aid, agent in self.agents.items()}
        }

class AgentDecisionEngine:
    """
    多智能体协同决策引擎

    职责：
    - 向指定的参与智能体征询建议
    - 依据上下文与角色权重综合各方建议
    - 形成最终决策并进行广播
    """
    
    def __init__(self, communication_hub: AgentCommunicationHub):
        self.hub = communication_hub
        
    def collaborative_decision(self, decision_context: Dict[str, Any], 
                             involved_agents: List[str]) -> Dict[str, Any]:
        """
        召集多位智能体共同参与，产出一次协同决策

        参数：
        - decision_context: 决策上下文（如用户需求、主要关切点、约束条件等）
        - involved_agents: 参与决策的智能体 ID 列表

        返回：
        - 综合后的最终决策字典，包含主要建议、置信度、支撑证据等
        """
        
        # 步骤 1：向参与智能体征询各自建议
        recommendations = {}
        for agent_id in involved_agents:
            if agent_id in self.hub.agents:
                agent = self.hub.agents[agent_id]
                rec = agent.generate_recommendation(decision_context)
                recommendations[agent_id] = rec
        
        # 步骤 2：分析并综合多方建议
        final_decision = self._synthesize_recommendations(recommendations, decision_context)
        
        # 步骤 3：广播最终决策，便于各方同步
        self.hub.broadcast_message("decision_engine", {
            'decision': final_decision,
            'context': decision_context,
            'contributing_agents': involved_agents
        })
        
        return final_decision
    
    def _synthesize_recommendations(self, recommendations: Dict[str, Dict], 
                                  context: Dict[str, Any]) -> Dict[str, Any]:
        """
        将多个智能体的建议综合为最终决策

        方法要点：
        - 基于上下文计算各智能体的权重（与角色专业性匹配）
        - 采用简化的一致性与加权选择策略选出主要建议
        - 保留所有建议作为支撑证据，供透明化追踪
        """
        
        # 基于智能体专业性与当前上下文计算权重
        weights = self._calculate_agent_weights(recommendations, context)
        
        # 组合建议形成结构化的最终结果
        final_decision = {
            'primary_recommendation': None,
            'confidence_score': 0.0,
            'supporting_evidence': [],
            'alternative_options': [],
            'consensus_level': 0.0
        }
        
        # 简化的一致性机制（可在未来引入机器学习增强）
        if recommendations:
            # 聚合所有建议与对应权重
            all_recommendations = []
            for agent_id, rec in recommendations.items():
                weight = weights.get(agent_id, 1.0)
                all_recommendations.append({
                    'agent': agent_id,
                    'recommendation': rec,
                    'weight': weight
                })
            
            # 基于权重与一致性选择主要建议
            best_rec = max(all_recommendations, key=lambda x: x['weight'])
            final_decision['primary_recommendation'] = best_rec['recommendation']
            final_decision['confidence_score'] = best_rec['weight']
            final_decision['supporting_evidence'] = [r['recommendation'] for r in all_recommendations]
            
            # 计算一致性水平（此处为占位性度量）
            final_decision['consensus_level'] = len(all_recommendations) / len(recommendations) if recommendations else 0
        
        return final_decision
    
    def _calculate_agent_weights(self, recommendations: Dict[str, Dict], 
                               context: Dict[str, Any]) -> Dict[str, float]:
        """
        根据角色专业性与当前关注点计算各智能体建议的权重

        规则示例：
        - 若主要关注点为预算，则提升预算优化师的权重
        - 若主要关注点为天气，则提升天气分析师的权重
        - 若主要关注点为本地洞察，则提升当地专家的权重
        """
        weights = {}
        
        # 按角色与上下文设定默认权重
        for agent_id in recommendations.keys():
            if agent_id in self.hub.agents:
                agent = self.hub.agents[agent_id]
                base_weight = 1.0
                
                # 根据与当前关注点的相关性提升权重
                if context.get('primary_concern') == 'budget' and agent.role == AgentRole.BUDGET_OPTIMIZER:
                    base_weight = 2.0
                elif context.get('primary_concern') == 'weather' and agent.role == AgentRole.WEATHER_ANALYST:
                    base_weight = 2.0
                elif context.get('primary_concern') == 'local_insights' and agent.role == AgentRole.LOCAL_EXPERT:
                    base_weight = 2.0
                
                weights[agent_id] = base_weight
        
        return weights
