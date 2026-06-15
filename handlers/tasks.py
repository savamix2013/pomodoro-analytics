from fastapi import APIRouter, status, HTTPException
from typing import List

from fixtures import tasks as fixtures_tasks
from schema.task import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all", response_model=List[Task])
async def get_tasks():
    return fixtures_tasks


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    fixtures_tasks.append(task)
    return task


@router.put("/{task_id}")
async def update_task(task_id: int, task: Task):
    for index, item in enumerate(fixtures_tasks):
        if item["id"] == task_id:
            fixtures_tasks[index] = task
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.patch("/{task_id}")
async def patch_task(task_id: int, name: str):
    for task in fixtures_tasks:
        if task["id"] == task_id:
            task["name"] = name
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(fixtures_tasks):
        if task["id"] == task_id:
            del fixtures_tasks[index]
            return

    raise HTTPException(status_code=404, detail="Task not found")