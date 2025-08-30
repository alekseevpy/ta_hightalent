"""
Тесты схем ответов: UUID passthrough и конвертация строк в UUID5.
"""

from __future__ import annotations

import uuid

import pytest

from app.schemas.answer import AnswerCreate


def test_answer_create_uuid_passthrough() -> None:
    """
    Проверить, что валидный UUID сохраняется
    (нормализуется к нижнему регистру).
    """
    u = "00000000-0000-0000-0000-000000000001"
    a = AnswerCreate(user_id=u, text="ok")
    assert a.user_id == u


def test_answer_create_string_to_uuid5() -> None:
    """
    Проверить, что произвольная строка конвертируется в стабильный UUID5.
    """
    a = AnswerCreate(user_id="firstuser", text="ok")
    generated = uuid.UUID(a.user_id)
    assert str(generated) == a.user_id
    again = AnswerCreate(user_id="firstuser", text="ok")
    assert again.user_id == a.user_id


@pytest.mark.parametrize("bad", ["", "   "])
def test_answer_create_blank_text_rejected(bad: str) -> None:
    """
    Проверить, что пустой текст отклоняется валидатором.
    """
    with pytest.raises(Exception):
        AnswerCreate(user_id="firstuser", text=bad)
