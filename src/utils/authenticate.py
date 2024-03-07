
from src.config import Config
from src.remote.db.database import db
from src.utils.generate_verify_pwd import verify_hash_password
from src.controller.user.user import getUser
from datetime import datetime, timedelta, timezone
from jose import jwt


def authenticate_user(request_data: str, password: str):
    user = getUser(request_data)

    if not verify_hash_password(password, user.hashed_password):
        raise Exception("Username or Password is incorrect")
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)

    return encoded_jwt


