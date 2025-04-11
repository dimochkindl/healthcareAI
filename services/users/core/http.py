from typing import Union, Any


async def create_response(
        data: Union[Any, dict] = None,
        code: int = 200,
        description: str = None,
        message: str = None
)-> dict:
    _response = {
        'code': 200 if code is None else code,
        'description': description,
        'message': message,
        'data': data
    }

    return _response
