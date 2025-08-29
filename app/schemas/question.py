"""
Pydantic-схемы для работы с Question.

Содержит модели для создания вопроса, отдачи списка вопросов и детального
представления вопроса с вложенными ответами. Включает строгую валидацию:
    - text триммится и не может быть пустым;
    - длина ограничена (<= 500) в соответствии с моделью БД.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator
from pydantic.config import ConfigDict

from app.schemas.answer import AnswerShortOut


class QuestionCreate(BaseModel):
    """
    Модель тела запроса для создания вопроса.

    Args:
        text (str): Текст вопроса (обязателен, непустой, <= 500 символов).
    """

    text: str = Field(..., max_length=500, description="Текст вопроса")

    @field_validator("text")
    @classmethod
    def strip_and_non_blank(cls, v: str) -> str:
        """Обрезаем пробелы; запрещаем пустую строку."""
        vv = v.strip()
        if not vv:
            raise ValueError("text must not be blank")
        return vv


class QuestionListItem(BaseModel):
    """
    Элемент списка вопросов.
    """

    id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class QuestionDetail(BaseModel):
    """
    Детальное представление вопроса c вложенными ответами.

    Args:
        id (int): Идентификатор вопроса.
        text (str): Текст вопроса.
        created_at (datetime): Время создания.
        answers (List[AnswerShortOut]): Список связанных ответов.
    """

    id: int
    text: str
    created_at: datetime
    answers: List[AnswerShortOut] = []

    model_config = ConfigDict(from_attributes=True)
