from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import Tool
from typing import List, Dict
import random
import json
from datetime import datetime
import re
from backend.app.schemas.exam import QuestionCreate, Exam, ExamCreate  # 路径根据你的实际项目结构调整
from utils.model_client import ChatGLMClient

def extract_json_from_codeblock(text: str) -> str:
    print("ai_agents/teacher/exam_generation/exam_generator.py的extract_json_from_codeblock在工作")
    # match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    # if match:
    #     return match.group(1)
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return text.strip()

class ExamGeneratorAgent:
    def __init__(self):
        self.client = ChatGLMClient()
    
    async def _generate_question(
        self,
        knowledge_point: str,
        question_type: str,
        difficulty: int
    ) -> QuestionCreate:
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
        print("ai_agents/teacher/exam_generation/exam_generator.py的_generate_question在工作")
        response = await self.client.generate_text(prompt)
        json_str = extract_json_from_codeblock(response)
        print("大模型返回的json_str:", json_str)
        if not json_str.startswith("{"):
            print("警告：大模型返回内容不是JSON对象！内容如下：", json_str)
        try:
            result = json.loads(json_str)
        except Exception as e:
            print("解析JSON失败:", e)
            #raise
        # 处理 options 字段
        options = result.get("options")
        if options and isinstance(options, list) and isinstance(options[0], dict):
            # 转换为 ["A. xxx", ...] 形式
            options = [f"{opt.get('label', chr(65+i))}. {opt.get('text', '')}" for i, opt in enumerate(options)]
        else:
            # 保持原样
            options = options
        
        # return Question(
        #     id=None,
        #     type=question_type,
        #     content=result["content"],
        #     options=result.get("options"),
        #     answer=result["answer"],
        #     analysis=result.get("analysis"),
        #     difficulty=difficulty,
        #     knowledge_point=knowledge_point,
        #     score=int(result.get("score", 5)),  # 默认5分
        #     exam_id=None
        # )
        return QuestionCreate(
            id=None,
            type=question_type,
            content=result["content"],
            options=options,
            answer=result["answer"],
            analysis=result.get("analysis"),
            difficulty=difficulty,
            knowledge_point=knowledge_point,
            score=int(result.get("score", 5)),
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
        print("ai_agents/teacher/exam_generation/exam_generator.py的_generate_exam在工作")
        for q_type, count in question_config.items():
            for _ in range(count):
                k_point = random.choice(knowledge_points)
                question = await self._generate_question(k_point, q_type, difficulty)
                questions.append(question)
                total_score += question.score
        # return Exam(
        #     id=None,
        #     title=f"自动生成试卷-{datetime.now().strftime('%Y%m%d%H%M')}",
        #     course_id=course_id,
        #     total_score=total_score,
        #     duration=duration,
        #     questions=questions,
        #     created_at=datetime.now(),
        #     created_by=created_by,
        #     status="draft"
        # )
        return ExamCreate(
            id=None,
            title=f"自动生成试卷-{datetime.now().strftime('%Y%m%d%H%M')}",
            course_id=course_id,
            total_score=total_score,
            duration=duration,
            questions=questions,  # 这里是 List[QuestionCreate]
            created_at=datetime.now(),
            created_by=created_by,
            status="draft"
        )
