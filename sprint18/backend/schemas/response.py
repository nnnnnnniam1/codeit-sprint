from typing import Any, Optional
from pydantic import BaseModel

from schemas.pagination import PaginationResponse


class PaginationSchema(BaseModel):
    page: int
    page_size: int
    total_pages: int
    total_count: int

class BaseResponseSchema(BaseModel):
    status_code: int
    message: str

class DataResponseSchema(BaseResponseSchema):
    data: Optional[Any] = None

class PaginationResponseSchema(DataResponseSchema):
    pagination: Optional[PaginationResponse] = None