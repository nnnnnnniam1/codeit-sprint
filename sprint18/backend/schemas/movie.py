from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class MovieGenreInput(BaseModel):
    id: Optional[int] = Field(None, description="기존 장르 ID")
    genre: Optional[str] = Field(None, description="새 장르 이름")

    @property
    def is_existing(self) -> bool:
        return self.id is not None
    
class MovieBase(BaseModel):
    title: str = Field(..., description="영화 제목", example="인셉션")
    director: str = Field(..., description="감독 이름", example="크리스토퍼 놀란")
    release_date: date = Field(..., description="개봉일 (YYYY-MM-DD)", example="2010-07-16")
    poster: Optional[str] = Field(None, description="포스터 URL 또는 파일 경로", example="movies/inception.jpg")


class MovieCreate(MovieBase):
    genres: List[MovieGenreInput] = Field(
        ..., 
        description="장르 목록 (기존: id / 신규: genre)",
        example=[{"id": 1}, {"genre": "스릴러"}]
    )

class Movie(MovieBase):
    id: int = Field(..., description="영화 ID")

    class Config:
        from_attributes = True