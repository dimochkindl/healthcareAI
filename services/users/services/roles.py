from repository.database.roles import RolesRepository

class RoleService:

    @classmethod
    async def create(cls, values: dict):
        return await RolesRepository.create(data=values)

    @classmethod
    async def get_all(cls, skip: int = 0, limit: int = 15):
        return await RolesRepository.get_all(skip=skip, limit=limit)

    @classmethod
    async def get_by_name(cls, name: str):
        if not name:
            return None

        return await RolesRepository.get_by_name(name=name)

    @staticmethod
    async def get_by_id(id: int):
        return await RolesRepository.get_by_id(id=id)

    @staticmethod
    async def update(values: dict, id: int):
        return await RolesRepository.update(id=id, data=values)

    @staticmethod
    async def grant_user_roles(user_id: int, role_id: int):
        pass
