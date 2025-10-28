from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.response import success_response, error_response

class AuthService:
    @staticmethod
    def register_user(db, user_data):
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            return error_response("Email already registered", status.HTTP_400_BAD_REQUEST)

        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        UserRepository.create_user(db, new_user)
        user_data = {
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name,
            "role": new_user.role.value
        }
        return success_response("User registered successfully", user_data, status.HTTP_201_CREATED)

    @staticmethod
    def login_user(db, login_data):
        user = UserRepository.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            return error_response("Invalid email or password", status.HTTP_401_UNAUTHORIZED)

        token = create_access_token({"sub": user.email})
        return success_response("Login successful", {
            "access_token": token,
            "token_type": "bearer"
        })

    @staticmethod
    def get_user_from_token(db, token_data):
        email = token_data.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = UserRepository.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
