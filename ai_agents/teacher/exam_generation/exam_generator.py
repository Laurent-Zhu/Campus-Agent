from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from typing import List, Dict
import random
import json
from datetime import datetime

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
        5. score: 分值
        """
        response = await self.client.generate_text(prompt)
        result = json.loads(response)
        return Question(
            id=None,
            type=question_type,
            content=result["content"],
            options=result.get("options"),
            answer=result["answer"],
            analysis=result.get("analysis"),
            difficulty=difficulty,
            knowledge_point=knowledge_point,
            score=int(result.get("score", 5)),  # 默认5分
            exam_id=None
        )

    async def generate_exam(
        self,
        course_id: int,
        knowledge_points: List[str],
        question_config: Dict[str, int],
        difficulty: int = 3,
        duration: int = 90,
        created_by: int = None
    ) -> Exam:
        questions = []
        total_score = 0
        for q_type, count in question_config.items():
            for _ in range(count):
                k_point = random.choice(knowledge_points)
                question = await self._generate_question(k_point, q_type, difficulty)
                questions.append(question)
                total_score += question.score
        return Exam(
            id=None,
            title=f"自动生成试卷-{datetime.now().strftime('%Y%m%d%H%M')}",
            course_id=course_id,
            total_score=total_score,
            duration=duration,
            questions=questions,
            created_at=datetime.now(),
            created_by=created_by,
            status="draft"
        )