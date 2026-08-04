---
title: Add CHANGELOG.md following Keep a Changelog + SemVer
status: completed
created: 2026-08-04
updated: 2026-08-04
issue: #33
---

# Add CHANGELOG.md following Keep a Changelog + SemVer

## Objective

Que mantenedores/consumidores puedan ver qué cambió entre versiones a nivel producto, sin leer el `git log` completo.

## Context / User Story

Ver issue [#33](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/33) — 2 escenarios Gherkin son la fuente de verdad. Repo template/referencia: no requiere backfill histórico completo, alcanza con `[Unreleased]` + `[0.1.0]`.

## Requirements

1. `CHANGELOG.md` en la raíz, formato [Keep a Changelog](https://keepachangelog.com/), secciones `Added`/`Changed`/`Fixed`/`Removed` por versión.
2. Sección `[Unreleased]` presente.
3. Al menos una sección versionada coincidiendo con `pyproject.toml` (`0.1.0`).

## Boundaries

**Out of scope**: backfill histórico de cada commit pasado.

## Success Criteria

- [x] `CHANGELOG.md` existe con formato Keep a Changelog.
- [x] `[Unreleased]` presente.
- [x] `[0.1.0]` presente, sincronizada con `pyproject.toml`.

## Implementation Plan

Directo a implementación — Effort: XS. Sin tests automatizados (documentación); se valida por lectura.
