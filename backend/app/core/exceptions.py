from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

async def api_error_handler(request: Request, exc: HTTPException):
    """
    处理API错误
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def validation_error_handler(request: Request, exc):
    """
    处理请求验证错误
    """
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": str(exc)}
    )

async def general_exception_handler(request: Request, exc: Exception):
    """
    处理一般异常
    """
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)}
    )