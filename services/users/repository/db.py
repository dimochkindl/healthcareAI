from services.users.core.db import DatabaseSessionManager, DefaultBase
from sqlalchemy import select
from typing import TypeVar, Type

T = TypeVar('T', bound=DefaultBase)


class DatabaseRepository:

    def __init__(self, model: Type[T], session_manager: DatabaseSessionManager):
        self.session_manager = session_manager
        self.model = model

    async def create(self, data: dict) -> T:
        async with self.session_manager as session:
            data = self.model(**data)
            session.add(data)
            await session.commit()
            return data

    async def get_all(self, skip: int = 0, limit: int = 15) -> list[T]:
        async with self.session_manager as session:
            result = await session.fetch_all(
                select(self.model).offset(skip).limit(limit)
            )
            return result.scalars().all()

    async def get_by_id(self, id: int) -> T:
        async with self.session_manager as session:
            return await session.get(self.model(id=id))

    async def update(self, data: dict, id: int) -> T:
        async with self.session_manager as session:
            db_object = await session.get(self.model(id=id))
            if not db_object:
                raise ValueError(f'Can not fint in db object with id {id}')

            session.update(self.model(**data), id)
            await session.commit()
            await session.refresh(self.model(id=id))
            return db_object