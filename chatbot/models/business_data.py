from pydantic import BaseModel
from typing import Union


class Content(BaseModel):
    text: str


class ChatModel(BaseModel):
    user_id: Union[None, str] = None
    content: str
    user_name: Union[None, str] = None
