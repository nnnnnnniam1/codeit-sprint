
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Date, Table, func, null
from sqlalchemy.orm import relationship
from model.base_mixin import TimestampMixin
from model.database import Base


# movie genre 매핑 테이블
movie_genre_table = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
)

class Movie(Base, TimestampMixin):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String, index=True)
    release_date = Column(Date, index=True)
    poster = Column(String, nullable=True)
    
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
    genres = relationship(
        "Genre",
        secondary=movie_genre_table,
        back_populates="movies"
    )

class Genre(Base, TimestampMixin):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, index=True)
    genre = Column(String, unique=True, index=True)
    
    movies = relationship(
        "Movie",
        secondary=movie_genre_table,
        back_populates="genres"
    )

    
class Review(Base, TimestampMixin):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    reviewer_name = Column(String)
    content = Column(String)
    sentiment = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    
    movie = relationship("Movie", back_populates="reviews")