from fastapi import APIRouter, HTTPException
from ..services.proxy_service import request_through_proxy

router = APIRouter()

@router.get("/test")
def proxy_test(url: str):
    result = request_through_proxy(url)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
