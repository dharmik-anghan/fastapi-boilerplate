from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from src.remote.db.database import Base
from datetime import datetime


class Otp(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    otp = Column(String, nullable=False)
    email = Column(String, ForeignKey("users.email"), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
