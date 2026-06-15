from fastapi import APIRouter, status, HTTPException
from typing import List

from database.database import get_db_connection
from schema.task import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=List[Task])

async def get_tasks() -> List[Task]:
    result: List[Task] = []

    cursor = get_db_connection().cursor()
    tasks = cursor.execute("SELECT * FROM Tasks").fetchall()

    for task in tasks:
        result.append(
            Task(
                id=task[0],
                name=task[1],
                pomodoro_count=task[2],
                category_id=task[3],
            )
        )

    return result


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO Tasks (name, pomodoro_count, category_id) VALUES (?, ?, ?)",
        (task.name, task.pomodoro_count, task.category_id)
    )

    connection.commit()
    connection.close()

    return task


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE Tasks SET name = ?, pomodoro_count = ?, category_id = ? WHERE id = ?",
        (task.name, task.pomodoro_count, task.category_id, task_id)
    )

    if cursor.rowcount == 0:
        connection.close()
        raise HTTPException(status_code=404, detail="Task not found")

    connection.commit()
    updated = cursor.execute(
        "SELECT id, name, pomodoro_count, category_id FROM Tasks WHERE id = ?",
        (task_id,)
    ).fetchone()
    connection.close()

    return Task(
        id=updated[0],
        name=updated[1],
        pomodoro_count=updated[2],
        category_id=updated[3]
    )


@router.patch("/{task_id}", response_model=Task)
async def patch_task(task_id: int, name: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    # UPDATE
    cursor.execute(
        "UPDATE Tasks SET name = ? WHERE id = ?",
        (name, task_id)
    )

    connection.commit()

    # SELECT updated task
    task = cursor.execute(
        "SELECT * FROM Tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    connection.close()

    return Task(
        id=task[0],
        name=task[1],
        pomodoro_count=task[2],
        category_id=task[3]
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM Tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()