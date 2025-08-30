"""
Точка входа FastAPI-приложения.

Инициализирует приложение и подключает роутеры для вопросов и ответов.
"""

from __future__ import annotations

from fastapi import FastAPI

from app.routers import answers as answers_router
from app.routers import questions as questions_router

app = FastAPI(title="Q&A Service", version="1.0.0")

app.include_router(questions_router.router)
app.include_router(answers_router.router)
