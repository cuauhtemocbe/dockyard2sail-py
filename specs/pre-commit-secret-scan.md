---
title: Add secret scanning to pre-commit hook
status: completed
created: 2026-08-04
updated: 2026-08-04
issue: #34
---

# Add secret scanning to pre-commit hook

## Objective

Que un secreto en el diff staged sea detectado y bloquee el commit localmente, antes de que llegue al historial remoto — complementando (no reemplazando) el scan de `trivy-fs` en CI.

## Context / User Story

Ver issue [#34](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/34) — 2 escenarios Gherkin son la fuente de verdad. `.githooks/pre-commit` hoy corre `make lint` + `make format-check` dentro de Docker (`docker compose exec api ...`).

## Requirements

1. `.githooks/pre-commit` corre un scanner de secretos (`gitleaks`) sobre el diff staged, además de lint/format-check.
2. Documentar en README cómo se ejecuta (Docker, sin requerir instalación local del binario) y cómo instalar el hook.
3. Verificado localmente: un secreto plausible (ej. AWS key) staged bloquea el commit; un diff normal no se ve afectado.

## Boundaries

**Out of scope**: reemplazar el scan de `trivy-fs` en CI (ambos coexisten, defensa en profundidad).

## Success Criteria

- [x] Commit con secreto staged es rechazado por el hook.
- [x] Commit normal (sin secretos) pasa lint + format-check + secret scan sin fricción.
- [x] README documenta la herramienta y cómo se invoca.

## Implementation Plan

Directo a implementación — Effort: S. Uso de la imagen oficial `zricethezav/gitleaks` vía `docker run` (no se agrega el binario a `Dockerfile.dev`, evita bloat de una imagen usada también en runtime de dev) con `gitleaks protect --staged`. Se valida stageando una AWS key falsa y confirmando que el hook aborta el commit, luego revirtiendo el stage.
