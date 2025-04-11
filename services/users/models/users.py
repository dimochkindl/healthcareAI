from pydantic import BaseModel, ValidationError, PlainValidator, EmailStr
from typing import Annotated

def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any (char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one number")
    if not any (char.isalpha() for char in password):
        raise ValidationError("Password must contain at least one letter")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter")
    return password


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: Annotated[str, PlainValidator(validate_password)]


