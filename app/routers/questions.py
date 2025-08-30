"""
Маршруты для работы с вопросами.

Реализует эндпоинты:
    - GET /questions/ — список вопросов;
    - POST /questions/ — создать вопрос;
    - GET /questions/{id} — получить вопрос с ответами;
    - DELETE /questions/{id} — удалить вопрос (каскадно удалит ответы).
"""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import question as q_crud
from app.db.dependences import get_db, get_uow
from app.schemas.question import (
    QuestionCreate,
    QuestionDetail,
    QuestionListItem,
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/", response_model=List[QuestionListItem])
def list_questions(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_db)
):
    """
    Список вопросов. Поддерживает простую пагинацию.
    """
    items = q_crud.list_questions(db, limit=limit, offset=offset)
    return items


@router.post(
    "/", response_model=QuestionDetail, status_code=status.HTTP_201_CREATED
)
def create_question(payload: QuestionCreate, db: Session = Depends(get_uow)):
    """
    Создать новый вопрос.
    """
    obj = q_crud.create_question(db, text=payload.text)
    return obj


@router.get("/{question_id}", response_model=QuestionDetail)
def get_question(question_id: int, db: Session = Depends(get_db)):
    """
    Получить вопрос по id вместе с ответами.
    """
    obj = q_crud.get_question(db, question_id, with_answers=True)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return obj


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_uow)):
    """
    Удалить вопрос по id. Связанные ответы будут удалены каскадно на уровне БД.
    """
    deleted = q_crud.delete_question(db, question_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return None
