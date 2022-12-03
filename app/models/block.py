from typing import Optional
import uuid

from pydantic import BaseModel, Field


class Block(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    type: str = Field(..., alias="type")
    properties: str = Field(..., alias="properties")
    content: Optional[list] = Field(..., alias="content")
    editors: Optional[list] = Field(..., alias="editors")
    parent: Optional[str] = Field(None, alias="parent")

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
                "parent": "2a59gah6",
            }
        }
