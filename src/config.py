import os
from dotenv import load_dotenv

load_dotenv(os.getenv("ENV_FILE", ".env"))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
    HOST = os.environ["HOST"]
    PORT = os.environ["PORT"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"]
    EMAIL_FROM = os.environ["EMAIL_FROM"]
    EMAIL_PASS = os.environ["EMAIL_PASS"]
    OTP_EXPIRE_MINUTES = os.environ["OTP_EXPIRE_MINUTES"]
