from fastapi import FastAPI
from sqlalchemy import select
from database import Base, get_db_session
from database.accessor import engine
from models import Tasks
from handlers import routers

app = FastAPI()


@app.on_event("startup")
async def ensure_sample_tasks():
    Base.metadata.create_all(bind=engine)
    session = get_db_session()
    try:
        existing_tasks = session.execute(select(Tasks)).scalars().all()
        if len(existing_tasks) < 2:
            additions = []
            if len(existing_tasks) == 0:
                additions = [
                    Tasks(name="Task 1", pomodoro_count=1, category_id=1),
                    Tasks(name="Task 2", pomodoro_count=2, category_id=1),
                    Tasks(name="Task 3", pomodoro_count=3, category_id=1),
                ]
            elif len(existing_tasks) == 1:
                additions = [
                    Tasks(name="Task 2", pomodoro_count=2, category_id=1),
                ]
            session.add_all(additions)
            session.commit()
    finally:
        session.close()


for router in routers:
    app.include_router(router)