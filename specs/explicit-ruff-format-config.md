---
title: Add explicit ruff format configuration
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #9
---

# Add explicit ruff format configuration

## Objective

Fijar la configuración de `ruff format` explícitamente para que el formato sea consistente entre máquinas, sin depender de los defaults implícitos de ruff (que pueden cambiar entre versiones).

## Context / User Story

Ver issue [#9](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/9) — 3 escenarios Gherkin son la fuente de verdad.

## Requirements

1. Sección `[tool.ruff.format]` explícita en `pyproject.toml`.
2. `ruff format --check src/ tests/` sin cambios pendientes sobre el código actual.
3. CI hace fallar el job `lint` si `ruff format --check` encuentra archivos sin formatear.

## Boundaries

Fuera de alcance: reorganizar el Makefile (#10, Fase 4). Se agregó únicamente el target `format-check` necesario para este spec.

## Success Criteria

- [x] `pyproject.toml` tiene `[tool.ruff.format]` con settings explícitos (quote-style, indent-style, skip-magic-trailing-comma, line-ending).
- [x] `ruff format --check src/ tests/` reporta "6 files already formatted" (sin cambios pendientes).
- [x] `ci.yml` corre `make format-check` como parte del job `lint`.

## Implementation Plan

Directo a implementación — Effort: XS.

**Nota técnica descubierta**: `pyproject.toml` no está montado como volumen en `docker-compose.yml` (solo `src/`, `tests/`, `poetry.lock`) — se copia al build de la imagen. Cualquier cambio a `pyproject.toml` requiere `docker compose build api` antes de que el container lo vea.
