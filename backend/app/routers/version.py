from fastapi import APIRouter
from ..services.version_service import get_latest_version

router = APIRouter()

@router.get("/latest")
def latest():
    return get_latest_version()
