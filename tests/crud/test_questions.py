"""
CRUD-тесты для Question: создание/список и каскадное удаление.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud import answer as a_crud
from app.crud import question as q_crud
from tests.utils.helpers import to_uuid


def test_create_and_list(db_session: Session) -> None:
    """
    Проверить создание вопроса и появление в выдаче list_questions.
    """
    q = q_crud.create_question(db_session, text="Q")
    db_session.commit()

    items = q_crud.list_questions(db_session)
    assert any(x.id == q.id for x in items)


def test_delete_cascade(db_session: Session) -> None:
    """
    Проверить каскадное удаление ответов при удалении вопроса.
    """
    q = q_crud.create_question(db_session, text="Q")
    a1 = a_crud.create_answer(
        db_session, question_id=q.id, user_id=to_uuid("u"), text="A1"
    )
    a2 = a_crud.create_answer(
        db_session, question_id=q.id, user_id=to_uuid("u2"), text="A2"
    )
    db_session.commit()

    # Сохраняем первичные ключи ДО удаления и коммитов,
    # чтобы не трогать удалённые экземпляры ORM.
    a1_id = a1.id
    a2_id = a2.id

    deleted: bool = q_crud.delete_question(db_session, q.id)
    db_session.commit()
    assert deleted is True

    assert a_crud.get_answer(db_session, a1_id) is None
    assert a_crud.get_answer(db_session, a2_id) is None
