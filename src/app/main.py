from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings


def _get_version() -> str:
    try:
        return version("dockyard2sail-py")
    except PackageNotFoundError:
        return "0.0.0-dev"


def create_app() -> FastAPI:
    fastapi_app = FastAPI(title="dockyard2sail-py", version=_get_version())
    fastapi_app.include_router(router)

    if settings.cors_allowed_origins:
        fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @fastapi_app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return fastapi_app


app = create_app()
