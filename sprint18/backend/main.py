from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from utils.exception_handler import http_exception_handler, validation_exception_handler
from routers import movie, review
from model.database import init_db

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 앱 시작 중: DB 초기화 실행")
    await init_db()
    yield
    print("🛑 앱 종료 중: 정리 작업 가능")


app = FastAPI(title="Movie Sentiment API", lifespan=lifespan)

# 커스텀 예외 핸들러
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.include_router(movie.router)
app.include_router(review.router)

