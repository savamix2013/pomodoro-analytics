from sqlalchemy import create_engine
from sqlalchemy.orm import Session as DBSession, sessionmaker

from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url)

SessionLocal = sessionmaker(engine, class_=DBSession)


def get_db_session() -> DBSession:
    return SessionLocal()
