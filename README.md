# dockyard2sail-py

Template base para proyectos de APIs REST con Python. Incluye configuración lista para desarrollo local y deploy en Railway u otros proveedores cloud.

## Stack

- **Python 3.13** + **FastAPI** + **Poetry**
- **Docker** (imagen separada para dev y prod)
- **pytest** + **httpx** para tests async
- **Ruff** para linting y formato

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

## Inicio rápido

```bash
# Levantar en desarrollo con hot-reload
docker compose up

# Correr tests
docker compose run --rm api pytest

# Lint
docker compose run --rm api ruff check src
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/api/v1/hello` | Saludo (`?name=`) |
| GET | `/docs` | Swagger UI |

## Deploy

Apunta tu proveedor al `Dockerfile` raíz. El puerto se configura vía la variable de entorno `PORT` (por defecto `8000`).

```bash
# Build de producción local
docker build -t dockyard2sail-py .
docker run -p 8000:8000 dockyard2sail-py
```

## Variables de entorno

Copia `.env.example` como punto de partida:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Entorno de ejecución |
| `PORT` | `8000` | Puerto del servidor (inyectado por el proveedor cloud) |

## Licencia

[MIT](./LICENSE)
