from fastapi import HTTPException
from jose import jwt
from sqlalchemy import or_
from src.config import Config
from src.remote.db.database import db
from src.remote.db.user.model import User
from src.utils.generate_verify_pwd import verify_hash_password
from src.controller.user.user import getUser
from datetime import datetime, timedelta, timezone


def authenticate_user(username_or_email: str, password: str):
    user = getUser(username_or_email)

    if not verify_hash_password(password, user.hashed_password):
        raise Exception("Username or Password is incorrect")
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=int(Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM
    )
    return encoded_jwt


def getUser(request_data: str):
    user = (
        db.query(User)
        .filter(
            or_(
                User.email == request_data.get("username_or_email"),
                User.username == request_data.get("username_or_email"),
            )
        )
        .first()
    )
    if user is None:
        raise Exception("User Not Found")

    return user
