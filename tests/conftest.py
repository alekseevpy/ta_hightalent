"""
Фикстуры pytest:
    - Создание/инициализация тестовой БД в Postgres.
    - Транзакционная сессия SQLAlchemy для каждого теста
    (rollback по завершении).
    - TestClient FastAPI с переопределением зависимостей get_db/get_uow.
"""

from __future__ import annotations

import os
import re
from typing import Generator, Iterator

import pytest
import sqlalchemy as sa
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db import dependences as app_deps
from app.db.base import Base
from app.main import app


def _derive_test_url(url: str) -> str:
    """
    Построить URL тестовой БД из основного URL.
    """
    return re.sub(r"/([^/]+)$", r"/\1_test", url)


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """
    Получить URL тестовой БД из ENV (TEST_DATABASE_URL) или
    из основного DATABASE_URL.

    Returns:
        str: DSN вида postgresql+psycopg2://user:pass@host:port/dbname_test
    """
    url: str | None = os.getenv("TEST_DATABASE_URL")
    if url:
        return url
    from app.core.config import (
        settings,  # локальный импорт, чтобы .env считался корректно
    )

    return _derive_test_url(settings.database_url)


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_db(test_database_url: str) -> Iterator[None]:
    """
    Создать тестовую БД (если отсутствует) и применить схему через
    Base.metadata.create_all.
    Используем AUTOCOMMIT на системной БД для CREATE DATABASE.
    """
    admin_url: str = re.sub(r"/([^/]+)$", "/postgres", test_database_url)
    admin_engine: Engine = sa.create_engine(
        admin_url, isolation_level="AUTOCOMMIT", future=True
    )
    db_name_match = re.search(r"/([^/]+)$", test_database_url)
    assert (
        db_name_match is not None
    ), "Не удалось определить имя тестовой БД из URL"
    db_name: str = db_name_match.group(1)

    with admin_engine.connect() as conn:
        exists: bool = bool(
            conn.execute(
                sa.text("SELECT 1 FROM pg_database WHERE datname=:n"),
                {"n": db_name},
            ).scalar()
        )
        if not exists:
            conn.execute(sa.text(f'CREATE DATABASE "{db_name}"'))

    engine: Engine = sa.create_engine(test_database_url, future=True)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def db_session(test_database_url: str) -> Iterator[Session]:
    """
    Выдать транзакционную сессию SQLAlchemy для изоляции теста:
      - Открываем соединение и начинаем транзакцию.
      - Привязываем к ней Session.
      - По завершении теста — делаем rollback и закрываем соединение.

    Returns:
        Iterator[Session]: Сессия SQLAlchemy, обёрнутая в транзакцию.
    """
    engine: Engine = sa.create_engine(test_database_url, future=True)
    TestingSessionLocal: sessionmaker[Session] = sessionmaker(
        bind=engine, autoflush=False, autocommit=False, class_=Session
    )
    connection = engine.connect()
    trans = connection.begin()

    session: Session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Вернуть TestClient FastAPI с переопределённым
    зависимостями get_db и get_uow, указывающими на одну
    и ту же транзакционную сессию (rollback в фикстуре).
    """

    def _get_db_override() -> Iterator[Session]:
        """
        Переопределение зависимость для read-only эндпоинтов (без коммита).
        """
        try:
            yield db_session
        finally:
            pass

    def _get_uow_override() -> Iterator[Session]:
        """
        Переопределение зависимости Unit of Work для write-эндпоинтов.
        Коммит не вызываем — фиксируем откат в рамках общей транзакции теста.
        """
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[app_deps.get_db] = _get_db_override
    app.dependency_overrides[app_deps.get_uow] = _get_uow_override

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
