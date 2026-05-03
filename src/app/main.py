from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="dockyard2sail-py", version="0.1.0")
app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
