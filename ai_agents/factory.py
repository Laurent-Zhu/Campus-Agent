from typing import Optional
from langchain.chat_models import ChatOpenAI
from .base.base_agent import BaseAgent
from .teacher.exam.exam_generator import ExamGeneratorAgent

class AgentFactory:
    """智能体工厂类"""
    
    @staticmethod
    def create_agent(
        agent_type: str,
        model_name: str = "chatglm3",
        **kwargs
    ) -> Optional[BaseAgent]:
        """
        创建智能体实例
        
        Args:
            agent_type: 智能体类型
            model_name: 模型名称
            **kwargs: 其他参数
        
        Returns:
            BaseAgent: 智能体实例
        """
        # 创建LLM实例
        llm = ChatOpenAI(
            model_name=model_name,
            temperature=kwargs.get("temperature", 0.7)
        )
        
        # 根据类型创建对应的智能体
        if agent_type == "exam_generator":
            agent = ExamGeneratorAgent(llm=llm)
        else:
            return None
        
        # 初始化智能体
        agent.initialize()
        return agent