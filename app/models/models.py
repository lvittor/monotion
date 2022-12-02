from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class Block(BaseModel):
    id: str = Field(..., alias = "_id")
    type: str = Field(..., alias = "type")
    properties: str = Field(..., alias = "properties")
    content: Optional[list] = Field(..., alias = "content")
    editors: Optional[list] = Field(..., alias = "editors")
    parent: Optional[str] = Field(None, alias = "parent")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "e7e93fae",
                "type": "to_do",
                "properties": """{
                        "title": "Hello World",
                        "checked": "No"
                    }""",
                "content": ["00315dfb", "bf2d3c32", "3070827f"],
                "editors": ["1", "2"],
                "parent": "2a59gah6"
            }
        }
                
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