---
title: Pin third-party GitHub Actions to commit SHA
status: completed
created: 2026-08-04
updated: 2026-08-04
issue: #31
---

# Pin third-party GitHub Actions to commit SHA

## Objective

Evitar que un tag mutable (`actions/checkout@v4`, `aquasecurity/trivy-action@v0.36.0`) re-apuntado de forma maliciosa ejecute código no auditado en CI.

## Context / User Story

Ver issue [#31](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/31) — 2 escenarios Gherkin son la fuente de verdad. Referencia: compromiso de supply-chain de `tj-actions/changed-files` (2025).

## Requirements

1. Todas las referencias `uses:` de terceros en `.github/workflows/ci.yml` pinneadas a un commit SHA completo, con comentario trailing indicando la versión legible.
2. Dependabot (`github-actions` ecosystem, ya configurado) debe seguir pudiendo proponer bumps del SHA pinneado.

## Boundaries

**Out of scope**: acciones propias de GitHub sin mantenedor externo no aplica aquí (no hay ninguna en este workflow además de `actions/checkout`, que sí es de terceros a efectos de esta política).

## Success Criteria

- [x] `actions/checkout@v4` → `actions/checkout@<sha> # v4` en las 7 ocurrencias del workflow.
- [x] `aquasecurity/trivy-action@v0.36.0` → `aquasecurity/trivy-action@<sha> # v0.36.0` en las 2 ocurrencias.
- [x] CI corre verde tras el cambio.

## Implementation Plan

Directo a implementación — Effort: XS. Sin tests automatizados posibles (config de plataforma); se valida con CI run verde. SHAs resueltos vía `git ls-remote` (peeled para tags anotados):
- `actions/checkout@v4` → `11d5960a326750d5838078e36cf38b85af677262`
- `aquasecurity/trivy-action@v0.36.0` → `ed142fd0673e97e23eac54620cfb913e5ce36c25`
