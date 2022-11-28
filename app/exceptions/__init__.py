"""Application implementation - exceptions."""
from app.exceptions.http import HTTPException, http_exception_handler

__all__ = ("HTTPException", "http_exception_handler")
