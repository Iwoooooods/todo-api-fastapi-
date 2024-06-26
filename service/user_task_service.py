from fastapi import Depends
from loguru import logger

from schema.user_task import PageResponse, CreateTaskRequest, CompleteTaskRequest, BaseResponse
from model.task import Task
from repository.user_task_repository import TaskRepository, get_repository

class TaskService:
    def __init__(self, repo: TaskRepository):
        """
        Initialize the task service
        :param user_id: int
        """
        self.repo = repo

    async def get_tasks(self, user_id: int) -> PageResponse:
        """
        Get all tasks
        :param user_id:
        :return:
        """
        try:
            tasks = await self.repo.get_task_by_user(user_id)
            tasks = [task.to_dict() for task in tasks]
            return PageResponse(code=200, message="Success", data={"tasks": tasks})
        except Exception as e:
            return PageResponse(code=500, message="Fail to Get(qwq)", data={"detail": str(e)})

    async def create_task(self, req: CreateTaskRequest) -> PageResponse:
        """

        :param user_id:
        :return:
        """
        task = Task(**req.dict())
        try:
            await self.repo.add_task(task)
            logger.success(task)
            return PageResponse(code=200, message="Success", data={})
        except Exception as e:
            return PageResponse(code=500, message="Fail to Create(qwq)", data={"detail": str(e)})



    async def complete_task(self, task_id: int, req: CompleteTaskRequest) -> BaseResponse:
        try:
            await self.repo.update_task(task_id, req.dict())
            return BaseResponse(code=200, message="Task Completed! Congratulation!!", data={})
        except Exception as e:
            return BaseResponse(code=500, message="Fail to Update(qwq)", data={"detail": str(e)})

    async def delete_task(self, task_id: int) -> BaseResponse:
        # await self.repo.delete_task(task_id)
        # return BaseResponse(code=200, message="Task Deleted! Keep Going!", data={})
        try:
            await self.repo.delete_task(task_id)
            return BaseResponse(code=200, message="Task Deleted! Keep Going!")
        except Exception as e:
            return BaseResponse(code=500, message="Fail to Delete(qwq)", data={"detail": str(e)})



async def get_task_service(repo: TaskRepository = Depends(get_repository)):
    """
    Get the task service
    :param repo:
    :return:
    """
    return TaskService(repo)