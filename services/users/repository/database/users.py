from sqlalchemy import select
from services.users.repository.db import DatabaseRepository
from services.users.schema.users import User, user_groups
from services.users.core.db import DatabaseSessionManager


class UsersRepository(DatabaseRepository):

    def __init__(self, manager: DatabaseSessionManager):
        super().__init__(model=User, session_manager=manager)

    async def get_users_by_group(self, group_id):
        async with self.manager.manage_session as session:
            users = await session.execute(
                select(User).join(user_groups, user_groups.c.user_id == User.id).where(user_groups.group_id == group_id)
            )
        return users.scalars().all()
