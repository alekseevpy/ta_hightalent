"""
CRUD-тесты для Answer: создание, получение и удаление.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud import answer as a_crud
from app.crud import question as q_crud
from tests.utils.helpers import to_uuid


def test_create_get_delete_answer(db_session: Session) -> None:
    """
    Проверить жизненный цикл ответа (create - get - delete).
    """
    q = q_crud.create_question(db_session, text="Q")
    db_session.commit()

    ans = a_crud.create_answer(
        db_session,
        question_id=q.id,
        user_id=to_uuid("firstuser"),
        text="A",
    )
    db_session.commit()

    got = a_crud.get_answer(db_session, ans.id)
    assert got is not None
    assert got.text == "A"

    deleted: bool = a_crud.delete_answer(db_session, ans.id)
    db_session.commit()
    assert deleted is True
    assert a_crud.get_answer(db_session, ans.id) is None
