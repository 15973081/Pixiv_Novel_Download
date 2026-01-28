from fastapi import APIRouter
from ..services.login_service import simulate_login

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    result = simulate_login(username, password)
    return result
