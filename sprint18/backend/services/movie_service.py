from datetime import datetime, timezone
import re
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from torch import ge
from schemas.pagination import Pagination
from utils.response import ResponseMessage
from model.models import Genre, Movie
from schemas.movie import MovieCreate
import os

class MovieService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, movie: MovieCreate):
        # 중복 확인
        existing = await self.db.execute(
            select(Movie).where(
                Movie.title == movie.title,
                Movie.director == movie.director,
                Movie.deleted_at.is_(None)
            )
        )
        
        existing = existing.scalars().first()
        
        if existing:
            raise ResponseMessage.BAD_REQUEST(f"이미 등록된 영화입니다: {movie.title} ({movie.director})")
        
        # 포스터 경로
        if movie.poster and "http" in movie.poster:
            match = re.search(r"(movies/.*)", movie.poster)
            if match:
                movie.poster = match.group(1)
        
        # 장르
        genre_list = []
        for g in movie.genres:
            if g.id:
                genre = await self.db.get(Genre, g.id)
                if not genre:
                    raise ResponseMessage.NOT_FOUND(f"장르(id={g.id})를 찾을 수 없습니다.")
            elif g.genre:
                result = await self.db.execute(
                    select(Genre).where(Genre.genre == g.genre, Genre.deleted_at.is_(None))
                )
                genre = result.scalars().first()
                if not genre:
                    genre = Genre(genre=g.genre)
                    self.db.add(genre)
                    await self.db.flush()
            if genre and all(existing_genre.id != genre.id for existing_genre in genre_list):
                genre_list.append(genre)
        
        
                

        db_movie = Movie(
            title=movie.title,
            director=movie.director,
            release_date=movie.release_date,
            poster=movie.poster,
            genres=genre_list
        )
        self.db.add(db_movie)
        await self.db.commit()
        await self.db.refresh(db_movie)
        return db_movie
    
    async def find_all(self, pagination: Pagination = Pagination()):
        """영화 목록 조회"""
        offset = pagination.offset()
        
        result = await self.db.execute(
            select(Movie)
            .options(selectinload(Movie.genres))
            .where(Movie.deleted_at.is_(None))
            .order_by(Movie.release_date.desc())
            .offset(offset)
            .limit(pagination.page_size)
        )
        movies = result.scalars().all()
        
        # 전체 개수
        count_query = select(func.count(Movie.id)).where(Movie.deleted_at.is_(None))
        total_count = (await self.db.execute(count_query)).scalar_one()
        pagination.set_total(total_count)
        

        
        return movies, pagination
    
    async def find_one(self, movie_id: int):
        """단일 영화 조회"""
        result = await self.db.execute(
            select(Movie).where(
                Movie.id == movie_id,
                Movie.deleted_at.is_(None)
            )
        )
        movie = result.scalars().first()
        
        if not movie:
            raise ResponseMessage.NOT_FOUND("해당 영화를 찾을 수 없습니다.")
        
        
        return movie
    
    async def delete(self, movie_id: int):
        """영화 삭제"""

        existing = await self.db.execute(
            select(Movie)
            .options(selectinload(Movie.reviews))
            .where(Movie.id == movie_id)
        )
        movie = existing.scalars().first()
        
        if not movie:
            raise ResponseMessage.NOT_FOUND("해당 영화를 찾을 수 없습니다.")
        
        # await self.db.delete(movie)
        movie.soft_delete()
        
        # 영화 관련 리뷰도 삭제
        for review in movie.reviews:
            review.soft_delete()
        
        await self.db.commit()
        await self.db.refresh(movie)
        return movie

    async def find_all_genres(self):
        """장르 리스트 조회"""
        genres = await self.db.execute(
            select(Genre)
            .where(Genre.deleted_at.is_(None))
        )
        
        return [{"id": g.id, "genre": g.genre} for g in genres.scalars().all()]


    

    