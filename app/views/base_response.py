"""Application implementation - ready response."""
from typing import Any, Dict, Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):

    success: Optional[bool]
    properties: Optional[Dict] = None
