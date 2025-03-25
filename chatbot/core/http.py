import typing


async def create_response(
    data: typing.Union[typing.Any, dict] = None,
    code: int = None,
    description: str = None,
    message: str = None,
    message_code: str = None
):

    _response = {
        "code": 200 if code is None else code,
        "description": description,
        "message": message,
        "message_code": message_code,
        "data": data,
    }
    if message_code is None:
        _response.pop("message_code")

    return _response


class ResponseException(Exception):
    def __init__(self, error: str, message_code: str = "", code: int = 400):
        self.error = error
        self.message_code = message_code
        self.code = code
