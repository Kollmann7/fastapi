from fastapi import FastAPI, Path, Query, Depends
import uvicorn
from logger import logger
from middleware import log_middleware
from starlette.middleware.base import BaseHTTPMiddleware
import starlette.status as status

from typing import Annotated
from models import BandCreate, Band, GenreUrl, Album

from db import init_db, get_session
from sqlmodel import Session, select

from contextlib import asynccontextmanager

@asynccontextmanager
async def livespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=livespan)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello"}

@app.get("/bands", status_code=status.HTTP_200_OK)
async def bands(
    genre: GenreUrl | None = None, 
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
    ) -> list[Band]:

    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [b for b in band_list if b.genre.value.lower() == genre.value.lower()]
    if q:
        band_list = [b for b in band_list if q.lower() in b.name.lower()]
        
    return band_list

@app.get("/bands/{band_id}", status_code=status.HTTP_200_OK)
async def bands(
    band_id: Annotated[int, (0, Path(title="band_id"))],
    session: Session = Depends(get_session),

) -> Band:
    # band =  next((Band(**b) for b in BANDS if b['id'] == band_id), None)
    band = session.get(Band, band_id)
    if band is None:
        raise ValueError(status_code=status.HTTP_404_NOT_FOUND, detail=f"Band {band_id} not found")
    return band

@app.post("/bands", status_code=status.HTTP_201_CREATED)
async def bands(
    band_data: BandCreate,
    session: Session = Depends(get_session),
    ) -> Band:

    
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title=album.title, release_year=album.release_year, band=band)
            session.add(album_obj)

    session.commit()
    session.refresh(band)

    return band
