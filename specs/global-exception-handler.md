---
title: Add a global exception handler for consistent JSON errors
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #18
---

# Add a global exception handler for consistent JSON errors

## Objective

Que cualquier excepción no controlada devuelva un cuerpo JSON consistente (status 500), sin exponer el mensaje interno de la excepción al cliente.

## Context / User Story

Ver issue [#18](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/18) — 3 escenarios Gherkin son la fuente de verdad. Afecta `src/app/main.py`.

## Requirements

1. Exception handler global (`@app.exception_handler(Exception)`) que devuelve `{"error": "Internal Server Error"}` (o similar genérico) con status 500.
2. El mensaje real de la excepción no se filtra en el body de la respuesta (solo se loggea server-side).
3. Endpoints existentes (`/health`, `/api/v1/hello`) no cambian su comportamiento.

## Boundaries

**Out of scope**: manejo diferenciado por tipo de excepción (p.ej. excepciones de dominio específicas) — hoy no existen, se agregará cuando aparezcan.

## Success Criteria

- [x] `/health` sigue devolviendo 200 sin cambios.
- [x] Una ruta que lanza una excepción no controlada devuelve 500 con JSON `{"error": ...}`.
- [x] El mensaje interno de la excepción no aparece en el body de la respuesta.

## Implementation Plan

Directo a implementación — Effort: S. Requiere una ruta de test dedicada (o monkeypatch de una ruta existente) para forzar la excepción de forma determinística.

**Nota técnica**: Starlette's `ServerErrorMiddleware` re-lanza la excepción original después de enviar la respuesta (para que el server ASGI la loggee) — `httpx.ASGITransport` por defecto también la re-lanza hacia el test (`raise_app_exceptions=True`). Los tests necesitan `ASGITransport(app=test_app, raise_app_exceptions=False)` para poder inspeccionar la respuesta 500 real en vez de recibir la excepción de Python. La excepción se loggea server-side vía `logger.exception(...)` antes de construir la respuesta genérica.
