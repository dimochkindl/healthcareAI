from core.db import DefaultBase, manage_session
from sqlalchemy import select
from typing import TypeVar, Type, List

T = TypeVar('T', bound=DefaultBase)

class DatabaseRepository:

    model: Type[T]

    @classmethod
    async def create(cls, data: dict) -> T:
        async with manage_session() as session:
            data = cls.model(**data)
            session.add(data)
            await session.commit()
            return data

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 15) -> List[T]:
        async with manage_session() as session:
            result = await session.execute(
                select(cls.model).offset(skip).limit(limit)
            )
            return result.scalars().all()

    @classmethod
    async def get_by_id(cls, id: int) -> T:
        async with manage_session() as session:
            return await session.get(cls.model, id)

    @classmethod
    async def update(cls, data: dict, id: int) -> T:
        async with manage_session() as session:
            db_object = await session.get(cls.model, id)
            if not db_object:
                raise ValueError(f'Cannot find object with id {id}')

            for key, value in data.items():
                setattr(db_object, key, value)

            await session.commit()
            await session.refresh(db_object)
            return db_object

    @classmethod
    async def delete(cls, id: int):
        object_from_db = cls.get_by_id(id)
        if not object_from_db:
            raise ValueError(f'Cannot find object with id {id}')

        async with manage_session() as session:
            await session.delete(object)
            session.commit()
