from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.hashing import Hash

def create_user(request: schemas.user_schema.UserCreate, db: Session):
    new_user = models.user.User(
        username=request.username,
        email=request.email,
        hashed_password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(email: str, db: Session):
    return db.query(models.user.User).filter(models.user.User.email == email).first()
