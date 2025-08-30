"""
Зависимости для доступа к базе данных.

Содержит два провайдера сессий:
    - get_db()  — read-only: отдаёт сессию без автокоммита (для GET);
    - get_uow() — unit of work: коммитит на успехе, делает rollback при
    исключении (для POST/PUT/PATCH/DELETE).
"""

from __future__ import annotations

from typing import Iterator

from sqlalchemy.orm import Session

from app.db.base import SessionLocal


def get_db() -> Iterator[Session]:
    """
    Отдаёт сессию SQLAlchemy для операций чтения.

    Сессия не выполняет автоматический commit. Используется в обработчиках,
    где не предполагается изменение данных (GET).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_uow() -> Iterator[Session]:
    """
    Unit of Work: сессия для операций записи.

    Коммитит при успешном завершении запроса; при исключении откатывает
    транзакцию. Используется в write-эндпоинтах (POST/PUT/PATCH/DELETE).
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
