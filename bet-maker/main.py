import uvicorn
import logging
from fastapi import FastAPI

from config import settings
from api import router as bet_router

logger = logging.getLogger(__name__)


app = FastAPI(debug=settings.debug)
app.include_router(bet_router)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bet maker")
    uvicorn.run(app, host="0.0.0.0", port=8888)
