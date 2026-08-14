# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Página de aterrizaje interactiva en `GET /` (antes 404, API pura JSON): plantillas Jinja2 + archivos estáticos, con demo en vivo del endpoint `/api/v1/hello` y chequeo de estado del servicio.
- `docs/development-standards.md`: estándar de prácticas de desarrollo (Docker-first, hooks, CI, arquitectura hexagonal, config, TDD) documentado en el propio repo.

### Changed

- Imagen base bumpeada de `python:3.13-slim` a `python:3.14-slim` (prod y dev).
- Contenedor de desarrollo (`Dockerfile.dev`) corre como root a propósito, para que los bind mounts de `src/`/`tests/` queden escribibles sin desajuste de UID — asimetría documentada frente al `Dockerfile` de producción (no-root).
- `actions/checkout` y dependencias de desarrollo (`pytest-asyncio`, `mypy`, `pytest-cov`) actualizadas vía Dependabot.
- README: badges del stack, screenshot de la landing page y diagrama de arquitectura; texto sincronizado con la versión de Python y la estructura actual del código.

### Fixed

- Copy de la landing page ajustado a español mexicano.

### Security

- CVEs sin fix de `perl` (heredados del bump a `python:3.14-slim`) allowlisteados explícitamente en `.trivyignore.yaml`, con fecha de re-revisión.

## [0.1.0] - 2026-08-04

Línea base del template: skeleton FastAPI con arquitectura hexagonal, pipeline de CI y tooling de desarrollo containerizado.

### Added

- Skeleton FastAPI con separación `api/` / `domain/` / `services/` / `infrastructure/` (arquitectura hexagonal, `typing.Protocol` para contratos de dominio).
- Configuración tipada con `pydantic-settings` (`.env` + variables de entorno).
- Pipeline de CI: lint, test con cobertura mínima 90%, typecheck (mypy strict), verificación de `poetry.lock`, verificación de LICENSE, escaneo de seguridad con Trivy (filesystem e imagen).
- Dependabot para `pip`, `github-actions` y `docker`.
- Manejador global de excepciones y CORS configurable.
- Dockerfiles separados para desarrollo y producción, con healthcheck y digest de imagen base pinneado.
- Hook de pre-commit nativo (ruff lint + format check).
- Makefile autodocumentado, Docker-first.
- Licencia MIT.

[Unreleased]: https://github.com/cuauhtemocbe/dockyard2sail-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/cuauhtemocbe/dockyard2sail-py/releases/tag/v0.1.0
