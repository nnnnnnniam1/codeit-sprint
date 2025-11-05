from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.encoders import jsonable_encoder
from requests import Session
from schemas.pagination import Pagination, PaginationRequest
from schemas.response import BaseResponseSchema, DataResponseSchema, PaginationResponseSchema
from services.movie_service import MovieService
from utils.response import ResponseMessage
from model.database import get_db
from schemas.movie import MovieCreate


router = APIRouter(prefix="/movies", tags=["Movies"])    

# 서비스 의존성
def get_movie_service(db: Session = Depends(get_db)) -> MovieService:
    return MovieService(db)

@router.get("/genres", response_model=DataResponseSchema, summary="장르 리스트 조회")
async def get(service:MovieService = Depends(get_movie_service)):
    genres = await service.find_all_genres()
    return ResponseMessage.OK(
        message="장르 리스트가 성공적으로 조회되었습니다.",
        data = jsonable_encoder(genres)
    )
    
@router.post("", response_model=DataResponseSchema, status_code=201, summary="영화 추가")
async def create(movie: MovieCreate, service:MovieService = Depends(get_movie_service)):
    result = await service.create(movie)
    return ResponseMessage.CREATED(
        message="영화가 성공적으로 추가되었습니다.",
        data=jsonable_encoder(result)
    )


@router.get("", response_model=PaginationResponseSchema, summary="영화 목록 조회")
async def find_all(
    params: PaginationRequest = Depends(),
    service:MovieService = Depends(get_movie_service)):
    
    pagination = Pagination(page=params.page, page_size=params.page_size)
    results, pagination = await service.find_all(pagination)
    
    return ResponseMessage.PAGINATION(
        message="영화 목록이 성공적으로 조회되었습니다.",
        data=jsonable_encoder(results),
        pagination=pagination.to_schema()
    )
@router.get("/{movie_id}", response_model=DataResponseSchema, summary="단일 영화 조회")
async def find_one(movie_id: int, service:MovieService = Depends(get_movie_service)):
    movie =  await service.find_one(movie_id)
    return ResponseMessage.OK(
        message=f"영화{movie.title}이/가 성공적으로 조회되었습니다.",
        data = jsonable_encoder(movie)
    )

@router.delete("/{movie_id}", response_model=BaseResponseSchema, summary="영화 삭제")
async def delete(movie_id: int, service:MovieService = Depends(get_movie_service)):
    movie = await service.delete(movie_id)
    return ResponseMessage.OK(
        message=f"영화{movie.title}이/가 성공적으로 삭제되었습니다.",
    )