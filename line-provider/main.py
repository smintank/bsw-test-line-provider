import logging

import uvicorn
from fastapi import FastAPI

from config import settings
from routes import router as events_router

logger = logging.getLogger(__name__)


app = FastAPI(title=settings.app_name, debug=settings.debug, root_path="/service")

app.include_router(events_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
