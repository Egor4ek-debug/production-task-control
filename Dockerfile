FROM python:3.13-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
 && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копируем только манифесты для кеширования зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости без dev‑группы и без попытки установить сам проект
RUN poetry config virtualenvs.create false \
 && poetry install --only main --no-interaction --no-ansi --verbose --no-root

# Копируем всё приложение
COPY . /app

ENV PYTHONUNBUFFERED=1 \
    ENV=prod \
    DATABASE_URL=postgresql+asyncpg://postgres:admin@db:5432/task_control

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
