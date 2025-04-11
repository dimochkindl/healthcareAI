from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schema.users import User, user_groups


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users_by_group(self, group_id: int) -> list[User]:
        result = await self.session.execute(
            select(User)
            .join(user_groups, user_groups.c.user_id == User.id)
            .where(user_groups.c.group_id == group_id)
        )
        return list(result.scalars().all())

    async def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()