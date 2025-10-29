from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import decode_access_token
from app.services.auth_service import AuthService

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Extract user from Bearer token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = AuthService.get_user_from_token(db, token_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def admin_only(current_user=Depends(get_current_user)):
    """Allow only admin users"""
    if current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access only")
    return current_user
