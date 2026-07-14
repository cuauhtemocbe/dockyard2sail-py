---
title: Add git hooks for ruff (lint + format) via .githooks
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #11
---

# Add git hooks for ruff (lint + format) via .githooks

## Objective

Que `ruff check` y `ruff format --check` corran automáticamente antes de cada commit, sin depender de acordarse de correrlos a mano y sin sumar el framework `pre-commit` (dependencia Python extra + su propio formato de config).

## Context / User Story

Ver issue [#11](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/11) — 5 escenarios Gherkin son la fuente de verdad. Patrón git nativo (`core.hooksPath`) usado en `AvocadoDash`, depende de la reorganización del Makefile (#10).

## Requirements

1. `.githooks/pre-commit`: script que corre `make lint` y `make format-check`.
2. `make install-hooks`: setea `git config core.hooksPath .githooks` y da permisos de ejecución al script.
3. El hook corre enteramente contra Docker (vía `make lint`/`make format-check`, que son `exec`+`up-d`) — no requiere Poetry local.
4. No se agrega ninguna dependencia nueva a `pyproject.toml`.

## Boundaries

**Out of scope**: pre-push hooks, hooks de `commit-msg` (validación de formato de mensajes) — no los pide el issue.

## Success Criteria

- [x] `make install-hooks` setea `core.hooksPath=.githooks` y hace ejecutable `.githooks/pre-commit` (verificado con `git config core.hooksPath`).
- [x] Commit bloqueado por violación de lint (`import os` sin usar + fuera de orden): `ruff check` reporta 2 errores, `make lint` sale con código 1, el hook aborta el commit (`set -e`), no se crea commit.
- [x] Commit bloqueado por violación de formato pura (comillas simples, sin errores de lint): `ruff check` pasa, `ruff format --check` reporta "Would reformat", `make format-check` sale con código 1, no se crea commit.
- [x] Commit exitoso con código limpio y formateado: ambos checks pasan, el commit se crea normalmente.
- [x] Todo el flujo corrió sin Poetry local — solo `make lint`/`make format-check` (Docker `exec`).
- [x] `pyproject.toml` no tiene cambios.

## Implementation Plan

Directo a implementación — Effort: XS.

**Nota de verificación**: los 4 escenarios de commit se probaron en una copia aislada del working tree (`rsync` a un directorio scratch, con el puerto de `docker-compose.yml` remapeado a 18001 para no chocar con el container principal en 8000), no contra el repo real, para no ensuciar el historial de `main` con commits de prueba.
