"""
Модуль инициализации базы данных.

Содержит:
    - объект 'engine' для подключения к PostgreSQL;
    - 'SessionLocal' для создания сессий работы с БД;
    - базовый класс 'Base' для описания моделей.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
