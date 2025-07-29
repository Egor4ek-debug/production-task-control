FROM python:3.13-slim

# Устанавливаем Poetry
ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y curl build-essential libpq-dev && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s ~/.local/bin/poetry /usr/local/bin/poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости
RUN poetry install --no-root --only main

# Копируем остальной код
COPY . /app

# Запускаем приложение
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]