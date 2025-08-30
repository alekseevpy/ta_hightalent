"""
Тесты схем вопроса: строгая валидация пробельных строк.
"""

from __future__ import annotations

import pytest

from app.schemas.question import QuestionCreate


def test_question_create_valid() -> None:
    """
    Проверить нормализацию текста и корректность результата.
    """
    q = QuestionCreate(text="  Привет  ")
    assert q.text == "Привет"


@pytest.mark.parametrize("bad", ["", "   "])
def test_question_create_blank_rejected(bad: str) -> None:
    """
    Проверить, что пустые/пробельные строки отклоняются валидатором.
    """
    with pytest.raises(Exception):
        QuestionCreate(text=bad)
