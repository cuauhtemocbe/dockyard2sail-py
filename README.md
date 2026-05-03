# dockyard2sail-py

API REST con Python 3.13, FastAPI, Poetry y Docker.

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) >= 29
- [Poetry](https://python-poetry.org/docs/) >= 1.8 (solo para desarrollo local)
- Python 3.13 (solo para desarrollo local)

## Estructura

```
.
├── Dockerfile              # Multi-stage: dev (hot-reload) y prod
├── docker-compose.yml      # Orquestación para desarrollo
├── Makefile                # Comandos de conveniencia
├── pyproject.toml          # Dependencias y configuración del proyecto
├── src/
│   └── app/
│       ├── main.py         # Aplicación FastAPI + /health
│       └── api/
│           └── routes.py   # Rutas en /api/v1
└── tests/
    └── test_main.py        # Tests async con pytest + httpx
```

## Inicio rápido (Docker)

```bash
# Construir la imagen
make build

# Levantar la API con hot-reload en http://localhost:8000
make up

# Ver logs
make logs

# Detener
make down
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/health` | Estado del servicio |
| GET | `/api/v1/hello` | Saludo (param: `?name=`) |
| GET | `/docs` | Documentación interactiva (Swagger UI) |
| GET | `/redoc` | Documentación alternativa (ReDoc) |

## Tests

```bash
# Correr tests dentro del contenedor
make test

# Con salida detallada
make test-v
```

## Lint

```bash
make lint
```

## Desarrollo local

Requiere Python 3.13 instalado. En Ubuntu/Debian:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.13 python3.13-venv
```

```bash
poetry env use python3.13
make install      # instala dependencias
make run-local    # uvicorn con --reload en :8000
make test-local   # pytest local
make lint-local   # ruff local
```

## Variables de entorno

Copia `.env.example` y ajusta según necesites:

```bash
cp .env.example .env
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Entorno de ejecución |

## Dockerfile multi-stage

El `Dockerfile` define dos targets:

- **`dev`** — incluye dependencias de desarrollo y activa hot-reload con `watchfiles`.
- **`prod`** — solo dependencias de producción, sin herramientas de dev.

Para construir la imagen de producción:

```bash
docker build --target prod -t dockyard2sail-py:prod .
```
