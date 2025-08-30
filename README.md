# API-сервис "Вопросы и Ответы"

Исполнитель: **Алексеев Лев, tg: @lsalekseev**  

Тестовое задание для демонстрации навыков разработки backend-приложений на FastAPI с использованием PostgreSQL, SQLAlchemy, Alembic и Docker.

---

## Использованный стек

- **Язык:** Python 3.11  
- **Фреймворк:** FastAPI  
- **База данных:** PostgreSQL 16  
- **ORM:** SQLAlchemy 2.x  
- **Миграции:** Alembic  
- **Валидация:** Pydantic v2  
- **Инфраструктура:** Docker, docker-compose 
- **Тестирование:** pytest  
- **Линтеры и форматтеры:** black, isort, flake8

---

## Реализовано

- REST API с CRUD-операциями:
  - **Вопросы**:
    - `GET /questions/` — список всех вопросов
    - `POST /questions/` — создать новый вопрос
    - `GET /questions/{id}` — получить вопрос и все ответы на него
    - `DELETE /questions/{id}` — удалить вопрос с каскадным удалением всех ответов
  - **Ответы**:
    - `POST /questions/{id}/answers/` — добавить ответ к вопросу
    - `GET /answers/{id}` — получить конкретный ответ
    - `DELETE /answers/{id}` — удалить ответ
- Каскадное удаление всех ответов при удалении вопроса.
- Полная валидация входных данных через Pydantic.
- Разделение кода на слои:
  - `models` — SQLAlchemy-модели
  - `schemas` — Pydantic-схемы
  - `crud` — бизнес-логика
  - `routers` — маршруты API
  - `core` — конфигурация и утилиты
- Автоматизированные миграции Alembic.
- Unit-тесты CRUD и API с использованием тестовой базы.
- Docker-окружение с Postgres и приложением.
- Автоматический прогон миграций при старте контейнера.

---

## Запуск с использованием Docker

1. Склонировать проект:
   ```bash
   git clone https://github.com/alekseevpy/ta_hitalent.git

2. Запустить контейнеры:
    ```bash
    docker compose --env-file .env.docker up --build -d

3. Открыть документацию:
    ```bash
    http://127.0.0.1:8000/docs
