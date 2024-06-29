import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from starlette import status

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()


# Create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid or expired")