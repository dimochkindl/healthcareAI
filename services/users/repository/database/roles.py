from sqlalchemy import select
from core.db import manage_session
from repository.db import DatabaseRepository
from schema.users import Role, user_roles


class RolesRepository(DatabaseRepository):

    model = Role

    @staticmethod
    async def get_user_roles(user_id):
        async with manage_session() as session:
            roles = await session.execute(
                select(Role).join(user_roles, user_roles.c.role_id == Role.id).where (user_roles.c.user_id == user_id)
            )
        return roles.scalars().all()

    @staticmethod
    async def get_by_name( name):
        async with manage_session() as session:
            roles = await session.execute(
                select(Role).where(Role.name == name)
            )
        return roles.scalars().all()