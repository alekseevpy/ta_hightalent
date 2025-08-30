"""
API-тесты ответов: 404 при несуществующем вопросе, получение и удаление.
"""

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient


def test_create_answer_to_missing_question_returns_404(
    client: TestClient,
) -> None:
    """
    Проверить 404 при создании ответа на несуществующий вопрос.
    """
    r = client.post(
        "/questions/999999/answers/", json={"user_id": "u", "text": "A"}
    )
    assert r.status_code == 404


def test_get_and_delete_answer(client: TestClient) -> None:
    """
    Проверить создание, чтение и удаление ответа.
    """
    q = client.post("/questions/", json={"text": "Q"}).json()
    a = client.post(
        f"/questions/{q['id']}/answers/",
        json={"user_id": "u", "text": "A"},
    ).json()

    r = client.get(f"/answers/{a['id']}")
    assert r.status_code == 200
    fetched: dict[str, Any] = r.json()
    assert fetched["text"] == "A"

    r = client.delete(f"/answers/{a['id']}")
    assert r.status_code == 204

    r = client.get(f"/answers/{a['id']}")
    assert r.status_code == 404
