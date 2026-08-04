---
title: Add explicit minimal permissions block to CI workflow
status: completed
created: 2026-08-04
updated: 2026-08-04
issue: #32
---

# Add explicit minimal permissions block to CI workflow

## Objective

Limitar el radio de impacto de un `GITHUB_TOKEN` comprometido declarando permisos mínimos explícitos en vez de heredar el default del repo.

## Context / User Story

Ver issue [#32](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/32) — 2 escenarios Gherkin son la fuente de verdad. Ninguno de los 7 jobs actuales (lint, test, typecheck, lock-check, license-check, trivy-fs, build) necesita escritura.

## Requirements

1. Bloque `permissions:` a nivel de workflow en `.github/workflows/ci.yml`, scope `contents: read`.

## Boundaries

**Out of scope**: escalar permisos por job — ninguno lo necesita hoy.

## Success Criteria

- [x] `permissions:` presente a nivel de workflow, `contents: read`.
- [x] Los 7 jobs corren verdes con el token reducido.

## Implementation Plan

Directo a implementación — Effort: XS. Se valida con CI run verde.
