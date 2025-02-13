from fastapi import APIRouter
from crud import fetch_available_events


router = APIRouter()

@router.get("/")
async def get_available_events():
    return await fetch_available_events()
