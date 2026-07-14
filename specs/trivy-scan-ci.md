---
title: Add Trivy vulnerability scanning to the CI pipeline
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #14
---

# Add Trivy vulnerability scanning to the CI pipeline

## Objective

Detectar vulnerabilidades HIGH/CRITICAL de dependencias e imagen antes de que lleguen a `main`, reusando las excepciones ya curadas en `.trivyignore.yaml`.

## Context / User Story

Ver issue [#14](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/14) — 5 escenarios Gherkin son la fuente de verdad. A diferencia de SonarQube (herramienta personal, no de CI — ver memoria del proyecto), Trivy sí corre en CI porque escanea vulnerabilidades reales.

## Requirements

1. Job/step `trivy-fs` en `.github/workflows/ci.yml`: escanea el filesystem (dependencias de `poetry.lock`) en cada push/PR, usando `aquasecurity/trivy-action`.
2. Step de escaneo de imagen dentro del job `build` (que ya construye `dockyard2sail-py:ci` solo en push a `main`): escanea la imagen recién construida.
3. Ambos respetan `.trivyignore.yaml` existente (vía `trivyignores` input de la action).
4. `severity: CRITICAL,HIGH` y `exit-code: 1` para que el job falle en hallazgos no exceptuados.

## Boundaries

**Out of scope**: escaneo de secretos/IaC en CI (ya cubierto localmente por el skill `/trivy-scan` personal); esto es solo vulnerabilidades de dependencias/imagen.

## Success Criteria

- [x] El scan de filesystem corre en cada push/PR y no falla con el estado actual del repo (sin vulnerabilidades HIGH/CRITICAL no exceptuadas).
- [x] El scan de imagen corre dentro del job `build`.
- [x] `.trivyignore.yaml` se pasa correctamente (verificado localmente con `trivy fs`/`trivy image` reproduciendo los mismos flags que usa la CI action — ambos exit code 0).

## Implementation Plan

Directo a implementación — Effort: S. Solo toca `.github/workflows/ci.yml`, no hay tests de pytest aplicables (comportamiento de infraestructura CI). Usa `aquasecurity/trivy-action@0.36.0` (última release al momento de implementar).

**Bug encontrado y corregido en `.trivyignore.yaml`**: el campo `expired_at` estaba en formato solo-fecha (`"2026-10-12"`), que esta versión de Trivy (0.72.0) no puede parsear como RFC3339 (`FATAL ... cannot parse "" as "T"`) — sin este fix, el job de CI habría fallado inmediatamente pese a que las excepciones eran válidas. Se corrigió a `"2026-10-12T00:00:00Z"` en las 27 entradas existentes. Verificado con `trivy fs`/`trivy image` locales antes y después del fix.
