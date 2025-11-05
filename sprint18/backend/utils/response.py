

from fastapi import HTTPException, status

from schemas.pagination import Pagination


class ResponseMessage:
    @staticmethod
    def OK(message: str = "성공적으로 처리되었습니다", data: dict | None = None):
        return {
            "status_code": 200,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def CREATED(message: str = "성공적으로 생성되었습니다", data: dict | None = None):
        return {
            "status_code": 201,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def BAD_REQUEST(message: str = "잘못된 요청입니다"):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail={"error": message}
        )
        
    @staticmethod
    def PAGINATION(data: list, pagination: Pagination, message: str="데이터 조회 성공"):
        return {
            "status_code": 200,
            "message": message,
            "data": data,
            "pagination": pagination
        }
    
    @staticmethod
    def NOT_FOUND(message: str = "요청한 리소스를 찾을 수 없습니다"):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail={"error": message}
        )    
    
    @staticmethod
    def INTERNAL_SERVER_ERROR(message: str = "서버 내부 오류가 발생했습니다"):
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": message
            }
        )
    
    @staticmethod
    def CUSTOM_ERROR(status_code: int, message: str):
        raise HTTPException(
            status_code = status_code,
            detail={"error": message}
        ) 