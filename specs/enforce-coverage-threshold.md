---
title: Enforce minimum test coverage threshold
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #7
---

# Enforce minimum test coverage threshold

## Objective

Evitar que código sin tests se mergee silenciosamente: `pytest --cov` debe fallar si la cobertura cae debajo de un umbral fijo.

## Context / User Story

Ver issue [#7](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/7) — 3 escenarios Gherkin son la fuente de verdad. Cobertura actual: 100% (12/12 statements).

## Requirements

1. `--cov-fail-under=90` en la configuración de pytest (`pyproject.toml`).
2. Aplicado en `make test` y por lo tanto en el job `test` de CI (ya invoca `make test`, no requiere cambios en `ci.yml`).
3. Probado rojo→verde: se valida agregando código sin cubrir, verificando que falla, y confirmando que el estado real (cubierto) pasa.

## Boundaries

**Out of scope**: subir cobertura de módulos futuros (#4, #5) por encima del umbral — eso es responsabilidad de cada issue que agregue código nuevo, no de este spec.

## Success Criteria

- [x] `pyproject.toml` tiene `--cov-fail-under=90` en `[tool.pytest.ini_options]` (vía `addopts`).
- [x] `make test` falla si la cobertura baja de 90% (probado con un módulo temporal sin tests: 86% → exit 1).
- [x] `make test` pasa con el código real actual (100% de cobertura, exit 0).

## Implementation Plan

Directo a implementación — Effort: XS. Un solo cambio en `pyproject.toml`.
