import logging

import uvicorn
from fastapi import FastAPI

from config import settings
from database import lifespan
from routes.bets import router as bet_router
from routes.events import router as event_router

logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name, lifespan=lifespan, debug=settings.debug)
app.include_router(bet_router, tags=["Bets"])
app.include_router(event_router, prefix="/events", tags=["Events"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
