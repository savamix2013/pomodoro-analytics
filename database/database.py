from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///pomodoro.sqlite")

SessionLocal = sessionmaker(bind=engine)


def get_db_session() -> Session:
    return SessionLocal()