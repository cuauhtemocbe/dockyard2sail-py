---
title: Landing page in production — environment badge and no horizontal scroll
status: in-progress
created: 2026-11-19
updated: 2026-11-19
issue: #72
---

# Landing page in production — environment badge and no horizontal scroll

## Objective

Garantizar con tests automáticos que la landing (`GET /`) muestra el entorno real cuando `ENVIRONMENT=production` y que no genera scroll horizontal en teléfonos (320–1280 px). El badge es operativo (variable en Railway); el overflow es un bug de CSS.

## Context

Observado el 2026-11-19 en producción (ver #72): el badge dice `development` y a 390x844 la página hace scroll horizontal porque `.footer` mide 401 px.

- Badge: `Settings.environment` tiene default `development` (`src/app/config.py:17`). El código no está mal: en producción solo muestra `production` si el servicio define `ENVIRONMENT=production`. Cambiar el default queda descartado (el desarrollo local y `docker-compose.yml` dependen de él). Fijar la variable en Railway queda fuera de este spec (acción operativa pendiente del dueño).
- Overflow: confirmado en el browser. `body` es `display: flex` (fila) y `.footer` es hijo directo de `body` junto a `#app`, así que el footer se coloca a la derecha de la tarjeta en vez de debajo (a 390 px: `#app` left -26 / width 343, `.footer` left 317 / width 84, `scrollWidth` 401).

## Requirements

### Functional Requirements

- [ ] Test: con `settings.environment == production`, la landing muestra el badge `production` y el texto `development` no aparece en la página.
- [ ] Test de browser: a 320, 390, 768 y 1280 px, `document.documentElement.scrollWidth <= window.innerWidth` en la landing servida por la app.
- [ ] Fix de CSS mínimo en `landing.css`: el footer queda debajo de la tarjeta (`body` en columna).

### Non-Functional Requirements

- [ ] La imagen de producción y sus dependencias no cambian: `pytest-playwright` solo en el grupo `dev` de Poetry.
- [ ] El navegador headless se instala en `Dockerfile.dev` (flujo Docker-first); `make validate` sigue en verde.

## Architecture

### Components

- `tests/test_web.py`: test del badge en producción (httpx + `monkeypatch` sobre `settings`).
- `tests/test_landing_layout.py`: Scenario Outline de overflow con `pytest-playwright` contra un uvicorn real en un puerto libre.
- `src/app/static/css/landing.css`: `body` en columna.
- `Dockerfile.dev`: `playwright install --with-deps chromium`.

### External Dependencies

- `pytest-playwright` (dev only): único cambio en dependencias.

## Testing Strategy

### Unit Tests

Badge: `GET /` con `settings.environment` en `production`.

### E2E Tests

Overflow: Chromium headless real, 4 anchos, mide `scrollWidth` vs `innerWidth`. Debe fallar antes del fix de CSS (401 > 390) y pasar después.

## Boundaries & Constraints

### In Scope

- Los dos tests, el fix de CSS, la instalación del browser en la imagen de desarrollo, entrada en `CHANGELOG.md`.

### Out of Scope

- Cambiar el default de `Settings.environment`; tocar Railway o sus variables; la imagen de producción; reescribir el copy de la página.

### Technical Constraints

- `Dockerfile.dev` corre como root: Chromium necesita `--no-sandbox` en ese caso.
- `pyproject.toml` no está montado como volumen: añadir la dependencia exige reconstruir la imagen.

## Success Criteria

- [ ] El test de overflow falla antes del fix (401 > 390 a 390 px) y pasa a los 4 anchos después.
- [ ] El test del badge pasa (se espera verde desde el inicio: el código ya es correcto).
- [ ] `make validate` verde.
- [ ] Production check pendiente tras fijar `ENVIRONMENT=production` en Railway (Definition of Done de #72; por eso el PR usa `Refs #72`).

## Implementation Plan

Ver [landing-production-badge-and-footer-overflow-plan.md](./landing-production-badge-and-footer-overflow-plan.md).
