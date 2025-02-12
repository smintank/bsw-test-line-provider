import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/events/")
async def get_events():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://fastapi-app:8080/events")
    return response



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
