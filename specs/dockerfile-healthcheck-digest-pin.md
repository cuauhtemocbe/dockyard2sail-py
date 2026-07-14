---
title: Add HEALTHCHECK and pin base image digest in production Dockerfile
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #6
---

# Add HEALTHCHECK and pin base image digest in production Dockerfile

## Objective

Detectar automáticamente un contenedor de producción colgado y evitar drift silencioso de la imagen base.

## Context / User Story

Ver issue [#6](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/6) — 4 escenarios Gherkin son la fuente de verdad. Afecta solo `Dockerfile` (producción), no `Dockerfile.dev`.

## Requirements

1. `HEALTHCHECK` que llama a `/health` y marca el contenedor `healthy`/`unhealthy` según la respuesta.
2. `FROM python:3.13-slim@sha256:...` con digest fijo en vez de solo el tag.
3. La imagen sigue construyendo correctamente con el digest pinneado.

## Boundaries

**Out of scope**: `Dockerfile.dev` (no es la imagen de producción, no lo pide el issue). Instalar `curl`/`wget` para el healthcheck — se usa `python -c` con `urllib.request` (ya disponible en la imagen base) para no aumentar superficie/tamaño de la imagen.

## Success Criteria

- [x] `docker build -f Dockerfile -t dockyard2sail-py .` completa exitosamente con el digest pinneado.
- [x] `docker inspect --format='{{.State.Health.Status}}'` devuelve `healthy` tras el `start-period` (verificado: `starting` → `healthy` en la segunda revisión, ~6s).
- [x] `FROM` incluye el pin `@sha256:eb43ff125d8d58d7449dcba7d336c23bcac412f526d861db493b9994d8010280` para `python:3.13-slim`.

## Implementation Plan

Directo a implementación — Effort: XS.

**Nota**: el healthcheck usa el puerto vía `os.environ.get("PORT", "8000")`, consistente con el `CMD` que ya lee `${PORT:-8000}` — necesario porque Railway (u otro proveedor) inyecta `$PORT` dinámicamente.
