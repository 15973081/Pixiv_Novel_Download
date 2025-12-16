from fastapi import APIRouter
from ..services.proxy_service import request_through_proxy

router = APIRouter()

@router.get("/test")
def proxy_test(url: str):
    return request_through_proxy(url)
