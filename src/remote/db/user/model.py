from sqlalchemy import Boolean, Column, Integer, String, DateTime
from src.remote.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utc)