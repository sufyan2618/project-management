from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    access_token: Optional[str] = None
    message: Optional[str] = None

class ErrorModel(BaseModel):
    success: bool
    error: str
    details: Optional[str] = None

class PaginationModel(BaseModel):
    total: int
    page: int
    size: int
    has_next: bool
    has_previous: bool
