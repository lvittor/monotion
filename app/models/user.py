from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr = Field(..., alias="email")
    username: str = Field(..., alias="name")
    password: str = Field(..., alias="password")
    ownerPages: Optional[list] = Field(None, alias="ownerPages")
    editorPages: Optional[list] = Field(None, alias="editorPages")
    viewerPages: Optional[list] = Field(None, alias="viewerPages")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "username": "user",
                "password": "password",
                "ownerPages": ["f7f91xw5", "914aad24"],
                "editorPages": ["wfa642ju", "acd22d14"],
                "viewerPages": ["5das7qh1", "8xcaxy21"],
            }
        }
