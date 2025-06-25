from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class QuestionBase(BaseModel):
    type: str
    content: str
    options: Optional[List[str]] = None
    answer: str
    analysis: Optional[str] = None
    score: int
    knowledge_point: str
    difficulty: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    exam_id: int
    
    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: int
    duration: int
    total_score: int

class ExamCreate(ExamBase):
    questions: List[QuestionCreate]

class Exam(ExamBase):
    id: int
    created_by: int
    created_at: datetime
    status: str
    questions: List[Question]
    
    class Config:
        from_attributes = True

class ExamGenerateRequest(BaseModel):
    course_id: int
    knowledge_points: List[str]
    question_types: dict  # {"choice": 5, "completion": 3, "programming": 2}
    difficulty: int  # 1-5