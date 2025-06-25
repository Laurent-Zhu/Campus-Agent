from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from ...core.deps import get_db, get_current_user
from ...schemas.exam import ExamCreate, Exam, ExamGenerateRequest, ExamUpdate
from ...services.exam_service import ExamGenerator
from ...models.exam import Exam as ExamModel, Question as QuestionModel
from ...models.user import User
from .....ai_agents.factory import AgentFactory
import datetime

router = APIRouter()

@router.post("/generate", response_model=ExamCreate)
async def generate_exam(
    request: ExamGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """生成考试题目"""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="只有教师可以生成考试"
        )
    
    try:
        # 创建考试生成智能体
        agent = AgentFactory.create_agent("exam_generator")
        if not agent:
            raise ValueError("创建智能体失败")
        
        # 生成试题
        questions = await agent.arun(
            course=request.course_id,
            knowledge_points=request.knowledge_points,
            question_types=request.question_types,
            difficulty=request.difficulty
        )
        
        # 创建考试
        exam = ExamCreate(
            title=f"AI生成的考试-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            description="基于知识点智能生成的试卷",
            course_id=request.course_id,
            questions=questions,
            total_score=sum(q["score"] for q in questions),
            duration=120  # 默认120分钟
        )
        
        return exam
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成考试失败: {str(e)}"
        )

@router.post("/", response_model=Exam)
async def create_exam(
    exam: ExamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """保存考试"""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403,
            detail="只有教师可以创建考试"
        )
    
    try:
        db_exam = ExamModel(
            **exam.dict(exclude={"questions"}),
            created_by=current_user.id,
            status="draft"
        )
        db.add(db_exam)
        db.commit()
        db.refresh(db_exam)
        
        # 添加题目
        for q in exam.questions:
            db_question = QuestionModel(
                **q.dict(),
                exam_id=db_exam.id
            )
            db.add(db_question)
        
        db.commit()
        return db_exam
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"创建考试失败: {str(e)}"
        )

@router.get("/{exam_id}", response_model=Exam)
async def get_exam(
    exam_id: int = Path(..., title="考试ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取考试详情"""
    exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="考试不存在")
    
    if exam.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权访问此考试")
    
    return exam

@router.put("/{exam_id}", response_model=Exam)
async def update_exam(
    exam_id: int,
    exam_update: ExamUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新考试"""
    db_exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="考试不存在")
    
    if db_exam.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="只有创建者可以修改考试")
    
    try:
        for key, value in exam_update.dict(exclude_unset=True).items():
            setattr(db_exam, key, value)
        
        db.commit()
        db.refresh(db_exam)
        return db_exam
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"更新考试失败: {str(e)}"
        )

@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除考试"""
    db_exam = db.query(ExamModel).filter(ExamModel.id == exam_id).first()
    if not db_exam:
        raise HTTPException(status_code=404, detail="考试不存在")
    
    if db_exam.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="只有创建者可以删除考试")
    
    try:
        db.delete(db_exam)
        db.commit()
        return {"message": "考试已删除"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"删除考试失败: {str(e)}"
        )