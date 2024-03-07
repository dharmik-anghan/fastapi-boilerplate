from fastapi import APIRouter
from src.controller.user.user import loginUser, registerUser
from src.route.user.schema import LoginUserSchema, RegisterUserSchema, OutputUserSchema, Token


user_router = APIRouter()


@user_router.post("/register", status_code=201, response_model=OutputUserSchema)
def register_user(request: RegisterUserSchema):
    """
    API: To create user
    """
    user = registerUser(request.model_dump())

    return user


@user_router.post("/login", status_code=200, response_model=Token)
async def login(request_data: LoginUserSchema):
    """
    API: To login user
    """
    user = loginUser(request_data.model_dump())

    return user


# @user_router.get("/me", )
