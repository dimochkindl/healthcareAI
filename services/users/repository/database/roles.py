from sqlalchemy import select
from services.users.core.db import DatabaseSessionManager
from services.users.repository.db import DatabaseRepository
from services.users.schema.users import Role, user_roles

class RolesRepository(DatabaseRepository):

    def __init__(self, manager: DatabaseSessionManager):
        super().__init__(Role, manager)

    async def get_user_roles(self, user_id):
        async with self.manager.manage_session() as session:
            roles = await session.execute(
                select(Role).join(user_roles, user_roles.c.role_id == Role.id).where (user_roles.c.user_id == user_id)
            )
        return roles.scalars().all()