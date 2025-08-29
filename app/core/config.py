"""
Модуль конфигурации приложения.

- Считывает переменные окружения из '.env' и предоставляет
объект настроек 'settings'.
- Используется для доступа к параметрам подключения к БД и
другим конфигам проекта.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
