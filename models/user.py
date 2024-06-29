from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String

class UserBase(SQLModel):
    username: str = Field(sa_column=Column("username", String, unique=True))
    hashed_password: str = Field(sa_column=Column("hashed_password", String))

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass