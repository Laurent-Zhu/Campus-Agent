from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from models.exam import Exam, Question
from ai_agents.teacher.exam_generation.exam_generator import ExamGeneratorAgent
from backend.dependencies import get_current_teacher, get_llm

router = APIRouter()

class ExamGenerateRequest(BaseModel):
    course_id: str
    knowledge_points: List[str]
    question_config: Dict[str, int]
    difficulty: int = 3
    duration: int = 90

@router.post("/exams/generate", response_model=Exam)
async def generate_exam(
    request: ExamGenerateRequest,
    current_teacher = Depends(get_current_teacher),
    llm = Depends(get_llm)
):
    """生成考试试卷"""
    try:
        generator = ExamGeneratorAgent(llm=llm)
        
        exam = await generator.generate_exam(
            course_id=request.course_id,
            knowledge_points=request.knowledge_points,
            question_config=request.question_config,
            difficulty=request.difficulty
        )
        
        # 更新创建者信息
        exam.created_by = current_teacher.id
        exam.duration = request.duration
        
        # TODO: 保存到数据库
        
        return exam
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))