from fastapi import APIRouter
from ..core.config import app_config

router = APIRouter()

@router.get("/info")
def get_config():
    return {"config": app_config}
