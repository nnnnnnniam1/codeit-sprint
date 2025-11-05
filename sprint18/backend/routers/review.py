# Standard Library
from fastapi import APIRouter, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from requests import Session

# Schemas
from schemas.review import ReviewCreate
from schemas.pagination import Pagination, PaginationRequest
from schemas.response import DataResponseSchema, PaginationResponseSchema

# Models, Database
from model.database import get_db

# Services
from services.review_service import ReviewService
from services.movie_service import MovieService

# Utils
from utils.response import ResponseMessage


router = APIRouter(prefix="/reviews", tags=["Reviews"])    

# 서비스 의존성
def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    movie_service = MovieService(db)
    return ReviewService(db, movie_service)

@router.post("", response_model=DataResponseSchema, status_code=201, summary="리뷰 추가")
async def create(review: ReviewCreate, service:ReviewService = Depends(get_review_service)):
    result = await service.create(review)
    return ResponseMessage.CREATED(
        message="리뷰가 성공적으로 추가되었습니다.",
        data=jsonable_encoder(result)
    )

@router.get("", response_model=PaginationResponseSchema, summary="전체 영화 리뷰 목록 조회")
async def find_all(
    movie_id: int = Query(None, description="리뷰를 조회할 영화의 ID", example=1) ,
    params: PaginationRequest = Depends(),
    service:ReviewService = Depends(get_review_service)):
    
    pagination = Pagination(page=params.page, page_size=params.page_size)
    results, average_score, pagination = await service.find_all(pagination, movie_id)
    
    return ResponseMessage.PAGINATION(
        message="영화 리뷰 목록이 성공적으로 조회되었습니다.",
        data=jsonable_encoder({
            "average_score": average_score,
            "reviews": results
        }),
        pagination=pagination.to_schema()
    )
    

@router.get("/{review_id}", response_model=DataResponseSchema, summary="단일 영화 조회")
async def find_one(review_id: int, service:ReviewService = Depends(get_review_service)):
    review =  await service.find_one(review_id)
    return ResponseMessage.OK(
        message=f"리뷰가 성공적으로 조회되었습니다.",
        data = jsonable_encoder(review)
    )

# @router.delete("/{movie_id}", response_model=BaseResponseSchema, summary="영화 삭제")
# async def delete(movie_id: int, service:MovieService = Depends(get_movie_service)):
#     movie = await service.delete(movie_id)
#     return ResponseMessage.OK(
#         message=f"영화{movie.title}이/가 성공적으로 삭제되었습니다.",
#     )

