FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==$POETRY_VERSION && \
    addgroup --system appgroup && adduser --system --ingroup appgroup appuser && \
    adduser --system --ingroup appgroup user

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

# ---- development stage ----
FROM base AS dev
RUN poetry install --no-interaction --no-ansi --no-root
COPY src/ ./src/
RUN chown -R user:appgroup /app
USER user
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---- production stage ----
FROM base AS prod
RUN poetry install --no-interaction --no-ansi --only main --no-root
COPY src/ ./src/
RUN chown -R appuser:appgroup /app
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
