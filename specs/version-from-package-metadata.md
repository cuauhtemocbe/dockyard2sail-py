---
title: Read app version from package metadata instead of hardcoding it
status: draft
created: 2026-07-14
updated: 2026-07-14
issue: #15
---

# Read app version from package metadata instead of hardcoding it

## Objective

Eliminar la duplicación entre la versión declarada en `pyproject.toml` y la hardcodeada en `FastAPI(version="0.1.0")`, para que no puedan divergir silenciosamente.

## Context / User Story

Ver issue [#15](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/15) — 3 escenarios Gherkin son la fuente de verdad. Afecta `src/app/main.py`.

## Requirements

1. `FastAPI(version=...)` se resuelve vía `importlib.metadata.version("dockyard2sail-py")` en vez de un string literal.
2. Si la metadata no se puede resolver (`PackageNotFoundError`), la app no crashea: usa un fallback (`"0.0.0-dev"` o similar).

## Boundaries

**Out of scope**: cambiar el mecanismo de release/tagging del proyecto (no hay CI de publicación de paquete hoy).

## Success Criteria

- [ ] `/openapi.json` reporta la versión declarada en `pyproject.toml`.
- [ ] Si `importlib.metadata.version` se mockea para devolver otra versión, `/openapi.json` la refleja.
- [ ] Si `importlib.metadata.version` lanza `PackageNotFoundError`, la app arranca igual con un fallback.

## Implementation Plan

Directo a implementación — Effort: XS.
