"""
Модуль с моделью Question.

Содержит SQLAlchemy-модель для таблицы вопросов.
Используется для хранения и управления данными вопросов, а также
связанными с ними ответами (отношение один-ко-многим).
"""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Question(Base):
    """
    Модель для хранения вопросов.

    Args:
        id (int): Уникальный идентификатор вопроса;
        text (str): Текст вопроса;
        created_at (datetime): Дата и время создания;
        answers (list[Answer]): Связанные ответы на вопрос.
    """

    __tablename__ = "questions"
    __table_args__ = (
        # Запрет пустых строк/пробелов
        CheckConstraint(
            "btrim(text) <> ''", name="ck_questions_text_not_blank"
        ),
    )

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, index=True
    )
    text: Mapped[str] = mapped_column(sa.String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
