from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.exceptions.http import HTTPException
from app.models import TokenData, User
from app.settings import settings
from app.utils import MongoDBClient
from app.views import ErrorResponse

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
    async def get_current_user(
        cls,
        token: str = Depends(oauth2_scheme),
        database=Depends(MongoDBClient.get_database),
    ):
        """Get current user."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=ErrorResponse(
                code=status.HTTP_401_UNAUTHORIZED,
                message="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            ).dict(exclude_none=True),
        )

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email: str = payload.get("sub")
            if not email:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = database.users.find_one({"email": token_data.email})
        if not user:
            raise credentials_exception
        return User(**user)

    @classmethod
    def create_access_token(
        cls, data: dict, expires_delta: Union[timedelta, None] = None
    ):
        """Create access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
