from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from typing import List, Dict
import uuid
from datetime import datetime
import random
import json

from models.exam import Question, Exam
from utils.model_client import ChatGLMClient

class ExamGeneratorAgent:
    def __init__(self):
        self.client = ChatGLMClient()
    
    async def _generate_question(
        self,
        knowledge_point: str,
        question_type: str,
        difficulty: int
    ) -> Question:
        prompt = f"""
        请根据以下要求生成一道考试题:
        知识点: {knowledge_point}
        题型: {question_type}
        难度等级: {difficulty}/5
        
        返回JSON格式包含:
        1. content: 题目内容
        2. options: 选项列表(选择题必需)
        3. answer: 标准答案
        4. analysis: 解题思路
        """
        
        response = await self.client.generate_text(prompt)
        result = json.loads(response)
        
        return Question(
            id=str(uuid.uuid4()),
            type=question_type,
            content=result["content"],
            options=result.get("options"),
            answer=result["answer"],
            analysis=result["analysis"],
            difficulty=difficulty,
            knowledge_point=knowledge_point,
            score=self._calculate_score(question_type, difficulty)
        )
    
    async def __del__(self):
        await self.client.close()

    async def generate_exam(
        self,
        course_id: str,
        knowledge_points: List[str],
        question_config: Dict[str, int],  # {"选择题": 10, "填空题": 5}
        difficulty: int = 3
    ) -> Exam:
        """生成完整试卷"""
        questions = []
        total_score = 0
        
        # 生成每种类型的题目
        for q_type, count in question_config.items():
            for _ in range(count):
                k_point = random.choice(knowledge_points)
                question = await self._generate_question(k_point, q_type, difficulty)
                questions.append(question)
                total_score += question.score
        
        # 创建试卷
        return Exam(
            id=str(uuid.uuid4()),
            title=f"自动生成试卷-{datetime.now().strftime('%Y%m%d%H%M')}",
            course_id=course_id,
            total_score=total_score,
            duration=90,  # 默认90分钟
            questions=questions,
            created_at=datetime.now(),
            created_by="system"
        )