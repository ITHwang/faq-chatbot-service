from typing import Dict

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def health() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "alive"}
