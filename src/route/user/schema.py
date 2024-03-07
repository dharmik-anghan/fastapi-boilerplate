from typing import Optional, Union
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class RegisterUserSchema(UserSchema):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None

class LoginUserSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
