from fastapi import APIRouter, status, Request
from src.controller.user.user import registerUser
from src.route.user.schema import RegisterUserSchema, UserSchema


user_router = APIRouter()


@user_router.post("/register", status_code=201, response_model=UserSchema)
def register_user(request: RegisterUserSchema):
    """
    API: To create user
    """
    user = registerUser(request.model_dump())

    return user
