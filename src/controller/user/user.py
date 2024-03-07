from fastapi import HTTPException
from sqlalchemy import or_
from src.remote.db.database import db
from src.remote.db.user.model import User


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


def getUser(request_data: str):
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
        if user is None:
            raise Exception("User Not Found")

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
