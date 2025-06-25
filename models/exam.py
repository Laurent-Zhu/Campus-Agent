from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Question(BaseModel):
    """题目模型"""
    id: str
    type: str  # 选择题/填空题/简答题/编程题
    content: str
    options: Optional[List[str]]  # 选择题选项
    answer: str
    analysis: str
    difficulty: int = Field(ge=1, le=5)  # 难度1-5
    knowledge_point: str
    score: int

class Exam(BaseModel):
    """试卷模型"""
    id: str
    title: str
    description: Optional[str]
    course_id: str
    total_score: int
    duration: int  # 考试时长(分钟)
    questions: List[Question]
    created_at: datetime
    created_by: str
    status: str = "draft"  # draft/published