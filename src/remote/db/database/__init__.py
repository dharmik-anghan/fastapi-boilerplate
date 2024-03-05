from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base
from src.config import Config

engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        return db  # Return session directly instead of using yield
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

db = SessionLocal()