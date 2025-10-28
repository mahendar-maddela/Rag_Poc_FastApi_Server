from fastapi import HTTPException, status
from app.repository import user_repository
from app.utils.hashing import Hash
from app.utils.token import create_access_token
from sqlalchemy.orm import Session

def login_user(email: str, password: str, db: Session):
    user = user_repository.get_user_by_email(email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")
    if not Hash.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
