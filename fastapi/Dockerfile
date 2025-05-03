# Используем Python как базовый образ
FROM python:3.11 AS backend

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы проекта для бэкенда
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости бэкенда
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копируем папку фронтенда
COPY app/frontend/test-app /app/frontend/test-app

# Устанавливаем Node.js и npm
RUN apt-get update && apt-get install -y nodejs npm

# Удаляем node_modules и package-lock.json перед установкой
WORKDIR /app/frontend/test-app
RUN rm -rf node_modules package-lock.json

# Устанавливаем зависимости фронтенда
RUN npm install

# Собираем фронтенд
RUN npm run build

# Возвращаемся в основную папку
WORKDIR /app

# Устанавливаем библиотеку для работы с RabbitMQ
RUN pip install aio-pika

# Запускаем бекенд и фронтенд
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & serve -s /app/frontend/test-app/build -l 3000"]
