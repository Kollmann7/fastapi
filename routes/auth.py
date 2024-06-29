from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, verify_token
from db import get_session
from models.user import User, UserCreate
from passlib.context import CryptContext
from logger.main_logger import logger


auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(username: str, session: Session = Depends(get_session)):
    return session.exec(select(User).where(User.username == username)).first()

def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = pwd_context.hash(user.hashed_password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    return "complete"

@auth_router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = get_user_by_username(user.username, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(user=user, session=session)

def authenticate_user(username: str, password: str, session: Session = Depends(get_session)):
    user = get_user_by_username(username, session)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user

@auth_router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    logger.info(f"User {form_data.username} is logging in")
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/verify-token/{token}")
async def verify_user_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}
