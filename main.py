from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from routes.auth import auth_router
from routes.band import band_router
from routes.orders import orders_router
from middleware import log_middleware
from logger.smtp_logger import listener
from contextlib import asynccontextmanager

listener.start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    listener.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(band_router, prefix="/band", tags=["band"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])

@app.get("/")
def read_root() -> dict:
    return {"message": "Hello"}
