from fastapi import HTTPException
from sqlalchemy import or_
from src.config import Config
from src.remote.db.database import db
from src.remote.db.user.model import User
from src.route.user.schema import Token
from src.utils.authenticate import authenticate_user, create_access_token, getCurrentUser

from src.utils.authenticate import getUser
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


def changePassword(token : str , request_data : dict) :
    try :
        user = getCurrentUser(token = token)

        if verify_hash_password(request_data['old_password'] , user.get('passsword')  ) != True :
            raise Exception(status_code=400,detail='Old password does not match!')
        
        if request_data['new_password'] != request_data['confirm_password'] :
            raise Exception(status_code=400,detail='New Password and Confirm Password does not match!')
        
        user.password = request_data['new_password'] 
        db.commit()        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "message": f"Error occurred while processing the request: {str(e)}",
                "status": "error",
                "status_code": 400,
            },
        )