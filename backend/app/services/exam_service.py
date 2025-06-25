from typing import List, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent
from langchain.schema import AgentAction, AgentFinish

from ..core.config import settings
from ..schemas.exam import ExamCreate, QuestionCreate
import random
import datetime

class ExamGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_path=settings.MODEL_PATH,
            temperature=0.7
        )
        
        self.tools = [
            Tool(
                name="create_choice_question",
                func=self._create_choice_question,
                description="生成选择题"
            ),
            Tool(
                name="create_completion_question",
                func=self._create_completion_question,
                description="生成填空题"
            ),
            Tool(
                name="create_programming_question",
                func=self._create_programming_question,
                description="生成编程题"
            )
        ]
        
        self.agent = LLMSingleActionAgent(
            llm=self.llm,
            tools=self.tools,
            prompt=self._get_agent_prompt()
        )
        
        self.executor = AgentExecutor.from_agent_and_tools(
            agent=self.agent,
            tools=self.tools,
            verbose=True
        )
    
    def _get_agent_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            """你是一个专业的考试出题助手。根据以下要求生成考试题目：
            
            知识点: {knowledge_point}
            题型: {question_type}
            难度: {difficulty}/5
            
            请使用合适的工具生成题目。题目要求：
            1. 知识点准确、描述清晰
            2. 难度符合要求
            3. 答案正确且有详细解析
            """
        )
    
    async def _create_choice_question(
        self, 
        knowledge_point: str,
        difficulty: int
    ) -> dict:
        prompt = """生成一道选择题：
        知识点：{knowledge_point}
        难度：{difficulty}/5
        
        要求：
        1. 题干清晰准确
        2. 四个选项，只有一个正确答案
        3. 提供详细解析
        """
        
        # 调用LLM生成题目...
        return {
            "content": "题目内容",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "answer": "A",
            "analysis": "解析说明"
        }
    
    async def generate_exam(
        self,
        course_id: int,
        knowledge_points: List[str],
        question_types: Dict[str, int],
        difficulty: int
    ) -> ExamCreate:
        questions = []
        total_score = 0
        
        for q_type, count in question_types.items():
            score_map = {
                "choice": 5,
                "completion": 10,
                "programming": 20
            }
            score = score_map[q_type]
            
            for _ in range(count):
                result = await self.executor.arun(
                    knowledge_point=knowledge_points[_],
                    question_type=q_type,
                    difficulty=difficulty
                )
                
                question = QuestionCreate(
                    type=q_type,
                    content=result["content"],
                    options=result.get("options"),
                    answer=result["answer"],
                    analysis=result["analysis"],
                    score=score,
                    knowledge_point=knowledge_points[_],
                    difficulty=difficulty
                )
                questions.append(question)
                total_score += score
        
        return ExamCreate(
            title=f"自动生成的考试-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description="AI自动生成的考试题目",
            course_id=course_id,
            duration=120,
            total_score=total_score,
            questions=questions
        )