from sqlalchemy import Boolean, Column, Integer, String, DateTime, event
from src.remote.db.database import Base
from datetime import datetime

from src.utils.generate_verify_pwd import generate_hash_password


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(15), nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def hash_password(self):
        self.password = generate_hash_password(self.password)


# Event listener to hash password before insertion
@event.listens_for(User, "before_insert")
def hash_user_password(mapper, connection, target):
    target.hash_password()


# Event listener to hash password before update
@event.listens_for(User, "before_update")
def hash_user_password(mapper, connection, target):
    target.hash_password()
