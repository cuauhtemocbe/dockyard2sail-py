---
title: Add LICENSE file
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #8
---

# Add LICENSE file

## Objective

Dar certeza legal a quien evalúe adoptar este template: bajo qué licencia puede usar, modificar y distribuir el código.

## Context / User Story

Ver issue [#8](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/8) — 3 escenarios Gherkin son la fuente de verdad. La issue sugería MIT "a confirmar"; el usuario confirmó MIT.

## Requirements

1. Archivo `LICENSE` en la raíz con texto MIT válido.
2. README referencia el archivo `LICENSE`.
3. CI verifica que `LICENSE` exista en la raíz.

## Boundaries

Fuera de alcance: licenciar dependencias de terceros individualmente (poetry.lock ya expresa sus propias licencias).

## Success Criteria

- [x] `LICENSE` existe en la raíz con texto MIT (copyright 2026 Kuautli).
- [x] `README.md` enlaza `./LICENSE`.
- [x] Job `license-check` en `ci.yml` falla si `LICENSE` no existe (`test -f LICENSE`).

## Implementation Plan

Directo a implementación — Effort: XS.
