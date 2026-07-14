IMAGE = dockyard2sail-py

.DEFAULT_GOAL := help
.PHONY: help build up up-d down logs test test-v lint format-check typecheck install-hooks install run-local test-local lint-local

# --- Docker (flujo principal) ---

build: ## Construir la imagen de desarrollo
	docker compose build

up: ## Levantar el servicio en foreground (con logs)
	docker compose up

up-d: ## Levantar el servicio en background, esperando a que esté healthy
	docker compose up -d --wait

down: ## Bajar el servicio
	docker compose down

logs: ## Seguir los logs del servicio api
	docker compose logs -f api

test: up-d ## Correr la suite de tests con cobertura dentro de Docker
	docker compose exec api pytest --cov=app --cov-report=term-missing

test-v: up-d ## Correr los tests en modo verbose dentro de Docker
	docker compose exec api pytest -v

lint: up-d ## Correr ruff check dentro de Docker
	docker compose exec api ruff check src/ tests/

format-check: up-d ## Verificar formato con ruff dentro de Docker (sin modificar archivos)
	docker compose exec api ruff format --check src/ tests/

typecheck: up-d ## Correr mypy dentro de Docker
	docker compose exec api mypy src/ tests/

install-hooks: ## Habilitar el git hook de pre-commit (lint + format, corre en Docker)
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

# --- Local (opcional: fallback sin Docker, requiere Python 3.13 y Poetry) ---

install: ## [local] Instalar dependencias con poetry
	poetry install

run-local: ## [local] Levantar la app con uvicorn --reload
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test-local: ## [local] Correr tests con poetry
	poetry run pytest -v

lint-local: ## [local] Correr ruff check con poetry
	poetry run ruff check src/ tests/

help: ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'
