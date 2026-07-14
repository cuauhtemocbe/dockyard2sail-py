---
title: Enable required status checks on main via branch protection
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #21
---

# Enable required status checks on main via branch protection

## Objective

Que la pipeline de CI sea un gate real de merge, no solo un badge que nadie hace cumplir.

## Context / User Story

Ver issue [#21](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/21) — 2 escenarios Gherkin son la fuente de verdad. Decisión del usuario confirmada: activar la protección exceptuando al owner (`enforce_admins: false`), para no romper el flujo actual de push directo a `main`.

## Requirements

1. Branch protection en `main` con `required_status_checks.strict = true`.
2. Checks requeridos: los que corren en `pull_request` (no `build`, que solo corre en push a `main`): `lint`, `test`, `typecheck`, `lock-check`, `trivy-fs`, `license-check`.
3. `enforce_admins = false` — el owner puede seguir pusheando directo.
4. Documentado en el README.

## Boundaries

**Out of scope**: `required_pull_request_reviews` (no pedido), restricciones de quién puede pushear (no pedido) — solo status checks.

## Success Criteria

- [x] Branch protection activa en `main` (`gh api repos/.../branches/main/protection` ya no devuelve 404).
- [x] `required_status_checks.contexts` incluye los 6 jobs que corren en PR.
- [x] `enforce_admins.enabled` es `false`.
- [x] README documenta la regla y la excepción del owner.

## Implementation Plan

Directo a implementación — Effort: XS. Configuración de plataforma (GitHub Settings vía API), no hay tests de pytest aplicables. Aplicado con `gh api repos/cuauhtemocbe/dockyard2sail-py/branches/main/protection -X PUT`.
