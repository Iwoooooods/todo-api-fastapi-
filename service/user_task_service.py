from typing import Union

from fastapi import Depends
from loguru import logger
from datetime import datetime, date

from schema.user_task import PageResponse, CreateTaskRequest, CompleteTaskRequest, BaseResponse, BaseQueryRequest
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

    async def completed_or_in_process(self, user_id: int, in_processed: bool) -> BaseResponse:
        try:
            tasks = await self.repo.get_in_process_task(user_id, in_processed)
            tasks = [task.to_dict() for task in tasks]
            return BaseResponse(code=200, message="Success", data={"tasks": tasks})
        except Exception as e:
            return BaseResponse(code=500, message="Fail to Get(qwq)", data={"detail": str(e)})

    async def create_task(self, req: CreateTaskRequest) -> PageResponse:
        """

        :param user_id:
        :return:
        """
        task: Task = Task(**req.dict())
        # Check if the deadline is later than now 
        if task.deadline:
            deadline: date = datetime(task.deadline.year, task.deadline.month, task.deadline.day, 
                                        0, 0, 0)
            if deadline < datetime.now():
                return PageResponse(code=400, message="Deadline should be later than now!", data={})
        try:
            await self.repo.add_task(task)
            logger.success(task)
            return PageResponse(code=200, message="Success", data={})
        except Exception as e:
            return PageResponse(code=500, message="Fail to Create(qwq)", data={"detail": str(e)})



    async def update_task(self, task_id: int, req: Union[CompleteTaskRequest,BaseQueryRequest]) -> BaseResponse:
        try:
            await self.repo.update_task(task_id, req.dict())
            if isinstance(req, CompleteTaskRequest):
                return BaseResponse(code=200, message="Task Completed! Congratulation!!", data={})
            else:
                return BaseResponse(code=200, message="Task Update!", data={})
        except Exception as e:
            return BaseResponse(code=500, message="Fail to Update(qwq)", data={"detail": str(e)})

    async def delete_task(self, task_id: int) -> BaseResponse:
        # await self.repo.delete_task(task_id)
        # return BaseResponse(code=200, message="Task Deleted! Keep Going!", data={})
        try:
            await self.repo.delete_task(task_id)
            return BaseResponse(code=200, message="Task Deleted! Keep Going!", data={})
        except Exception as e:
            return BaseResponse(code=500, message="Fail to Delete(qwq)", data={"detail": str(e)})



async def get_task_service(repo: TaskRepository = Depends(get_repository)):
    """
    Get the task service
    :param repo:
    :return:
    """
    return TaskService(repo)