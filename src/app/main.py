import logging
from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config import settings

logger = logging.getLogger(__name__)


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

    @fastapi_app.exception_handler(Exception)
    async def handle_unexpected_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception while processing %s", request.url)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})

    return fastapi_app


app = create_app()
