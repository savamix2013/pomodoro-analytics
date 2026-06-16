from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from typing import Annotated
from database import get_db_session
from models import Tasks
from dependecy import get_task_service
from service import TaskService
from schema.task import Task, TaskSchema

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    path="/all",
    response_model=List[TaskSchema],
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return task_service.get_tasks()

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    session = get_db_session()

    session.execute(
        "INSERT INTO Tasks (name, pomodoro_count, category_id) VALUES (:name, :pomodoro_count, :category_id)",
        {
            "name": task.name,
            "pomodoro_count": task.pomodoro_count,
            "category_id": task.category_id
        }
    )

    session.commit()
    session.close()

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    session = get_db_session()
    cursor = session.cursor()

    cursor.execute(
        "UPDATE Tasks SET name = ?, pomodoro_count = ?, category_id = ? WHERE id = ?",
        (task.name, task.pomodoro_count, task.category_id, task_id)
    )

    if cursor.rowcount == 0:
        session.close()
        raise HTTPException(status_code=404, detail="Task not found")

    session.commit()
    updated = cursor.execute(
        "SELECT id, name, pomodoro_count, category_id FROM Tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    session.close()

    return Task(
        id=updated[0],
        name=updated[1],
        pomodoro_count=updated[2],
        category_id=updated[3]
    )


@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int, name: str):
    session = get_db_session()
    cursor = session.cursor()

    # UPDATE
    cursor.execute(
        "UPDATE Tasks SET name = ? WHERE id = ?",
        (name, task_id)
    )

    session.commit()

    # SELECT updated task
    task = cursor.execute(
        "SELECT * FROM Tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    session.close()

    return Task(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        category_id=task[3]
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    session = get_db_session()
    cursor = session.cursor()

    cursor.execute(
        "DELETE FROM Tasks WHERE id = ?",
        (task_id,)
    )

    session.commit()
    session.close()