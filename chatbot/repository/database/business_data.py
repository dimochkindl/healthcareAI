import sqlalchemy
from db.contents import contents
from repository.database.database import DatabaseRepository
from repository.tools import get_values


class BusinessDataRepository(DatabaseRepository):

    @staticmethod
    async def create(values: dict):
        query = contents.insert().values(values)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def update(id: int, values: dict):
        query = contents.update().values(values).where(contents.c.id == id)
        result = await DatabaseRepository.execute(query)
        return result

    @staticmethod
    async def get_by_id(id: int):
        query = contents.select().where(contents.c.id == id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_external_id(external_id: str):
        query = contents.select().where(contents.c.external_id == external_id)
        result = await DatabaseRepository.fetch_one(query)
        return get_values(result)

    @staticmethod
    async def get_by_closest_l2_distance(embedding: list, limit: int = 3):

        query = (sqlalchemy
                 .select(contents.c.text,
                         contents.c.embedding.max_inner_product(embedding).label("score"))
                 .order_by(sqlalchemy.asc(contents.c.embedding.max_inner_product(embedding)))
                 .where(contents.c.embedding.max_inner_product(embedding) < -0.3)
                 .limit(limit)
                 )

        result = await DatabaseRepository.fetch_all(query)

        return get_values(result)
