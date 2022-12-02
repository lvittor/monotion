from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: str = Field(..., alias = "_id")
    email: EmailStr = Field(..., alias = "email")
    username: str = Field(..., alias = "name")
    password: str = Field(..., alias = "password")
    ownerPages: Optional[list] = Field(..., alias = "ownerPages")
    editorPages: Optional[list] = Field(..., alias = "editorPages")
    viewerPages: Optional[list] = Field(..., alias = "viewerPages")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "1",
                "email": "example@gmail.com",
                "username": "user",
                "password": "password",
                "ownerPages": ["f7f91xw5", "914aad24"],
                "editorPages": ["wfa642ju", "acd22d14"],
                "viewerPages": ["5das7qh1", "8xcaxy21"]
            }
        }