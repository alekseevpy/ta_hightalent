"""
CRUD-операции для Question.

Содержит функции для создания, получения, перечисления и удаления вопросов.
Удаление вопросов приводит к каскадному удалению ответов на уровне БД.
"""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload

from app.models.question import Question


def create_question(db: Session, *, text: str) -> Question:
    """
    Создать новый вопрос.

    Args:
        db: Сессия БД.
        text: Текст вопроса.

    Returns:
        Созданный объект Question.
    """
    obj = Question(text=text)
    db.add(obj)
    db.flush()
    db.refresh(obj)
    return obj


def get_question(
    db: Session, question_id: int, *, with_answers: bool = False
) -> Optional[Question]:
    """
    Получить вопрос по id.

    Args:
        db: Сессия БД.
        question_id: Идентификатор вопроса.
        with_answers: Если True — подгружает ответы (joinedload).

    Returns:
        Question или None.
    """
    stmt = select(Question).where(Question.id == question_id)
    if with_answers:
        stmt = stmt.options(joinedload(Question.answers))
    return db.scalar(stmt)


def list_questions(
    db: Session, *, limit: int = 100, offset: int = 0
) -> List[Question]:
    """
    Получить список вопросов.

    Args:
        db: Сессия БД.
        limit: Максимум записей.
        offset: Смещение.

    Returns:
        Список Question.
    """
    stmt = (
        select(Question)
        .order_by(Question.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.scalars(stmt))


def delete_question(db: Session, question_id: int) -> bool:
    """
    Удалить вопрос по id (каскадно удалит ответы на уровне БД).

    Args:
        db: Сессия БД.
        question_id: Идентификатор вопроса.

    Returns:
        True, если что-то удалено; False — если запись не найдена.
    """
    result = db.execute(delete(Question).where(Question.id == question_id))
    return bool(getattr(result, "rowcount", 0))
