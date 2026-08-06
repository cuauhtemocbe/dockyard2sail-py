---
title: Add an interactive landing page at GET /
status: completed
created: 2026-08-06
updated: 2026-08-06
issue:
---

# Add an interactive landing page at GET /

## Objective

Reemplazar el 404 actual en `GET /` por una landing page interactiva que sirva de demo real del boilerplate: pipeline visual del proceso CI/CD real del proyecto, más una demo funcional de los endpoints existentes (`/api/v1/hello`, `/health`) — sin nada simulado, todo lo que se ve en pantalla es tráfico real contra la propia API.

## Context / User Story

`dockyard2sail-ts` (el boilerplate hermano en TypeScript) tiene una landing animada en su raíz (fondo con gradiente, pipeline animado dev→push→deploy, un `fetch` simulado). `dockyard2sail-py` hoy es API pura — `/` devuelve 404. Quien clona este template como punto de partida no tiene ninguna señal visual de que el servicio esté vivo ni de qué expone. Esta feature le da paridad de producto al boilerplate Python y de paso funciona como smoke-test visual del API real (a diferencia del TS, que simula el fetch con un `setTimeout`).

## Requirements

### Functional Requirements

- [ ] `GET /` devuelve un `HTMLResponse` (renderizado con Jinja2) en vez de 404.
- [ ] La página muestra versión (`_get_version()`) y entorno (`settings.environment`) inyectados desde el backend en el momento del render — no hardcodeados en el HTML/JS.
- [ ] Pipeline animado que refleja el pipeline real de este repo: `lint/test/typecheck` → `trivy-fs` scan → `build` + Trivy image scan → deploy a Railway (gateado por el check suite de CI, como vimos en el incidente de producción de esta semana).
- [ ] Formulario (input de texto + botón) que dispara un `fetch` real a `GET /api/v1/hello?name=...` y renderiza la respuesta JSON tal cual vuelve del backend, con estados de loading/success/error.
- [ ] Indicador de salud que hace polling real a `GET /health` cada 5s y muestra un badge verde/rojo según el `status` devuelto.
- [ ] Vanilla JS, sin frameworks de frontend ni paso de build — servido directo como archivo estático.
- [ ] CSS y JS en archivos estáticos separados (no inline en el HTML), montados vía `StaticFiles`.

### Non-Functional Requirements

- [ ] No requiere autenticación ni sesión.
- [ ] No altera el comportamiento default de CORS (sigue deshabilitado salvo `CORS_ALLOWED_ORIGINS`).
- [ ] `/health` y `/api/v1/hello` no cambian su contrato ni comportamiento actual.

## Architecture

### Components

- `src/app/templates/index.html` — template Jinja2 con placeholders `{{ version }}` / `{{ environment }}`.
- `src/app/static/css/landing.css` — estilos de la landing.
- `src/app/static/js/landing.js` — animación del pipeline, fetch a `/api/v1/hello`, polling a `/health`.
- `src/app/api/web.py` — router nuevo, sin prefix (a diferencia de `api/routes.py` que usa `/api/v1`), con `GET /` renderizando el template.
- `main.py` — monta `StaticFiles` en `/static` e incluye el nuevo router.

### External Dependencies

- `jinja2`: requerido por `Jinja2Templates` de FastAPI. Nueva dependencia de producción en `pyproject.toml`.

## Testing Strategy

- Unit/integration (httpx + pytest, como el resto del proyecto): `GET /` devuelve 200, `Content-Type: text/html`, y el body contiene la versión y el entorno actuales.
- `GET /static/js/landing.js` y `GET /static/css/landing.css` devuelven 200 (assets servidos).
- El comportamiento del JS en el browser (fetch real, polling, animación) no se cubre con tests automatizados — se verifica manualmente en `docker compose up` antes de dar la feature por terminada.

## Boundaries & Constraints

### In Scope

- Landing HTML+CSS+JS servida por FastAPI, con datos reales del backend.

### Out of Scope

- Autenticación, dark mode, diseño responsive avanzado, i18n.
- Tests E2E de browser (Playwright/Selenium) para el JS.
- PWA/service worker, `favicon.ico` dedicado.
- Cualquier persistencia de datos nueva.

### Technical Constraints

- Sin frameworks de frontend (React/Vue/etc.) ni bundler — vanilla JS servido tal cual.
- Debe seguir la arquitectura hexagonal pragmática del proyecto: la landing es capa de presentación (`api/`), no toca `domain/`/`services/`.

## Success Criteria

- [x] `GET /` devuelve 200 con HTML que incluye versión y entorno actuales.
- [x] `GET /static/css/landing.css` y `GET /static/js/landing.js` devuelven 200.
- [x] El formulario en el browser dispara un fetch real a `/api/v1/hello` y muestra la respuesta (verificado manualmente).
- [x] El badge de salud refleja el estado real de `/health` vía polling (verificado manualmente).
- [x] `make test`, `make lint`, `ruff format` y `make typecheck` pasan sin errores nuevos.
- [x] `Dockerfile` sigue empaquetando `templates/` y `static/` sin cambios (ya cubierto por `COPY src/ ./src/`).
- [x] README actualizado con la nueva fila `GET /` en la tabla de Endpoints.

## Implementation Plan

**Effort**: M — nueva dependencia, 2 directorios nuevos, 1 router nuevo, ~150-200 líneas de CSS/JS, tests para la ruta nueva.

1. `poetry add jinja2` (dependencia de producción) + `poetry lock`.
2. Crear `src/app/templates/index.html` con el shell HTML y los placeholders Jinja2.
3. Crear `src/app/static/css/landing.css` y `src/app/static/js/landing.js`.
4. Crear `src/app/api/web.py`: router sin prefix, `GET /` usando `Jinja2Templates.TemplateResponse`, recibiendo versión/entorno vía contexto.
5. `main.py`: montar `StaticFiles(directory=...)` en `/static`, incluir el router de `web.py` en `create_app()`.
6. `tests/test_web.py`: test de `GET /` (200, contiene versión/entorno) y de los dos assets estáticos.
7. `make lint`, `ruff format src/ tests/`, `make typecheck`, `make test`.
8. Verificación manual en `docker compose up`: fetch real al formulario, polling de salud, animación del pipeline.
9. Actualizar tabla de Endpoints en `README.md`.

**Nota técnica**: `Jinja2Templates` requiere pasar el directorio absoluto (`Path(__file__).parent / "templates"`) para que funcione tanto en local (bind mount) como en la imagen Docker (`COPY src/ ./src/`), sin depender del `cwd` del proceso.
