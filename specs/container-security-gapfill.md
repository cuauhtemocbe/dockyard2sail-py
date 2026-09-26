---
title: Escaneo de misconfiguraciones de Dockerfile en CI (gap-fill)
status: in-progress
created: 2026-09-26
updated: 2026-09-26
issue: meta-projects#56
---

# Escaneo de misconfiguraciones de Dockerfile en CI (gap-fill)

## Objective

Agregar a `.github/workflows/ci.yml` un job `trivy-config` que escanea el `Dockerfile` en busca de misconfiguraciones CRITICAL/HIGH en cada push y pull request, y alinear `ignore-unfixed: true` en los pasos Trivy existentes. Es la parte de dockyard2sail-py (Group B, Task 7) de la US global meta-projects#56.

## Context

Spec y plan del rollout fleet-wide: `specs/global/container-security-scanning-fleet-rollout.md` y `-plan.md` en el repo meta-projects. Este spec solo cubre lo local a dockyard2sail-py.

Hoy `ci.yml` tiene `trivy-fs` (lockfile, todas las ramas y PRs) y, dentro del job `build`, un escaneo de imagen que solo corre en push a `main`. Nada escanea el `Dockerfile` en busca de misconfiguraciones. El workflow de referencia validado es `portfolio-website/.github/workflows/container-security.yml` (mismo SHA de `trivy-action`, mismos SHAs de `actions/checkout`).

Por ser gap-fill, no se crea `container-security.yml`: se extiende `ci.yml` sin renombrar ni quitar jobs existentes.

## Requirements

### Functional Requirements

- [ ] Job `trivy-config` en `ci.yml`: `scan-type: config`, `scan-ref: .`, `skip-files: Dockerfile.dev`, `severity: CRITICAL,HIGH`, `exit-code: "1"`, `ignore-unfixed: true`.
- [ ] `trivy-config` corre en `push` y `pull_request` (sin condición `if`, como `trivy-fs`).
- [ ] `ignore-unfixed: true` en el paso de `trivy-fs` y en el de imagen del job `build`.
- [ ] `trivy-action` y `actions/checkout` fijados por el mismo SHA que ya usa el archivo.

### Non-Functional Requirements

- [ ] `permissions: contents: read` (ya vigente a nivel workflow).
- [ ] Sin secretos, sin push de imagen.
- [ ] Jobs existentes (`lint`, `test`, `typecheck`, `lock-check`, `license-check`, `trivy-fs`, `build`) conservan su nombre.

## Architecture

### Components

- `.github/workflows/ci.yml`: job nuevo `trivy-config` (sin `needs`, corre en paralelo) y una línea `ignore-unfixed` en los pasos `trivy-fs` y `Trivy image scan`.

### Data Model

N/A.

### External Dependencies

- `aquasecurity/trivy-action@ed142fd0673e97e23eac54620cfb913e5ce36c25` (v0.36.0), ya en uso.

## User Stories

Rastreadas a nivel fleet en meta-projects#56 (escenario "A Dockerfile misconfiguration fails CI"). No se crea issue local.

```gherkin
Feature: Escaneo de misconfiguraciones de Dockerfile en CI

  Scenario: Una misconfiguración HIGH/CRITICAL en el Dockerfile falla el PR
    Given el Dockerfile tiene una misconfiguración HIGH o CRITICAL (p. ej. sin USER no-root)
    When corre CI en un pull_request
    Then el job trivy-config sale con código distinto de cero y nombra la regla

  Scenario: Dockerfile.dev no se escanea
    Given Dockerfile.dev corre como root a propósito
    When corre trivy-config
    Then Dockerfile.dev se omite y el job no falla por él
```

## Testing Strategy

### Unit Tests
N/A — solo cambios de workflow.

### Integration Tests
- Local: `trivy config . --skip-files Dockerfile.dev --severity CRITICAL,HIGH --exit-code 1` sale 0 sobre el `Dockerfile` actual.
- CI: el PR de este cambio muestra `trivy-config` verde, y `trivy-fs` verde con `ignore-unfixed: true`.

### E2E Tests
N/A.

### Performance Tests
Registrar duración de `trivy-config` (presupuesto fleet: < 10 min).

## Boundaries & Constraints

### In Scope
- Job `trivy-config` y alineación de `ignore-unfixed` en `ci.yml`.

### Out of Scope
- Nuevo `container-security.yml`, job `trivy-image` en PR, escaneo semanal (`schedule`): se proponen en la descripción del PR, no se implementan aquí.
- Podar `.trivyignore.yaml` (con `ignore-unfixed` sus entradas "sin fix upstream" quedan redundantes, pero conservan fecha de re-revisión; decisión del dueño).
- Cambiar branch protection o checks requeridos.

### Technical Constraints
- `permissions: contents: read`; acciones fijadas por SHA (spec `pin-actions-by-sha`).

## Success Criteria

- [ ] `trivy-config` verde en el PR, sin renombrar ni quitar checks existentes.
- [ ] `ignore-unfixed: true` presente en los tres pasos Trivy de `ci.yml`.
- [ ] Duración de `trivy-config` registrada en el PR.

## Implementation Plan

Plan fleet-wide: `specs/global/container-security-scanning-fleet-rollout-plan.md` (meta-projects), Task 7. Tarea única, esfuerzo XS: editar `ci.yml`.

## Changelog

<!-- Solo se usa una vez que este spec llegó a `completed`. -->
