from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from ...base.base_agent import BaseAgent

class ExamGeneratorAgent(BaseAgent):
    """考试生成智能体"""
    
    def initialize(self) -> None:
        # 定义生成题目的工具
        self.tools = [
            Tool(
                name="generate_choice_question",
                func=self._generate_choice_question,
                description="生成选择题，输入知识点和难度"
            ),
            Tool(
                name="generate_completion_question",
                func=self._generate_completion_question,
                description="生成填空题，输入知识点和难度"
            ),
            Tool(
                name="generate_programming_question",
                func=self._generate_programming_question,
                description="生成编程题，输入知识点和难度"
            )
        ]
        
        # 设置记忆模块
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 创建Agent执行器
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=self._create_agent(),
            tools=self.tools,
            memory=self.memory,
            verbose=True
        )
    
    def _create_agent(self) -> LLMSingleActionAgent:
        """创建LLM单动作智能体"""
        prompt = ChatPromptTemplate.from_template(
            """你是一个专业的考试出题助手。
            
            已知信息：
            - 课程：{course}
            - 知识点：{knowledge_points}
            - 难度要求：{difficulty}/5
            
            请根据以下规则生成考试题目：
            1. 知识点必须准确、描述清晰
            2. 难度符合要求
            3. 答案正确且有详细解析
            4. 选择题必须有4个选项
            5. 编程题必须包含示例输入输出
            
            你可以使用以下工具：
            {tools}
            
            请严格按照要求完成出题。
            """
        )
        
        return LLMSingleActionAgent.from_llm_and_tools(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
    
    async def _generate_choice_question(
        self,
        knowledge_point: str,
        difficulty: int
    ) -> Dict:
        """生成选择题"""
        prompt = """生成一道选择题：
        知识点：{knowledge_point}
        难度：{difficulty}/5
        
        要求：
        1. 题干描述清晰、专业准确
        2. 四个选项，只有一个正确答案
        3. 干扰项合理
        4. 提供详细解析
        """
        
        # 调用LLM生成题目
        response = await self.llm.agenerate([prompt])
        # 解析响应...
        
        return {
            "type": "choice",
            "content": "题目内容",
            "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
            "answer": "A",
            "analysis": "解析说明",
            "knowledge_point": knowledge_point,
            "difficulty": difficulty
        }
    
    async def arun(
        self,
        course: str,
        knowledge_points: List[str],
        question_types: Dict[str, int],
        difficulty: int
    ) -> List[Dict]:
        """生成完整的试卷"""
        questions = []
        
        for q_type, count in question_types.items():
            for i in range(count):
                knowledge_point = knowledge_points[i % len(knowledge_points)]
                
                result = await self.agent_executor.arun(
                    course=course,
                    knowledge_points=knowledge_point,
                    difficulty=difficulty
                )
                # 确保score为int
                if isinstance(result, dict) and "score" in result:
                    result["score"] = int(result["score"])
                questions.append(result)
        
        return questions