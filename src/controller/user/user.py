from datetime import datetime
from fastapi import HTTPException, Request
from sqlalchemy import or_
from src.remote.db.database import db
from src.remote.db.user.model import User
from src.route.user.schema import Token
from src.utils.authenticate import (
    authenticate_user,
    create_access_token,
    get_current_user,
)
from src.utils.authenticate import get_user
from src.utils.generate_verify_pwd import verify_hash_password


def registerUser(request_data):
    try:
        user = (
            db.query(User)
            .filter(
                or_(
                    User.email == request_data.get("email"),
                    User.username == request_data.get("username"),
                )
            )
            .first()
        )
        if user:
            if not user.is_verified:
                db.delete(user)
                db.commit()
            else:
                raise Exception("Email or Username has been taken")
        user = User(
            first_name=request_data.get("first_name"),
            last_name=request_data.get("last_name"),
            email=request_data.get("email"),
            username=request_data.get("username"),
            password=request_data.get("password"),
        )
        db.add(user)
        db.commit()

        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )


def loginUser(request_data: dict):
    try:
        user = authenticate_user(
            username_or_email=request_data.get("username_or_email"),
            password=request_data.get("password"),
        )
        access_token = create_access_token(data={"data": user.username})
        return Token(access_token=access_token, token_type="bearer")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )


def resetPassword(user: User, request_data: dict):
    try:
        # breakpoint()
        if (
            verify_hash_password(request_data.get("old_password"), user.password)
            != True
        ):
            raise Exception("Wrong password")

        if request_data.get("new_password") != request_data.get("confirm_password"):
            raise Exception("New Password and Confirm Password does not match!")

        user.password = request_data.get("new_password")
        user.updated_at = datetime.utcnow()
        db.commit()
        return {"message": "Password has been reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )


def verifyToken(req: Request):
    user = get_current_user(req.headers.get("Authorization"))
    return user
