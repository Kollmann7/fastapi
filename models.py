from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship

class GenreChoices(Enum):
    rock = 'Rock'
    progressive_rock = 'Progressive Rock'
    hard_rock = 'Hard Rock'
    grunge = 'Grunge'
    alternative_rock = 'Alternative Rock'
    heavy_metal = 'Heavy Metal'
    punk_rock = 'Punk Rock'

class AlbumBase(SQLModel):
    title: str
    release_year: date
    band_id: Optional[int] | None = Field(default=None, foreign_key='band.id')

class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates='albums')

class BandBase(SQLModel):
    name: str
    genre: GenreChoices
    
class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates='band')

class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None
    
    @field_validator('genre', mode='before')
    def validate_genre(cls, v):
        return v.title()

class GenreUrl(Enum):
    rock = 'rock'
    progressive_rock = 'progressive_rock'
    hard_rock = 'hard_rock'
    grunge = 'grunge'
    alternative_rock = 'alternative_rock'
    heavy_metal = 'heavy_metal'
    punk_rock = 'punk_rock'
    nu_metal = 'nu_metal'
    psychedelic_rock = 'psychedelic_rock'
