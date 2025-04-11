from typing import Optional
from passlib.context import CryptContext
from datetime import datetime
from repository.database.users import UsersRepository
from schema.users import User
from models.users import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> User:
        user_dict = user_data.model_dump(exclude={"password"})
        user_dict.update({
            "password_hash": pwd_context.hash(user_data.password),
            "is_active": True,
            "created_at": datetime.now()
        })

        return await self.repository.create_user(user_dict)

    async def get_users_by_group(self, group_id: int) -> list[User]:
        return await self.repository.get_users_by_group(group_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.repository.get_by_username(username)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.password_hash):
            return None
        return user
