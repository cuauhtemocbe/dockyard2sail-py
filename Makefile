IMAGE = dockyard2sail-py

# --- Docker ---
build:
	docker compose build

up:
	docker compose up

up-d:
	docker compose up -d --wait

down:
	docker compose down

logs:
	docker compose logs -f api

# --- Tests en container (requiere el servicio arriba, lo levanta si hace falta) ---
test: up-d
	docker compose exec api pytest --cov=app --cov-report=term-missing

test-v: up-d
	docker compose exec api pytest -v

# --- Lint en container ---
lint: up-d
	docker compose exec api ruff check src/ tests/

format-check: up-d
	docker compose exec api ruff format --check src/ tests/

# --- Local (requiere Python 3.13 activo) ---
install:
	poetry install

run-local:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test-local:
	poetry run pytest -v

lint-local:
	poetry run ruff check src/ tests/
