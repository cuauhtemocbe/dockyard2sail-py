---
title: Resolve or document the base-image pinning asymmetry (Dockerfile vs Dockerfile.dev)
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #22
---

# Resolve or document the base-image pinning asymmetry (Dockerfile vs Dockerfile.dev)

## Objective

Que la asimetría entre `Dockerfile` (digest pinneado) y `Dockerfile.dev` (tag flotante) se lea como una decisión deliberada, no como un descuido.

## Context / User Story

Ver issue [#22](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/22) — 2 escenarios Gherkin son la fuente de verdad. Decisión del usuario tras discutir el trade-off: documentar, no pinnear.

## Requirements

1. Comentario explícito en `Dockerfile.dev` explicando por qué no pinnea el digest.
2. Nota en el README (sección Deploy) contrastando ambas políticas.
3. Ambas imágenes siguen construyendo correctamente.

## Boundaries

**Out of scope**: pinnear `Dockerfile.dev` (decisión explícita del usuario: prioriza parches automáticos en dev sobre reproducibilidad exacta).

## Success Criteria

- [x] `Dockerfile.dev` tiene un comentario explícito arriba del `FROM` explicando la decisión.
- [x] README documenta el contraste entre ambas políticas de pinning.
- [x] `docker build -f Dockerfile .` y `docker build -f Dockerfile.dev .` completan exitosamente.

## Implementation Plan

Directo a implementación — Effort: XS. Verificado con build real de ambas imágenes.
