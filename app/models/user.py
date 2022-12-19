from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="name")
    password: str = Field(..., alias="password")
    pages: Optional[list] = Field(default_factory=list, alias="pages")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "username": "user",
                "password": "password",
                "pages": ["f7f91xw5", "914aad24"],
            }
        }
