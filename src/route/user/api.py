from fastapi import APIRouter, Depends, Request
from src.controller.user.user import loginUser, registerUser, resetPassword, verifyToken
from src.route.user.schema import (
    LoginUserSchema,
    RegisterUserSchema,
    OutputUserSchema,
    ResetPasswordSchema,
    Token,
)


user_router = APIRouter()


@user_router.post("/register", status_code=201, response_model=OutputUserSchema)
def register_user(request: RegisterUserSchema):
    """
    API: To create user
    """
    user = registerUser(request.model_dump())

    return user


@user_router.post("/login", status_code=200, response_model=Token)
def login(request_data: LoginUserSchema):
    """
    API: To login user
    """
    user = loginUser(request_data.model_dump())

    return user


@user_router.get("/me", status_code=200, response_model=OutputUserSchema)
def user_profile(authorized_user=Depends(verifyToken)):
    """
    API: To get user profile
    """

    return authorized_user


@user_router.put("/reset-password", status_code=200)
def reset_password(request_data: ResetPasswordSchema, authorized_user=Depends(verifyToken)):
    """
    API: To reset password of user
    """

    message = resetPassword(user=authorized_user, request_data=request_data.model_dump())

    return message
