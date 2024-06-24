from fastapi import Depends

from schema.user_task import BaseTaskResponse
from repository.user_task_repository import TaskRepository, get_repository

class TaskService:
    def __init__(self, repo: TaskRepository):
        """
        Initialize the task service
        :param user_id: int
        """
        self.repo = repo

    def get_tasks(self, user_id: int):
        """
        Get all tasks
        :param user_id:
        :return:
        """
        # try:
        tasks = self.repo.get_task_by_id(user_id)
        return BaseTaskResponse(code=200, message="Success", data={"tasks": tasks})
        # except Exception:
        #     print(Exception.__dict__)
        #     return  BaseTaskResponse(code=500, message="Internal Server Error", data={})


def get_task_service(repo: TaskRepository = Depends(get_repository)):
    """
    Get the task service
    :param repo:
    :return:
    """
    return TaskService(repo)