from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/hello")
async def hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}
