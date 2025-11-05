from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

async def http_exception_handler(request: Request, exc: HTTPException):
    """HTTPException 핸들러"""
    
    detail = exc.detail if isinstance(exc.detail, dict) else {"error": exc.detail}
    
    response_content = {
        "status_code": exc.status_code,
        "message": detail.get("error", "오류가 발생했습니다"),
    }
    # data가 있으면 포함
    if "data" in detail and detail["data"] is not None:
        response_content["data"] = detail["data"]
        
    return JSONResponse(
        status_code=exc.status_code,
        content=response_content
    )
    
    

async def validation_exception_handler(request: Request, exc: HTTPException):
    """ValidationError 핸들러"""
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc not in ("body", "query", "path"))
        msg = err.get("msg", "")
        input_val = err.get("input", None)
        errors.append({
            "field": field,
            "error": f"{msg} (입력값: {input_val})" if input_val is not None else msg
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": 422,
            "message": "요청 데이터 형식이 올바르지 않습니다.",
            "errors": errors
        }
    )