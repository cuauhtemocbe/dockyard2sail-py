---
title: Add typed settings with pydantic-settings
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #4
---

# Add typed settings with pydantic-settings

## Objective

Validar configuración al arranque en vez de en runtime: una clase `Settings` tipada que falle rápido si `ENVIRONMENT` o `PORT` son inválidos.

## Context / User Story

Ver issue [#4](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/4) — la scenario outline con 4 ejemplos (development/staging/production/qa) es la fuente de verdad. Sigue el patrón de `pydantic-settings` documentado en `CLAUDE.md` (singleton implícito vía instancia a nivel de módulo).

## Requirements

1. `src/app/config.py` con `Settings(BaseSettings)`: `environment: Environment` (enum development/staging/production, default development) y `port: int` (default 8000).
2. `model_config = SettingsConfigDict(env_file=".env", extra="ignore")`.
3. Instancia de módulo `settings = Settings()` (singleton implícito, cacheado en la primera importación).
4. Tests unitarios cubriendo los 4 escenarios Gherkin del issue (carga exitosa, default de PORT, PORT inválido, y los 4 casos de la scenario outline de ENVIRONMENT).

## Boundaries

**Out of scope**: consumir `settings` desde `main.py`/`routes.py` (no hay necesidad actual de leer config en el código existente) y las carpetas hexagonales (#5, spec separado).

## Success Criteria

- [x] `Settings()` carga `ENVIRONMENT=development` y `PORT=8000` correctamente.
- [x] Sin `PORT` en el entorno, `settings.port` es `8000`.
- [x] `PORT=not-a-number` lanza `ValidationError`.
- [x] `ENVIRONMENT` acepta development/staging/production y rechaza `qa` con `ValidationError`.
- [x] Cobertura 100% en `config.py`, `make lint` y `make format-check` en verde.

## Implementation Plan

Directo a implementación — Effort: S.

**Nota técnica**: se agregó `pydantic-settings` a `pyproject.toml` y se regeneró `poetry.lock` (`poetry lock --no-update`) fuera del container porque la imagen dev no tiene poetry con red al reconstruir sobre un lock desincronizado. Requirió `docker compose build api` para que el container viera el nuevo `pyproject.toml`/`poetry.lock` (no están montados como volumen).
