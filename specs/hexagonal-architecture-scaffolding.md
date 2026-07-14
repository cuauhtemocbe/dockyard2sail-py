---
title: Scaffold hexagonal architecture folders (domain/services/infrastructure)
status: completed
created: 2026-07-13
updated: 2026-07-13
issue: #5
---

# Scaffold hexagonal architecture folders (domain/services/infrastructure)

## Objective

Que quien clone este template arranque con la convención de arquitectura hexagonal ya presente, en vez de inventarla desde cero.

## Context / User Story

Ver issue [#5](https://github.com/cuauhtemocbe/dockyard2sail-py/issues/5) — 3 escenarios Gherkin son la fuente de verdad. El ejemplo (`PaymentGateway`) reutiliza literalmente el ejemplo documentado en `CLAUDE.md` para mantener docs y código sincronizados.

## Requirements

1. `src/app/domain/`, `src/app/services/`, `src/app/infrastructure/` como paquetes Python importables (`app.domain`, `app.services`, `app.infrastructure`).
2. `domain/ports.py` con un `Protocol` de ejemplo (`PaymentGateway`), sin herencia — tipado estructural puro.
3. `services/payment_service.py` con un service de ejemplo (`FakePaymentGateway` cumple `PaymentGateway` por duck typing, sin heredar; `process_payment` lo consume).
4. README documenta la estructura de 4 capas con la responsabilidad de cada una.

## Boundaries

**Out of scope**: mover `config.py` (#4, ya implementado, vive en la raíz de `app/`) a alguna de estas capas — el issue no lo pide. `infrastructure/` queda vacío salvo `__init__.py`: el issue no exige un ejemplo ahí, solo que sea importable.

## Success Criteria

- [x] `import app.domain`, `import app.services`, `import app.infrastructure` no fallan (test `test_domain_services_infrastructure_are_importable`).
- [x] `domain/ports.py` pasa `ruff check` sin errores.
- [x] README lista `api/`, `domain/`, `services/`, `infrastructure/` con su responsabilidad en la sección "Estructura".
- [x] Cobertura 100%, `make lint` y `make format-check` en verde.

## Implementation Plan

Directo a implementación — Effort: S.
