---
title: Make CORS origins configurable via Settings
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #19
---

# Make CORS origins configurable via Settings

## Objective

Permitir que un frontend integrador llame a la API sin hardcodear orígenes CORS en el código del template, manteniendo CORS deshabilitado por defecto (comportamiento actual).

## Context / User Story

Ver issue [#19](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/19) — 4 escenarios Gherkin son la fuente de verdad. Afecta `src/app/config.py` y `src/app/main.py`.

## Requirements

1. `Settings` gana un campo `cors_allowed_origins: list[str] = []`, parseado desde una env var separada por comas (`CORS_ALLOWED_ORIGINS`).
2. `main.py` registra `CORSMiddleware` solo si `settings.cors_allowed_origins` no está vacío.
3. Sin la env var configurada, no hay header `Access-Control-Allow-Origin` en la respuesta (comportamiento default seguro, sin cambios respecto a hoy).

## Boundaries

**Out of scope**: configurar métodos/headers permitidos más allá de los defaults de `CORSMiddleware`; wildcard `*` no se ofrece como opción documentada (el usuario puede pasarlo si quiere, pero no es el default ni se promueve).

## Success Criteria

- [x] Sin `CORS_ALLOWED_ORIGINS`, una request cross-origin no recibe `Access-Control-Allow-Origin`.
- [x] Con un origen configurado, ese origen recibe el header; otros no.
- [x] Con múltiples orígenes (coma-separados), todos los configurados son permitidos.
- [x] Variable documentada en el README junto a `ENVIRONMENT`/`PORT`.

## Implementation Plan

Directo a implementación — Effort: S.

**Nota técnica**: `main.py` pasó a exponer `create_app()` (factory) en vez de instanciar `app` directamente a nivel de módulo, porque `CORSMiddleware` se registra según el valor de `settings.cors_allowed_origins` al momento de crear la app — los tests necesitan poder reconstruirla tras mockear `settings`. `list[str]` en `Settings` requirió `Annotated[list[str], NoDecode]` (pydantic-settings intenta parsear JSON para tipos complejos antes de correr el `field_validator`; `NoDecode` se lo salta para poder aceptar el formato coma-separado del issue).
