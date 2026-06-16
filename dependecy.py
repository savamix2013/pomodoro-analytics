from repository import TaskRepository
from database import get_db_session

def get_tasks_repository() -> TaskRepository:
    db_session = get_db_session()
    return TaskRepository(db_session)