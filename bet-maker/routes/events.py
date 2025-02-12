from fastapi import APIRouter
from crud import fetch_all_events


router = APIRouter(prefix="/events", tags=["events"])

@router.get("/")
async def get_events():
    return await fetch_all_events()
