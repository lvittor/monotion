from enum import Enum
import json
from typing import Dict, List, Optional
import uuid

from bson import json_util
from bson.objectid import ObjectId
from fastapi import Depends
from pydantic import BaseModel, Field, validator
from pymongo import MongoClient

from app.exceptions.http import HTTPException
from app.utils import MongoDBClient


class BlockType(Enum):  # TODO: define scope of block types
    """Block type enum."""

    TO_DO = "to_do"
    NOTE = "note"
    HEADING = "heading"
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    FILE = "file"
    LINK = "link"
    LIST = "list"
    TABLE = "table"
    QUOTE = "quote"
    CODE = "code"
    DIVIDER = "divider"
    BOOKMARK = "bookmark"
    EMBED = "embed"
    COLUMN_LIST = "column_list"
    COLUMN = "column"
    BULLETED_LIST = "bulleted_list"
    NUMBERED_LIST = "numbered_list"
    TOGGLE = "toggle"
    CHILD_PAGE = "child_page"
    CALL = "call"
    MAP = "map"
    EXPAND = "expand"
    BREADCRUMB = "breadcrumb"
    PAGE = "page"
    COLLECTION_VIEW = "collection_view"
    COLLECTION_VIEW_PAGE = "collection_view_page"
    COLLECTION = "collection"
    COLLECTION_QUERY = "collection_query"
    COLLECTION_GROUP = "collection_group"
    SEARCH = "search"
    BOARD = "board"
    BOARD_VIEW = "board_view"
    BOARD_VIEW_PAGE = "board_view_page"
    CALENDAR = "calendar"
    CALENDAR_VIEW = "calendar_view"
    CALENDAR_VIEW_PAGE = "calendar_view_page"
    FORMULA = "formula"
    RELATION = "relation"
    ROLLUP = "rollup"
    AGGREGATE = "aggregate"
    TRANSFORM = "transform"
    MERGE = "merge"
    FILTER = "filter"
    EXTRACT = "extract"
    WIDGET = "widget"
    TEMPLATE = "template"
    GIST = "gist"
    GIST_PAGE = "gist_page"
    EQUATION = "equation"
    PRESENTATION = "presentation"
    PRESENTATION_PAGE = "presentation_page"
    PDF = "pdf"
    PDF_PAGE = "pdf_page"
    DRIVE = "drive"
    DRIVE_PAGE = "drive_page"
    FUSION_TABLE = "fusion_table"
    FUSION_TABLE_PAGE = "fusion_table_page"
    CANVAS = "canvas"
    CANVAS_PAGE = "canvas_page"


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str) and not isinstance(v, ObjectId):
            raise TypeError(f"Get type {type(v)} instead of ObjectId or str")
        elif not ObjectId.is_valid(v):
            raise ValueError(f"The parent id {v} is not a valid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class BaseBlock(BaseModel):
    type: BlockType = Field(..., alias="type")
    properties: Dict = Field(..., alias="properties")
    parent: Optional[PydanticObjectId] = Field(None, alias="parent")

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        schema_extra = {
            "example": {
                "type": "to_do",
                "properties": {"title": "Hello World", "checked": "No"},
                "parent": "638c1390af999d33f67f16f5",
            }
        }

    def to_json(self):
        return json.loads(json_util.dumps(self.__dict__))

    def is_page(self):
        return self.type == BlockType.PAGE.value

    def is_valid_page(self):
        return self.is_page() and self.parent is None

    async def has_valid_parent(self):
        """Check if parent is None or exists in the database."""
        if not self.parent:
            return self.is_page()

        # Block has a parent. So, check if it exists in the database
        database: MongoClient = await MongoDBClient.get_database()
        return database.blocks.find_one({"_id": self.parent})

    async def is_valid_block(self):
        """
        Check if block is valid before inserting it into the database.
        It's difficult to implement since we need to define the scope of block types and their properties.
        """
        return (
            await self.has_valid_parent() and True
        )  # We need to do more validations here


class Block(BaseBlock):
    content: Optional[List[PydanticObjectId]] = Field(
        default_factory=list, alias="content", uniqueItems=True
    )
    editors: Optional[List[PydanticObjectId]] = Field(
        default_factory=list, alias="editors", uniqueItems=True
    )

    def __init__(self, **data):
        super().__init__(**data)

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: lambda v: str(v)}
        schema_extra = {
            "example": {
                "type": "to_do",
                "properties": {"title": "Hello World", "checked": "No"},
                "content": ["00315dfb", "bf2d3c32", "3070827f"],
                "editors": ["1", "2"],
                "parent": "638c2fde3d4ef9116671fd4a",
            }
        }


class BlockRequest(BaseBlock):
    pass
