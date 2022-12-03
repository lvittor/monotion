from enum import Enum
from typing import Optional
import uuid

from pydantic import BaseModel, Field


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


class Block(BaseModel):
    type: BlockType = Field(..., alias="type")
    properties: str = Field(..., alias="properties")
    content: Optional[list] = Field(..., alias="content")
    editors: Optional[list] = Field(..., alias="editors")
    parent: Optional[str] = Field(None, alias="parent")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
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


class BlockRequest(BaseModel):
    type: BlockType = Field(..., alias="type")
    properties: str = Field(..., alias="properties")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "type": "to_do",
                "properties": {"title": "Hello World", "checked": "No"},
            }
        }
