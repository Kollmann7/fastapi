from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager

from routes.auth import auth_router
from routes.band import band_router
from routes.orders import orders_router
from middleware import log_middleware
from logger.smtp_logger import listener

listener.start()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    listener.stop()

app = FastAPI(
    lifespan=lifespan,
    title="My API",
    description="API with JWT Authentication",
    version="1.0.0",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True, reload_dirs=["./"])
