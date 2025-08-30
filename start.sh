#!/usr/bin/env bash
set -e

echo "Waiting for Postgres at host db:5432..."
until nc -z db 5432; do
  sleep 0.5
done
echo "Postgres is up."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000