---
title: Reorganize Makefile around the Docker-first workflow
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #10
---

# Reorganize Makefile around the Docker-first workflow

## Objective

Que el Makefile se autodocumente y deje claro cuáles son los targets Docker (uso diario) vs. los `-local` (fallback opcional sin Docker), en vez de que el lector tenga que adivinar por el nombre.

## Context / User Story

Ver issue [#10](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/10) — 5 escenarios Gherkin son la fuente de verdad. Inspirado en el Makefile de `AvocadoDash` (target `help` con comentarios `## descripción` parseados por `grep`+`awk`).

## Requirements

1. `make help` lista todos los targets con su descripción (parseado de comentarios `## `).
2. `make` sin argumentos se comporta igual que `make help` (`.DEFAULT_GOAL := help`).
3. Los targets Docker (`build`, `up`, `test`, `lint`, etc.) aparecen primero en el archivo.
4. Los targets `install`, `run-local`, `test-local`, `lint-local` quedan agrupados bajo un comentario que los marca como fallback opcional sin Docker, y con el prefijo `[local]` en su descripción de `help`.
5. `make test` sigue corriendo la suite dentro de Docker.

## Boundaries

**Decisión de scope (2026-07-14):** el escenario 5 de la issue dice literalmente que `make test` debe ejecutar `docker compose run --rm api pytest`. Ese comando quedó superado por el cambio a `docker compose exec` + `up-d --wait` (commit `acb7ca2`, sesión anterior, aprobado explícitamente por el usuario como "camino 1" para evitar acumular containers efímeros). Se interpreta el escenario por su intención — "los tests corren dentro de Docker", no el comando literal — que sigue cumpliéndose.

**Out of scope**: `.githooks`/`install-hooks` — spec y commit separados (#11), aunque depende de esta reorganización del Makefile.

## Success Criteria

- [x] `make help` imprime los 15 targets con su descripción.
- [x] `make` (sin target) produce el mismo output que `make help`.
- [x] Orden en el archivo: Docker primero (`build`...`format-check`), locales después (`install`, `run-local`, `test-local`, `lint-local`), `help` al final.
- [x] `make test` verificado end-to-end: corre dentro de Docker (vía `exec`), 12 tests, 100% cobertura.

## Implementation Plan

Directo a implementación — Effort: XS.
