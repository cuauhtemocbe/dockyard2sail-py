---
title: Gate de CVEs Trivy fail-closed en pre-push
status: in-progress
created: 2026-09-18
updated: 2026-09-18
issue: meta-projects#41
---

# Gate de CVEs Trivy fail-closed en pre-push

## Objective

Agregar un git hook `pre-push` que corre el scanner de vulnerabilidades de filesystem de Trivy y bloquea el push si encuentra algún CVE de severidad CRITICAL con fix publicado — y también lo bloquea si `trivy` no está instalado. Es la parte de dockyard2sail-py del rollout fleet-wide (meta-projects issue #41) de un gate local de CVEs, antes de que el código salga de la máquina del desarrollador.

## Context

dockyard2sail-py ya tiene un directorio de hooks versionado y opt-in: `.githooks/`, con `pre-commit` (`make validate` + gitleaks vía Docker), activado una vez por clon con `make install-hooks` (setea `core.hooksPath=.githooks`, ver `README.md`). Hoy no hay gate local de CVEs en dependencias: CI tiene el job `trivy-fs`, pero nada impide pushear una rama con un CVE CRITICAL fixable antes de que corra CI.

El mecanismo de activación ya existe y está documentado; este cambio solo agrega un archivo a ese directorio y hace que `make install-hooks` marque como ejecutables todos los hooks (`chmod +x .githooks/*`) en vez de solo `pre-commit`. No se crea `scripts/install-hooks.sh` ni ningún mecanismo paralelo (misma decisión que AvocadoDash PR #76).

A diferencia de `pre-commit`, este hook llama al CLI `trivy` directo en el host (no corre en Docker), por lo que falla cerrado — bloquea el push — si `trivy` no está en el `PATH`.

## Requirements

### Functional Requirements

- [ ] `.githooks/pre-push` (modo 755) corre en `git push` una vez ejecutado `make install-hooks`.
- [ ] Si `trivy` no está en el `PATH`, imprime un mensaje que apunta a `.claude/skills/trivy-scan/setup.md` y sale con código 1 (fail closed).
- [ ] Si `trivy` está presente, corre `trivy fs . --scanners vuln --severity CRITICAL --exit-code 1 --ignore-unfixed --quiet`; un CRITICAL con fix bloquea el push (exit 1, tabla visible), cualquier otro caso (HIGH/MEDIUM, CRITICAL sin fix, limpio) deja pasar (exit 0).
- [ ] `make install-hooks` hace `chmod +x .githooks/*` y su texto de ayuda menciona pre-push.
- [ ] `README.md` documenta el gate junto al párrafo del pre-commit: requiere `trivy` en el `PATH`, fail-closed, solo CRITICAL+fixable.

### Non-Functional Requirements

- [ ] Sin mecanismo de activación nuevo: se reutiliza `.githooks/` + `make install-hooks`.
- [ ] Sin efectos secundarios: el hook solo escanea y puede abortar, no modifica archivos ni hace commits.
- [ ] No requiere Docker (solo `trivy` en el `PATH` del host).
- [ ] Cero referencias a Engram en el hook.

## Architecture

### Components

- `.githooks/pre-push` (nuevo): bash, `set -uo pipefail` (deliberadamente sin `-e`, los `if` manejan ambos caminos de fallo y deben llegar a su `exit` explícito). Dos pasos: chequeo `command -v trivy` → exit 1 con puntero al setup; luego `trivy fs ...` cuyo código de salida determina el del hook.
- `Makefile` (`install-hooks`): `chmod +x .githooks/*`, ayuda actualizada.
- `README.md`: párrafo del pre-push gate.

### Data Model

N/A.

### External Dependencies

- [Trivy](https://github.com/aquasecurity/trivy) CLI en el `PATH` del desarrollador, instalado según `.claude/skills/trivy-scan/setup.md`. Nota: `.claude/` está en `.gitignore` en este repo, así que el puntero solo resuelve en clones que tengan ese skill localmente.

## User Stories

Rastreadas a nivel fleet en meta-projects issue #41. No se crea issue local; este spec es el artefacto de seguimiento.

```gherkin
Feature: Gate local de CVEs al hacer push

  Scenario: Un CVE CRITICAL con fix bloquea el push
    Given el hook pre-push está instalado y activo
    And una dependencia tiene un CVE CRITICAL con fix publicado
    When corro git push
    Then el hook sale con código no-cero y el push se aborta
    And la tabla nombra el paquete y el CVE

  Scenario: Un HIGH o un CRITICAL sin fix no bloquea
    Given el hook pre-push está instalado y activo
    And una dependencia tiene un CVE HIGH, o un CRITICAL sin fix publicado
    When corro git push
    Then el hook sale con código 0 y el push procede

  Scenario: Trivy ausente falla cerrado
    Given trivy no está en el PATH
    When corro git push
    Then el hook bloquea el push
    And el mensaje apunta a las instrucciones de setup

  Scenario: Instalar el hook es explícito
    Given .githooks/pre-push está commiteado
    But core.hooksPath no se ha configurado en el clon
    When pusheo
    Then el hook no corre
    And correr make install-hooks lo activa para los siguientes pushes
```

## Testing Strategy

### Unit Tests

N/A — tooling de shell fuera de `src/` y del alcance de pytest.

### Integration Tests

Verificación manual por invocación directa del hook:

- Sin `trivy` en el `PATH` (`/usr/bin/env -i PATH=/nonexistent /bin/bash .githooks/pre-push`): exit 1 con el mensaje.
- Repo real (limpio): exit 0.
- Manifest desechable fuera del repo con un paquete Python pineado con CRITICAL+fixable: exit 1 con el CVE en la tabla; con solo HIGH o solo CRITICAL sin fix: exit 0.
- Clon temporal sin `core.hooksPath`: el hook no corre en `git push`.

### E2E Tests

N/A — sin flujo de usuario.

## Boundaries & Constraints

### In Scope

- `.githooks/pre-push`, cambio de `chmod` en `make install-hooks`, párrafo en `README.md`.

### Out of Scope

- `scripts/install-hooks.sh` u otro mecanismo de activación paralelo.
- Cambios a `.githooks/pre-commit` o al job `trivy-fs` de CI.
- Otras severidades o scanners (secretos ya cubiertos por el pre-commit).
- Auto-instalar Trivy.
- Cualquier referencia a Engram (#33 fue declinado).
- Editar `CLAUDE.md` / `.claude/` (están en `.gitignore`).

### Technical Constraints

- bash (`#!/usr/bin/env bash`), ejecutable y versionado en `.githooks/`.
- No debe asumir Docker disponible.

## Success Criteria

- [ ] `.githooks/pre-push` existe, es ejecutable y contiene exactamente el contrato fleet-wide (chequeo de `trivy`, luego el `trivy fs` indicado).
- [ ] El scan previo a la activación (`trivy fs . --scanners vuln --severity CRITICAL --ignore-unfixed`) reportó 0 vulnerabilidades sobre la base de esta rama.
- [ ] Los 4 escenarios Gherkin verificados con salida real de comandos.
- [ ] `make install-hooks` deja ejecutables ambos hooks.

## Implementation Plan

Sin `-plan.md` separado: es un único script totalmente especificado más dos ediciones de una línea (ver Architecture).
