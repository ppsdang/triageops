"""The complaint web page for support agents."""
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
PAGE = Path(__file__).parent / "static" / "index.html"


@router.get("/", include_in_schema=False)
async def home() -> FileResponse:
    return FileResponse(PAGE)
