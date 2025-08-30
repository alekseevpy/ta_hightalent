"""
Маршруты для работы с ответами.

Реализует эндпоинты:
    - POST /questions/{id}/answers/ — добавить ответ к вопросу;
    - GET /answers/{id} — получить конкретный ответ;
    - DELETE /answers/{id} — удалить ответ.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import answer as a_crud
from app.crud import question as q_crud
from app.db.dependences import get_db, get_uow
from app.schemas.answer import AnswerCreate, AnswerOut

router = APIRouter(tags=["Answers"])


@router.post(
    "/questions/{question_id}/answers/",
    response_model=AnswerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_answer_for_question(
    question_id: int,
    payload: AnswerCreate,
    db: Session = Depends(get_uow),
):
    """
    Добавить ответ к вопросу. Если вопрос не существует — вернуть 404.
    """
    if not q_crud.get_question(db, question_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    obj = obj = a_crud.create_answer(
        db, question_id=question_id, user_id=payload.user_id, text=payload.text
    )
    return obj


@router.get("/answers/{answer_id}", response_model=AnswerOut)
def get_answer(answer_id: int, db: Session = Depends(get_db)):
    """
    Получить ответ по id.
    """
    obj = a_crud.get_answer(db, answer_id)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    return obj


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_uow)):
    """
    Удалить ответ по id.
    """
    deleted = a_crud.delete_answer(db, answer_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    return None
