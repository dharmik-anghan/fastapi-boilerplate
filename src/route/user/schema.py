from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str


class RegisterUserSchema(UserSchema):
    password: str
