from pydantic import BaseModel, field_validator
from typing import Union


class Content(BaseModel):
    text: str


class ChatModel(BaseModel):
    user_id: Union[None, str] = None
    content: str
    user_name: Union[None, str] = None
