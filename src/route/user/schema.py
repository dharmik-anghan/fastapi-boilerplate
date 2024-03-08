from typing import Optional, Union
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class OutputUserSchema(UserSchema):
    created_at: datetime
    is_verified: bool
    is_active: bool


class RegisterUserSchema(UserSchema):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class LoginUserSchema(BaseModel):
    username_or_email: str
    password: str


class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
