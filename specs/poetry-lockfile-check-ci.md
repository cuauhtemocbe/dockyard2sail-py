---
title: Verify poetry.lock consistency in CI
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #16
---

# Verify poetry.lock consistency in CI

## Objective

Detectar en CI si `poetry.lock` quedó desincronizado de `pyproject.toml`, antes de que rompa un build reproducible.

## Context / User Story

Ver issue [#16](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/16) — 3 escenarios Gherkin son la fuente de verdad.

## Requirements

1. Target `make lock-check` que corre `poetry check --lock` dentro de Docker.
2. Job/step en CI que corre `make lock-check`.
3. Documentado en `make help` y README.

## Boundaries

**Out of scope**: regenerar el lockfile automáticamente en CI (el chequeo solo detecta y falla, no corrige).

## Success Criteria

- [x] `make lock-check` pasa cuando el lockfile está sincronizado.
- [x] `make lock-check` falla si `pyproject.toml` cambia sin regenerar `poetry.lock`.
- [x] CI corre el chequeo en cada push/PR.

## Implementation Plan

Directo a implementación — Effort: XS. Verificado manualmente (`poetry check --lock` pasa/falla según lo esperado, ida y vuelta) — comportamiento de infraestructura, no cubierto por pytest.
