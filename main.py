from fastapi import FastAPI, Request
import uvicorn
from logger import logger
from middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

logger.info("app started")


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello"}

@app.get("/upload-videos")
def upload_videos() -> dict:
    return {"message": "upload videos"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)