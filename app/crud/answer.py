"""
CRUD-операции для Answer.

Содержит функции для создания, получения и удаления ответов.
Проверка существования вопроса выполняется на уровне вызывающего слоя
(роутера/сервиса),чтобы корректно вернуть 404 при попытке добавить
ответ к несуществующему вопросу.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.answer import Answer


def create_answer(
    db: Session, *, question_id: int, user_id: str, text: str
) -> Answer:
    """
    Создать новый ответ.

    Args:
        db: Сессия БД.
        question_id: Идентификатор вопроса.
        user_id: UUID пользователя (строкой).
        text: Текст ответа.

    Returns:
        Созданный объект Answer.
    """
    obj = Answer(question_id=question_id, user_id=user_id, text=text)
    db.add(obj)
    db.flush()
    db.refresh(obj)
    return obj


def get_answer(db: Session, answer_id: int) -> Optional[Answer]:
    """
    Получить ответ по id.

    Args:
        db: Сессия БД.
        answer_id: Идентификатор ответа.

    Returns:
        Answer или None.
    """
    stmt = select(Answer).where(Answer.id == answer_id)
    return db.scalar(stmt)


def delete_answer(db: Session, answer_id: int) -> bool:
    """
    Удалить ответ по id.

    Args:
        db: Сессия БД.
        answer_id: Идентификатор ответа.

    Returns:
        True, если что-то удалено; False — если запись не найдена.
    """
    result = db.execute(delete(Answer).where(Answer.id == answer_id))
    return bool(getattr(result, "rowcount", 0))
