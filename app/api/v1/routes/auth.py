from fastapi import APIRouter, Depends, Header, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import AuthService
from app.core.security import decode_access_token
from app.utils.response import error_response, success_response

router = APIRouter()
@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        return AuthService.register_user(db, user_data)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    try:
        return AuthService.login_user(db, login_data)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/me")
def get_me(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        return error_response("Missing or invalid token", status.HTTP_401_UNAUTHORIZED)

    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)
    if not token_data:
        return error_response("Invalid or expired token", status.HTTP_401_UNAUTHORIZED)

    try:
        user = AuthService.get_user_from_token(db, token_data)
        user_data = {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "role": user.role.value
        }
        return success_response("User profile retrieved successfully", user_data)
    except Exception as e:
        return error_response(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

