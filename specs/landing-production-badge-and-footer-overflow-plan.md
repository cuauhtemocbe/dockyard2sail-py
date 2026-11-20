# Implementation Plan: Landing page in production — environment badge and no horizontal scroll

**Spec**: [landing-production-badge-and-footer-overflow.md](./landing-production-badge-and-footer-overflow.md)
**Created**: 2026-11-19
**Status**: in-progress

## Components

### 1. Badge test
- **Purpose**: fijar que la landing refleja `settings.environment == production` y no contiene `development`.
- **Files**: `tests/test_web.py`
- **Effort**: XS

### 2. Browser test infrastructure
- **Purpose**: correr Chromium headless dentro del contenedor de desarrollo y servir la app en un puerto libre.
- **Files**: `pyproject.toml`, `poetry.lock`, `Dockerfile.dev`, `tests/conftest.py`
- **Effort**: S

### 3. Overflow test + CSS fix
- **Purpose**: medir `scrollWidth <= innerWidth` a 320/390/768/1280 px y corregir `body`.
- **Files**: `tests/test_landing_layout.py`, `src/app/static/css/landing.css`
- **Effort**: XS

## Dependencies

### Build Order
1. Browser test infrastructure (el test de overflow lo necesita).
2. Overflow test (rojo) → CSS fix (verde).
3. Badge test (independiente, verde desde el inicio).

### External Dependencies
- `pytest-playwright` (solo grupo dev): Chromium headless.

## Risks & Assumptions

### Risks
- **El browser no arranca como root en Docker**: pasar `--no-sandbox` cuando `os.geteuid() == 0`.
- **La imagen de desarrollo crece y CI tarda más**: aceptado; CI ya construye `Dockerfile.dev` en `make test`.
- **Falla de `apt` al instalar dependencias del browser**: si pasa, parar y reportar.

### Assumptions
- `pyproject.toml` no está montado: hay que reconstruir la imagen (`docker compose build`).
- La causa del overflow es `body` en fila (confirmado en el browser: `scrollWidth` 401 a 390 px).

## Milestones

- [ ] Tests escritos; el de overflow falla por la razón correcta (401 > 390).
- [ ] CSS corregido; tests verdes.
- [ ] `make validate` verde.

## Tasks

**Slicing strategy**: Mixed — la infraestructura del browser bloquea el test de overflow (se construye primero); el badge y el overflow son slices independientes.

### Foundation
- [ ] **Task 1**: dependencia `pytest-playwright` (dev) + Chromium en `Dockerfile.dev`
  - **Acceptance**: `docker compose exec api python -c "from playwright.sync_api import sync_playwright"` funciona; el browser arranca headless.
  - **Files**: `pyproject.toml`, `poetry.lock`, `Dockerfile.dev`
  - **Tests**: n/a (infraestructura)
  - **Effort**: S

### Slice 1: The environment badge shows production
- [ ] **Task 2**: test del badge en producción
  - **Acceptance**: pasa; `development` no aparece en el HTML.
  - **Files**: `tests/test_web.py`
  - **Tests**: `GET /` con `settings.environment = production`.
  - **Effort**: XS

### Slice 2: The page does not scroll horizontally
- [ ] **Task 3**: test de overflow (rojo) y fix de CSS (verde)
  - **Acceptance**: falla a 390 px antes del fix; pasa a los 4 anchos después.
  - **Files**: `tests/conftest.py`, `tests/test_landing_layout.py`, `src/app/static/css/landing.css`
  - **Tests**: Scenario Outline con 4 anchos.
  - **Effort**: S

## Effort Estimate

**Total Estimated Days**: 0.5
