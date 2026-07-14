from importlib.metadata import PackageNotFoundError, version

from fastapi import FastAPI

from app.api.routes import router


def _get_version() -> str:
    try:
        return version("dockyard2sail-py")
    except PackageNotFoundError:
        return "0.0.0-dev"


app = FastAPI(title="dockyard2sail-py", version=_get_version())
app.include_router(router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
