from sqlalchemy import or_
from remote.db.database import db
from remote.db.user.model import User
from route.user.schema import RegisterUserSchema


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
        user = RegisterUserSchema(
            first_name=request_data.get("first_name"),
            last_name=request_data.get("last_name"),
            email=request_data.get("email"),
            username=request_data.get("username"),
            password=request_data.get("password"),
        )
        db.add(user)
        db.commit()
    except:
        pass
