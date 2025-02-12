from contextlib import asynccontextmanager

import uvicorn
import logging
from fastapi import FastAPI

from config import settings
from database import init_db
from routes.bets import router as bet_router
from routes.events import router as event_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan, debug=settings.debug)
app.include_router(bet_router)
app.include_router(event_router)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bet maker")
    uvicorn.run(app, host="0.0.0.0", port=8888)
