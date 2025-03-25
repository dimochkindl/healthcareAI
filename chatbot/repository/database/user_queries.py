import sqlalchemy
from db.user_queries import user_queries
from repository.database.database import DatabaseRepository


class UserQueriesRepository(DatabaseRepository):

    @staticmethod
    async def create(values: dict):
        query = user_queries.insert(values)
        return await DatabaseRepository.execute(query)

    @staticmethod
    async def get_all(skip: int = 0, limit: int = 100):
        query = user_queries.select().offset(skip*limit).limit(limit)
        return await DatabaseRepository.fetch_all(query)

    @staticmethod
    async def get_by_user_id(user_id: int):
        query = user_queries.select().where(user_queries.c.user_id == user_id)
        return await DatabaseRepository.fetch_one(query)
