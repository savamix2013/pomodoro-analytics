import json
from typing import List

from redis import Redis
from schema.task import TaskSchema


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> List[TaskSchema]:
        with self.redis as redis:
            tasks_json = redis.lrange(name="tasks", start=0, end=-1)

        return [
            TaskSchema.model_validate(json.loads(task))
            for task in tasks_json
        ]

    def set_tasks(self, tasks: List[TaskSchema]):
        tasks_json = [task.model_dump_json() for task in tasks]

        with self.redis as redis:
            redis.rpush("tasks", *tasks_json)