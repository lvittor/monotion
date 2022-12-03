from datetime import datetime, timedelta
from typing import Union

from passlib.context import CryptContext
from jose import JWTError, jwt

from app.utils import MongoDBClient

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.models import TokenData

SECRET_KEY = "2e98402584bcf9bb7e5c10741522ca12f3842e865e2c91a8b5df052008c2d51f"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserVerificationClient:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """Verify password."""
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """Get password hash."""
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_user(cls, user_password: str, password: str) -> bool:
        """Verify user."""
        return cls.verify_password(password, user_password)

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme), database=Depends(MongoDBClient.get_database)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception

        user = database.users.find_one(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
