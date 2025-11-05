from venv import logger
import requests
import os
import logging

BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")

logger = logging.getLogger("[FRONTEND][API]")
def get_movies(page: int = 1, page_size: int = 3):
    try:
        res = requests.get(f"{BASE_URL}/movies", params={"page": page, "page_size": page_size})
        res.raise_for_status()
        data = res.json()
        logger.info(f"✅ 영화 목록 요청 성공 (page={page})")
        return data  
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 목록 조회 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None


def get_movie(movie_id: int):
    try:
        res = requests.get(f"{BASE_URL}/movie", params={"movie_id": movie_id})
        res.raise_for_status()
        logger.info(f"✅ 영화 상세 정보 조회 성공")
        return res.json()["data"]
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 상세 정보 조회 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None
    

def get_genres():
    try:
        res = requests.get(f"{BASE_URL}/movies/genres")
        res.raise_for_status()
        return res.json()["data"]
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 장르 목록 조회 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None

def create_movie(payload: dict):
    try:
        res = requests.post(f"{BASE_URL}/movies", json=payload)
        res.raise_for_status()
        logger.info("✅ 영화 등록 성공")
        return res
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 추가 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None

def delete_movie(movie_id: int):
    try:
        res = requests.delete(f"{BASE_URL}/movies/{movie_id}")
        res.raise_for_status()
        logger.info("✅ 영화 삭제 성공")
        return res
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 삭제 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None

def create_review(payload:dict):
    try:
        res = requests.post(f"{BASE_URL}/reviews", json=payload)
        res.raise_for_status()
        logger.info("✅ 리뷰 등록 성공")
        return res
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 리뷰 추가 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None
def get_reviews(movie_id:int | None, page: int = 1, page_size: int =10):
    try:
        params={"page": page, "page_size": page_size}
        if movie_id:
            params["movie_id"] = movie_id
        res = requests.get(f"{BASE_URL}/reviews", params=params)
        res.raise_for_status()
        logger.info("✅ 영화 리뷰 조회 성공")
        return res
    except requests.exceptions.HTTPError as e:
        try:
            error_data = e.response.json()
            message = error_data.get("message", str(e))
        except Exception:
            message = str(e)
        logger.error(f"❌ 영화 리뷰 조회 실패: {message}")
        return e.response  # ✅ response 자체 반환
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 서버 통신 오류: {e}")
        return None