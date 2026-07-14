---
title: Rewrite CLAUDE.md to reflect the actual Python/FastAPI stack
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #2
---

# Rewrite CLAUDE.md to reflect the actual Python/FastAPI stack

## Objective

`CLAUDE.md` documenta convenciones de TypeScript heredadas de `dockyard2sail-ts`. Hay que reemplazarlas por las equivalentes Python (poetry/ruff/pydantic-settings/typing.Protocol) y portar la estructura de `AvocadoDash` (Available Skills, Recommended Development Workflow, Before Merging).

## Context / User Story

Ver issue [#2](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/2) — contiene el user story completo y los 7 escenarios Gherkin que actúan como criterios de aceptación de este spec.

## Requirements

Los 7 escenarios Gherkin del issue #2 son la fuente de verdad:

1. Referencia a `poetry`/`ruff`, no `pnpm`.
2. Ejemplo de configuración con `pydantic-settings`, no zod/dotenv.
3. Tipado estructural documentado con `typing.Protocol`, no `interface`/`abstract class`.
4. Sección "Available Skills" listando los 6 skills instalados en `.claude/skills/`.
5. Checklist "Before Merging" (tests, lint/format, SonarQube Quality Gate, commits).
6. ~~Job de CI que falla si `CLAUDE.md` vuelve a contener `pnpm` o `zod`~~ — **fuera de alcance**, ver Boundaries.

## Boundaries

**Out of scope**: reorganizar el Makefile (#10), agregar `pydantic-settings` real al código (#4), crear carpetas hexagonales (#5), sección `[tool.ruff.format]` (#9). Este spec solo toca `CLAUDE.md`.

**Decisión (2026-07-13):** el escenario 7 (job de CI que escanea `CLAUDE.md`) es inviable porque `.gitignore` excluye `CLAUDE.md`, `.claude/` y `.mcp.json` desde el commit inicial del repo — CI hace `actions/checkout` sobre el repo git, donde ese archivo nunca existe, así que el job fallaría siempre por "file not found", no por contenido. El usuario confirmó mantener la convención actual (`CLAUDE.md` como tooling local, no trackeado) y descartar ese escenario en vez de romperla. El job `claude-md-check` que se había agregado a `ci.yml` en una sesión previa fue revertido.

## Success Criteria

- [x] Los escenarios 1-6 del issue #2 se cumplen (contenido de `CLAUDE.md`, verificado sin `pnpm`/`zod` y con las 6 secciones requeridas).
- [x] ~~Escenario 7 (check de CI)~~ — descartado por decisión de scope, ver Boundaries.
- [x] `make lint` y `make test` siguen pasando (no se tocó código de la app; `ci.yml` revertido a su estado original).

## Implementation Plan

Directo a implementación — el spec ya está completamente definido por el issue (Effort: S). Ver commit(s) asociados para el detalle de cambios.
