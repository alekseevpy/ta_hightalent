"""
Pydantic-схемы для работы с Answer.

Содержит модели валидации входных данных для создания ответа и модели
для формирования ответов API. Выполнена строгая валидация:
    - text триммится и не может быть пустой строкой;
    - user_id:
        * если корректный UUID — нормализуется к нижнему регистру;
        * если произвольная строка — генерируется детерминированный
        UUID5 на её основе.
    - включён режим from_attributes для удобной сериализации из ORM.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic.config import ConfigDict


class AnswerCreate(BaseModel):
    """
    Модель тела запроса для создания ответа.

    Args:
        user_id (str): Идентификатор пользователя:
            * валидный UUID - нормализуется;
            * произвольная строка - конвертируется в UUID5;
        text (str): Текст ответа (обязателен, непустой, <= 1000 символов).
    """

    user_id: str = Field(..., description="UUID пользователя или любая строка")
    text: str = Field(..., max_length=1000, description="Текст ответа")

    @field_validator("user_id")
    @classmethod
    def normalize_or_generate_uuid(cls, v: str) -> str:
        """
        Нормализует user_id к UUID:
            - если передан валидный UUID, то приводит к нижнему регистру;
            - если строка не UUID, то генерирует стабильный UUID5 на её основе.
        """
        vv = v.strip()
        if not vv:
            raise ValueError("user_id must not be blank")
        try:
            return str(uuid.UUID(vv)).lower()
        except ValueError:
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, vv)).lower()

    @field_validator("text")
    @classmethod
    def strip_and_non_blank(cls, v: str) -> str:
        """
        Обрезаем пробелы;
        запрещаем пустую строку.
        """
        vv = v.strip()
        if not vv:
            raise ValueError("text must not be blank")
        return vv


class AnswerOut(BaseModel):
    """
    Модель ответа API с полным описанием ответа.

    Args:
        id (int): Идентификатор ответа;
        question_id (int): Идентификатор вопроса;
        user_id (str): UUID пользователя (нормализованный);
        text (str): Текст ответа;
        created_at (datetime): Время создания.
    """

    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnswerShortOut(BaseModel):
    """
    Компактная модель ответа (без question_id) для вложенных списков
    внутри вопроса.
    """

    id: int
    user_id: str
    text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
