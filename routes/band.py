from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from sqlmodel import Session, select
from typing import List, Annotated
from logger.main_logger import logger

from models.models import BandCreate, Band, GenreUrl, Album
from db import get_session

band_router = APIRouter()

@band_router.get("/", status_code=200)
async def get_bands(
    request: Request,  # Request comes first
    session: Session = Depends(get_session),
    genre: GenreUrl | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
) -> List[Band]:
    current_user = request.state 
    logger.info(f"User {current_user['username']} is accessing to all bands")
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [b for b in band_list if b.genre.value.lower() == genre.value.lower()]
    if q:
        band_list = [b for b in band_list if q.lower() in b.name.lower()]
    return band_list

@band_router.get("/{band_id}", status_code=200)
async def get_band(
    request: Request,
    band_id: Annotated[int, Path(title="band_id")],
    session: Session = Depends(get_session),
) -> Band:
    current_user = request.state
    band = session.get(Band, band_id)
    if not band:
        raise HTTPException(status_code=404, detail=f"Band {band_id} not found")
    return band

@band_router.post("/", status_code=201)
async def create_band(
    request: Request,
    band_data: BandCreate,
    session: Session = Depends(get_session),
) -> Band:
    current_user = request.state.user  # Access the user information stored in request.state
    logger.info(f"User {current_user['username']} is creating a new band.")
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)
    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title=album.title, release_year=album.release_year, band=band)
            session.add(album_obj)
    session.commit()
    session.refresh(band)
    return band
