---
title: Add Dependabot for dependency and base-image updates
status: completed
created: 2026-07-14
updated: 2026-07-14
issue: #20
---

# Add Dependabot for dependency and base-image updates

## Objective

Que `poetry.lock`, las versiones de GitHub Actions, y el digest de la imagen base pinneada en `Dockerfile` no queden obsoletos sin aviso.

## Context / User Story

Ver issue [#20](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/20) — 4 escenarios Gherkin son la fuente de verdad.

## Requirements

1. `.github/dependabot.yml` con tres `updates`: ecosystem `pip` (raíz del repo, resuelve `pyproject.toml`/`poetry.lock`), `github-actions` (`.github/workflows`), `docker` (raíz, resuelve `Dockerfile`).
2. Schedule razonable (semanal) para no generar ruido excesivo de PRs.

## Boundaries

**Out of scope**: auto-merge de los PRs de Dependabot (decisión aparte, no pedida en el issue).

## Success Criteria

- [x] `.github/dependabot.yml` declara los 3 ecosystems.
- [x] El YAML es válido (verificado con `python -c "import yaml; yaml.safe_load(...)"`; la activación real se confirma en Insights tras el merge).

## Implementation Plan

Directo a implementación — Effort: XS. Sin tests automatizados posibles (config de plataforma), se valida con un linter YAML local.
