from fastapi import HTTPException, status
from sqlalchemy import or_
from src.config import Config
from src.remote.db.database import db
from src.remote.db.user.model import User
from src.route.user.schema import Token, TokenData
from src.utils.authenticate import authenticate_user, create_access_token
from jose import JWTError, jwt
from src.utils.authenticate import getUser


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
        user = getUser(username=token_data.username)
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
