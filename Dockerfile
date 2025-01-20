# -----------------------
# Шаг 1: Сборка (builder)
# -----------------------
FROM python:3.11-slim-bullseye AS builder

# Чтобы Python не создавал .pyc файлы и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем системные пакеты, необходимые для сборки некоторых зависимостей
# build-essential и т.д. 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Скопируем файл зависимостей отдельно, чтобы Docker мог воспользоваться кешем
COPY requirements.txt .

# Устанавливаем зависимости в отдельный путь --prefix=/install
# Опция --no-cache-dir уменьшает размер образа за счёт отказа от кеша pip
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# Теперь копируем всё приложение (при условии, что у нас в корне проекта лежит директория app)
COPY . /app

# -----------------------
# Шаг 2: Финальный образ
# -----------------------
FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создадим нового пользователя (не root) для лучшей безопасности
RUN addgroup --system fastapi && adduser --system --ingroup fastapi fastapi

WORKDIR /app

# Скопируем из builder только установленные зависимости
COPY --from=builder /install /usr/local

# Скопируем сам код приложения
COPY . /app

# Переключаемся на пользователя fastapi
USER fastapi

# Запуск приложения
# Предполагается, что входная точка — main.py c объектом FastAPI под именем "app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
