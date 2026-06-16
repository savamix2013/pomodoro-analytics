from typing import List
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from database import get_db_session
from models import Tasks, Categories


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        with self.db_session as session:
            task: list[Tasks] = (
                session.execute(select(Tasks)).scalars().all()
            )
            return task

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session as session:
            task: Tasks | None = (
                session.execute(
                    select(Tasks).where(Tasks.id == task_id)
                ).scalar_one_or_none()
            )
            return task

    def create_task(self, task: Tasks) -> None:
        with self.db_session as session:
            session.add(task)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            session.execute(query)
            session.commit()

    def get_tasks_by_category_name(self, category_name: str) -> List[Tasks]:
        query = (
            select(Tasks)
            .join(Categories, Tasks.category_id == Categories.id)
            .where(Categories.name == category_name)
        )

        with self.db_session as session:
            tasks: List[Tasks] = (
                session.execute(query).scalars().all()
            )
            return tasks