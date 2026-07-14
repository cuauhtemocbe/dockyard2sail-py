# dockyard2sail-py

![CI](https://github.com/cuauhtemocbe/dockyard2sail-py/actions/workflows/ci.yml/badge.svg)

Template base para proyectos de APIs REST con Python. Incluye configuración lista para desarrollo local y deploy en Railway u otros proveedores cloud.

## Stack

- **Python 3.13** + **FastAPI** + **Poetry**
- **Docker** (imagen separada para dev y prod; healthcheck + digest pin en producción)
- **pydantic-settings** para configuración tipada, validada al arranque
- **pytest** + **httpx** para tests async (cobertura mínima 90%, forzada en CI)
- **Ruff** para linting y formato (config explícita, enforced en CI y en un pre-commit hook)

## Estructura

Arquitectura hexagonal pragmática: separación entre presentación, dominio, lógica de negocio e infraestructura.

```
.
├── Dockerfile          # Imagen de producción
├── Dockerfile.dev      # Imagen de desarrollo (hot-reload)
├── docker-compose.yml  # Orquestación local
├── src/
│   └── app/
│       ├── main.py             # Aplicación FastAPI + /health
│       ├── config.py           # Settings tipados (pydantic-settings)
│       ├── api/                # Presentación: rutas HTTP
│       │   └── routes.py
│       ├── domain/              # Contratos (typing.Protocol), sin dependencias externas
│       │   └── ports.py
│       ├── services/             # Lógica de negocio, orquesta el dominio
│       │   └── payment_service.py
│       └── infrastructure/       # Implementaciones concretas (DB, APIs externas, etc.)
└── tests/
```

## Desarrollo

Todo el flujo corre dentro de Docker vía `make` (`make help` lista todos los targets con descripción):

```bash
make up               # Levantar en desarrollo con hot-reload
make test              # Tests con cobertura (mínimo 90%)
make lint               # ruff check
make format-check       # ruff format --check
make typecheck           # mypy (strict en src/, relajado en tests/)
make lock-check          # poetry check --lock (poetry.lock sincronizado con pyproject.toml)
make install-hooks      # Habilitar el pre-commit hook (lint + format antes de cada commit)
```

`install`, `run-local`, `test-local` y `lint-local` quedan como fallback opcional sin Docker (requieren Python 3.13 + Poetry instalados localmente).

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/api/v1/hello` | Saludo (`?name=`) |
| GET | `/docs` | Swagger UI |

## Deploy

Apunta tu proveedor al `Dockerfile` raíz. El puerto se configura vía la variable de entorno `PORT` (por defecto `8000`, inyectado dinámicamente por el proveedor). La imagen expone un `HEALTHCHECK` sobre `/health` y fija la imagen base a un digest específico para evitar drift.

```bash
# Build de producción local
docker build -t dockyard2sail-py .
docker run -p 8000:8000 dockyard2sail-py
```

**Nota sobre el pinning del base image**: `Dockerfile` (producción) fija `python:3.13-slim` a un digest `@sha256:...` específico para builds reproducibles — Dependabot propone el bump cuando hay una versión nueva (ver `.github/dependabot.yml`). `Dockerfile.dev` usa deliberadamente el tag flotante (sin digest): en desarrollo local pesa más recibir parches de seguridad automáticos en cada rebuild que la reproducibilidad exacta byte a byte.

## Variables de entorno

Copia `.env.example` como punto de partida:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Entorno de ejecución |
| `PORT` | `8000` | Puerto del servidor (inyectado por el proveedor cloud) |
| `CORS_ALLOWED_ORIGINS` | *(vacío)* | Orígenes permitidos separados por coma. Sin configurar, CORS queda deshabilitado (default seguro) |

## Licencia

[MIT](./LICENSE)
