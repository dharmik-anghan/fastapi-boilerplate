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
