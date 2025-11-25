import os
from passlib.context import CryptContext
from entities.models.user import User
from repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def register_user(email: str, password: str, username: str, type: str) -> User | None:

        existing_user_record = await UserRepository.get_user("email", email)
        if existing_user_record:
            raise ValueError("User with this email already exists.")

        hashed_password = UserService.hash_password(password)

        created_user_record = await UserRepository.create_user(
            email=email,
            hashed_password=hashed_password,
            username=username,
            type=type
        )
        return created_user_record


