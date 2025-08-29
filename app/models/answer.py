"""
Модуль с моделью Answer.

Содержит SQLAlchemy-модель для таблицы ответов.
Используется для хранения ответов пользователей на конкретные вопросы,
а также для связи с таблицей вопросов (отношение многие-к-одному).
"""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Answer(Base):
    """
    Модель для хранения ответов.

    Args:
        id (int): Уникальный идентификатор ответа;
        question_id (int): ID связанного вопроса (внешний ключ);
        user_id (str): Идентификатор пользователя, оставившего ответ;
        text (str): Текст ответа (не может быть пустым);
        created_at (datetime): Дата и время создания ответа;
        question (Question): Объект связанного вопроса.
    """

    __tablename__ = "answers"
    __table_args__ = (
        CheckConstraint("btrim(text) <> ''", name="ck_answers_text_not_blank"),
        sa.Index("ix_answers_question_created", "question_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, index=True
    )

    question_id: Mapped[int] = mapped_column(
        sa.ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # В API - строка, в БД — UUID
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False)
    text: Mapped[str] = mapped_column(sa.String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    question: Mapped["Question"] = relationship(back_populates="answers")
