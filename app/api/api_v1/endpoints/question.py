from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.api import deps
from app.models.user import User
from fastapi.encoders import jsonable_encoder
from app.models import Question

router = APIRouter()

# Get all questions 
@router.get("/questions", response_model=dict)
def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    total = db.query(Question).count()
    items = crud.question.get_multi(db, skip=skip, limit=limit)
    return {"items": jsonable_encoder(items), "total": total}

# Create a new question
@router.post("/questions", response_model=schemas.Question)
def create_question(q: schemas.QuestionCreate, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user)):
    return crud.question.create_question(
        db=db,
        user_id=current_user.id,
        title=q.title,
        description=q.description,
        email=current_user.email,
        role=current_user.role
    )

# Get a single question
@router.get("/questions/{question_id}", response_model=schemas.Question)
def get_question(question_id: int, db: Session = Depends(deps.get_db)):
    question = crud.question.get(db, id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# Reply to a question
@router.post("/questions/{question_id}/responses", response_model=schemas.QuestionResponse)
def create_response(
    question_id: int,
    r: schemas.QuestionResponseCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_t_admin)  # 只允许 t-admin 回答
):
    return crud.question_response.create_response(db=db, question_id=question_id, responder_id=current_user.id, content=r.content)

# Get all responses to a question
@router.get("/questions/{question_id}/responses", response_model=List[schemas.QuestionResponse])
def get_responses(question_id: int, db: Session = Depends(deps.get_db)):
    return crud.question_response.get_by_question(db=db, question_id=question_id) 