from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):
    movie_id: int = Field(..., description="영화 ID", example=1)
    reviewer_name: str = Field(..., description="리뷰작성자", example="리뷰어1")
    content: str = Field(..., description="리뷰 내용", example="이 영화 정말 재미있어요!")


class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int = Field(..., description="리뷰 ID")
    sentiment: Optional[str] = Field(None, description="감정 분석 결과 (positive/negative/neutral)")
    score: Optional[float] = Field(None, description="감정 점수 (0.0 ~ 1.0)")
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True