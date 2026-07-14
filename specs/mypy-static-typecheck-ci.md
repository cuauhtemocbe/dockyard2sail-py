---
title: Add static type checking (mypy) to CI
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #17
---

# Add static type checking (mypy) to CI

## Objective

Verificar en CI que las implementaciones realmente cumplen la forma de los `typing.Protocol` del dominio, en vez de confiar solo en convención.

## Context / User Story

Ver issue [#17](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/17) — 3 escenarios Gherkin son la fuente de verdad. CLAUDE.md establece `typing.Protocol` como regla arquitectónica crítica (`src/app/domain/ports.py`).

## Requirements

1. `mypy` como dependencia dev en `pyproject.toml`, con `[tool.mypy]` explícito (`python_version = "3.13"`, `strict` razonable para el tamaño del proyecto).
2. Target `make typecheck` (Docker-first, igual que `lint`/`format-check`).
3. Job `typecheck` en `.github/workflows/ci.yml`.
4. El código actual (`src/`, `tests/`) pasa el chequeo sin errores.

## Boundaries

**Out of scope**: adoptar `strict = true` completo si genera ruido excesivo en tests (usar un preset razonable, documentar la decisión si se relaja algo).

**Decisión tomada**: `strict = true` se mantiene completo para `src/` (donde vive el contrato `Protocol`). Para `tests/` se relaja `disallow_untyped_defs`/`disallow_incomplete_defs` vía `[[tool.mypy.overrides]]` — exigir anotaciones en cada fixture/test de pytest generaba 16 errores de ruido sin valor real (no hay contratos estructurales que proteger ahí).

## Success Criteria

- [x] `make typecheck` corre `mypy` dentro de Docker y pasa en verde contra el código actual.
- [x] Un método con firma incompatible con `PaymentGateway` (`Protocol`) hace fallar `mypy` con un error claro (verificado manualmente rompiendo `FakePaymentGateway.charge` temporalmente).
- [x] CI tiene un job `typecheck` que corre `make typecheck`.

## Nota técnica

`pyproject.toml` no está montado como volumen en `docker-compose.yml` — cualquier cambio requiere `docker compose build api` (o `docker cp` para iterar rápido) para que el container lo vea. Perdí tiempo de debugging en overrides de mypy que "no aplicaban" por este motivo exacto (ya documentado como gotcha recurrente en memoria del proyecto — ver `typed-settings-pydantic.md`, mismo síntoma).

## Implementation Plan

Directo a implementación — Effort: S. Se implementa antes que #19/#18 para que el código nuevo nazca type-checked.
