from pydantic import BaseModel, Field
from typing import Optional
from math import ceil


class PaginationRequest(BaseModel):
    """요청용 페이지네이션 (쿼리 파라미터 검증)"""
    page: int = Field(1, ge=1, description="페이지 번호 (1 이상)")
    page_size: int = Field(10, ge=1, le=100, description="페이지 크기 (1~100 사이)")


class PaginationResponse(BaseModel):
    """응답용 페이지네이션 정보"""
    page: int
    page_size: int
    total_pages: int
    total_count: int


class Pagination:
    """내부 계산용 클래스 (DB 조회용)"""
    def __init__(self, page: int = 1, page_size: int = 10):
        self.page = page
        self.page_size = page_size
        self.total_pages = 0
        self.total_count = 0

    def offset(self) -> int:
        """SQL OFFSET 계산"""
        return (self.page - 1) * self.page_size

    def set_total(self, total_count: int):
        """전체 개수 기반으로 total_pages 계산"""
        self.total_count = total_count
        self.total_pages = ceil(total_count / self.page_size) if self.page_size > 0 else 1
        return self

    def to_schema(self) -> PaginationResponse:
        """응답용 Pydantic 모델로 변환"""
        return PaginationResponse(
            page=self.page,
            page_size=self.page_size,
            total_pages=self.total_pages,
            total_count=self.total_count
        )
