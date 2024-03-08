from fastapi import HTTPException, status
from sqlalchemy import or_
from src.config import Config
from src.remote.db.database import db
from src.remote.db.user.model import User
from src.utils.generate_verify_pwd import verify_hash_password
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.route.user.schema import TokenData


def authenticate_user(username_or_email: str, password: str):
    user = get_user(username_or_email)

    if not verify_hash_password(password, user.password):
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


def get_user(username_or_email: str):
    user = (
        db.query(User)
        .filter(
            or_(
                User.email == username_or_email,
                User.username == username_or_email,
            )
        )
        .first()
    )
    if user is None:
        raise Exception("User Not Found")

    return user


def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
        )
        username: str = payload.get("data")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        user = get_user(username_or_email=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )
