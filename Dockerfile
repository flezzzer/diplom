FROM python:3.11

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY fastapi/pyproject.toml fastapi/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY app /app/app

ENV PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
