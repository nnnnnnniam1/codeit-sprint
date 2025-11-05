
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from utils.enums.sentiment_enum import SentimentEnum
from model.models import Review
from schemas.review import ReviewCreate
from schemas.pagination import Pagination
from utils.response import ResponseMessage
from sentiment.analyzer import analyze_sentiment
from services.movie_service import MovieService

class ReviewService:
    def __init__(self, db: AsyncSession, movie_service: MovieService):
        self.db = db
        self.movie_service = movie_service
    
    async def create(self, review: ReviewCreate):
        
        # 영화 존재 여부 검증
        await self.movie_service.find_one(review.movie_id)
        
        # 중복 확인
        existing = await self.db.execute(
            select(Review)
            .options(selectinload(Review.movie))
            .where(
                Review.movie_id == review.movie_id,
                Review.reviewer_name == review.reviewer_name,
            )
        )
        
        existing = existing.scalars().first()
        
        if existing:
            raise ResponseMessage.BAD_REQUEST(f"이미 등록된 리뷰입니다: {existing.movie.title} | {review.reviewer_name}")
        
        
        # 리뷰 분석
        sentiment, score = analyze_sentiment(review.content)
                        
        db_review = Review(**review.model_dump())
        db_review.sentiment = sentiment
        db_review.score = score
        
        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)
        return db_review
    
    async def find_all(self, pagination: Pagination = Pagination(), movie_id: int = None):
        """영화 리뷰 목록 조회"""
        offset = pagination.offset()
        
        # 리스트 조회
        query = (
            select(Review)
            .where(Review.deleted_at.is_(None))
            .order_by(Review.created_at.desc())
            .offset(offset)
            .limit(pagination.page_size)
        )
        
        # 점수 조회
        avg_query = select(Review.sentiment, Review.score).where(Review.deleted_at.is_(None))
        
        # 기본 카운트 쿼리
        count_query = select(func.count(Review.id)).where(Review.deleted_at.is_(None))

        if movie_id is not None:
            # 영화 존재 여부 검증
            await self.movie_service.find_one(movie_id)
            query = query.where(Review.movie_id == movie_id)
            count_query = count_query.where(Review.movie_id == movie_id)
            avg_query = avg_query.where(Review.movie_id == movie_id)
        else:
            query = query.options(selectinload(Review.movie))
        
        
        result = await self.db.execute(query)
        reviews = result.scalars().all()
        
        # 평균 평점 계산
        avg_result = await self.db.execute(avg_query)
        all_reviews = avg_result.all()
        ratings = [
            self.sentiment_to_rating(sentiment, score)
            for sentiment, score in all_reviews
            if sentiment and score is not None
        ]
        average_score = round(sum(ratings) / len(ratings), 3) if ratings else None
        
        # 감정라벨
        for review in reviews:
            review.sentiment_label = SentimentEnum[review.sentiment].label
        
        # 전체 개수
        total_count = (await self.db.execute(count_query)).scalar_one()
        pagination.set_total(total_count)

        
        return reviews, average_score, pagination
    
    async def find_one(self, review_id: int):
        """단일 리뷰 조회"""
        result = await self.db.execute(
            select(Review).where(
                Review.id == review_id,
                Review.deleted_at.is_(None)
            )
        )
        review = result.scalars().first()
        
        if not review:
            ResponseMessage.NOT_FOUND("해당 리뷰를 찾을 수 없습니다.")
        
        review.sentiment_label = SentimentEnum[review.sentiment].label
        
        return review
    
    async def delete(self, review_id: int):
        """리뷰 삭제"""

        existing = await self.db.execute(
            select(Review).where(Review.id == review_id)
        )
        review = existing.scalars().first()
        
        if not review:
            ResponseMessage.NOT_FOUND("해당 리뷰를 찾을 수 없습니다.")
        
        # await self.db.delete(movie)
        review.soft_delete()
        
        
        await self.db.commit()
        await self.db.refresh(review)
        return review



    @staticmethod
    def sentiment_to_rating(sentiment: str, score: float) -> float:
        weight_map = {
            SentimentEnum.VERY_NEGATIVE: 0.0,
            SentimentEnum.NEGATIVE: 0.25,
            SentimentEnum.NEUTRAL: 0.5,
            SentimentEnum.POSITIVE: 0.75,
            SentimentEnum.VERY_POSITIVE: 1.0
        }
        base = weight_map.get(sentiment, 0.5)
        return base * score  # 감정 방향 * 확신도 모두 반영
