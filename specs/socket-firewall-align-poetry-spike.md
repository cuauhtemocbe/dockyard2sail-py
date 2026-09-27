---
title: Align Socket Firewall workflow with the Poetry spike
status: in-progress
created: 2026-09-26
updated: 2026-09-26
issue: #49
---

# Align Socket Firewall workflow with the Poetry spike

## Objective

Que `dependabot-socket-firewall.yml` cubra también las dependencias de desarrollo y sea honesto sobre por qué cierra un PR, alineado con el spike de cuauhtemocbe/DataScience-Docker#38 (US global cuauhtemocbe/meta-projects#47).

## Context / User Story

Ver issue [#49](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/49) — 3 escenarios Gherkin son la fuente de verdad. El enfoque `poetry export` + `sfw pip install` ya es el correcto (`sfw poetry install` falla con `CERTIFICATE_VERIFY_FAILED`); faltan cuatro correcciones.

## Requirements

1. `poetry export` incluye el grupo `dev` (`--with dev`).
2. El comentario de cierre no afirma que hubo un bloqueo: admite que puede ser un error ajeno y pide reabrir si es falso positivo.
3. Un fallo de `poetry export` deja el job en rojo sin cerrar el PR: solo el paso de instalación con firewall lleva `continue-on-error`. Documentado en un comentario del workflow.
4. Sin `poetry-plugin-export` (Poetry 1.8.4 ya trae `export`); versión de Poetry sincronizada con `Dockerfile.dev`.
5. Actions fijadas por SHA re-resuelto vía API, sin secretos nuevos, job limitado a `dependabot[bot]`.

## Boundaries

**Out of scope**: subir a Poetry 2.x; cerrar el PR solo ante un bloqueo real leyendo `$SFW_JSON_REPORT_PATH` (esquema de `blocked` no verificado en el spike); cambiar el guard de actor.

## Success Criteria

- [x] `poetry export --with dev` incluye ruff/pytest/mypy (verificado en local).
- [x] El texto de cierre no afirma un bloqueo.
- [x] `poetry export` está en un paso sin `continue-on-error`.
- [x] Sin `poetry-plugin-export`.
- [x] SHAs de las 3 actions coinciden con `gh api repos/<repo>/tags`.
- [ ] Verificado en un PR real de Dependabot — **pendiente**: #45 y #46 ya están cerrado/mergeado; se valida en el siguiente PR de Dependabot.

## Implementation Plan

Ver [`socket-firewall-align-poetry-spike-plan.md`](socket-firewall-align-poetry-spike-plan.md).
