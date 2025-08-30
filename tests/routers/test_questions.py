"""
API-тесты вопросов: создание, список, деталка, каскадное удаление.
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def test_create_and_list_questions(client: TestClient) -> None:
    """
    Проверить создание вопроса и наличие в списке.
    """
    r = client.post("/questions/", json={"text": "Ваш любимый язык?"})
    assert r.status_code == 201, r.text
    created: dict[str, Any] = r.json()
    assert created["text"] == "Ваш любимый язык?"

    r = client.get("/questions/")
    assert r.status_code == 200
    items: list[dict[str, Any]] = r.json()
    assert any(i["id"] == created["id"] for i in items)


def test_get_question_with_answers(client: TestClient) -> None:
    """
    Проверить детальный GET вопроса с вложенными ответами.
    """
    q = client.post("/questions/", json={"text": "Q1"}).json()
    a_resp = client.post(
        f"/questions/{q['id']}/answers/",
        json={"user_id": "firstuser", "text": "A1"},
    )
    assert a_resp.status_code == 201, a_resp.text

    r = client.get(f"/questions/{q['id']}")
    assert r.status_code == 200
    data: dict[str, Any] = r.json()
    assert data["id"] == q["id"]
    assert isinstance(data["answers"], list)
    assert len(data["answers"]) == 1


def test_delete_question_cascade(client: TestClient) -> None:
    """
    Проверить каскадное удаление ответов при удалении вопроса.
    """
    q = client.post("/questions/", json={"text": "Q2"}).json()
    client.post(
        f"/questions/{q['id']}/answers/", json={"user_id": "u1", "text": "A1"}
    )
    client.post(
        f"/questions/{q['id']}/answers/", json={"user_id": "u2", "text": "A2"}
    )

    r = client.delete(f"/questions/{q['id']}")
    assert r.status_code == 204

    r = client.get(f"/questions/{q['id']}")
    assert r.status_code == 404
