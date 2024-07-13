from typing import Union, List

from fastapi import Depends, Response, status
from fastapi.responses import JSONResponse
from loguru import logger
from datetime import datetime, date, timedelta
from redis.asyncio import Redis

from schema.user_task import PageResponse, CreateTaskRequest, CompleteTaskRequest, BaseQueryRequest, UserTask
from schema.base import BaseResponse
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

    async def completed_or_in_process(self, user_id: int, in_processed: bool) -> Response | List[UserTask]:
        try:
            tasks = await self.repo.get_in_process_task(user_id, in_processed)
            tasks = [task.to_dict() for task in tasks]
            return [UserTask(**task) for task in tasks]
        except Exception as e:
            logger.error(e)
            return JSONResponse({"msg": "Fail to Complete"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def create_task(self, req: CreateTaskRequest, redis_client: Redis) -> Response | dict:
        """

        :param redis_client:
        :param req:
        :return:
        """
        task: Task = Task(**req.model_dump())
        # Check if the deadline is later than now 
        if task.deadline and task.deadline < datetime.now():
            return JSONResponse(content={"msg": "Deadline should be later than now!"},
                                status_code=status.HTTP_400_BAD_REQUEST)
        try:
            task = await self.repo.add_task(task)
        except Exception as e:
            logger.error(str(e))
            return JSONResponse(content={"msg": "Fail to Create"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if task.deadline:
            deadline_timestamp = int(task.deadline.timestamp())
            name = f"user:{task.user_id}:time_remain"
            await redis_client.zadd(name, {str(task.id): deadline_timestamp})
            # await redis_client.expire(name, deadline_timestamp - int(datetime.now().timestamp()))
        return {"task_id": task.id}

    async def update_task(self, task_id: int, user_id: int, req: CompleteTaskRequest | BaseQueryRequest,
                          redis_client: Redis) -> Response:
        try:
            await self.repo.update_task(task_id, req.dict())
            if req.deadline:
                deadline_timestamp = int(req.deadline.timestamp())
                await redis_client.zadd(f"user:{user_id}:time_remain", {str(task_id): deadline_timestamp})
            if req.is_completed:
                return JSONResponse(content={"msg": "Task Completed! Congratulation!!"}, status_code=status.HTTP_200_OK)
            else:
                return JSONResponse(content={"msg": "Task Updated"}, status_code=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex)
            return JSONResponse(content={"msg": "Fail to Update"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def delete_task(self, task_id: int, user_id: int, redis_client: Redis) -> Response:
        # await self.repo.delete_task(task_id)
        # return BaseResponse(code=200, message="Task Deleted! Keep Going!", data={})
        try:
            await self.repo.delete_task(task_id)
            await redis_client.zrem(f"user:{user_id}:time_remain", str(task_id))
            return JSONResponse(content={"msg": "Task Deleted"}, status_code=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex))
            return JSONResponse(content={"msg": "Internal Server Error"},
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    async def overdue_warning(user_id: int, redis_client: Redis) -> Response | dict:
        now = datetime.now()
        in_24_hours = datetime.now() + timedelta(days=1)
        try:
            warning_tasks = await redis_client.zrangebyscore(f"user:{user_id}:time_remain", now.timestamp(),
                                                             in_24_hours.timestamp())
        except Exception as ex:
            logger.error(ex)
            return JSONResponse(content="Internal Server Error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return {"warning_task_num": len(warning_tasks)}


async def get_task_service(repo: TaskRepository = Depends(get_repository)) -> TaskService:
    """
    Get the task service
    :param repo:
    :return:
    """
    return TaskService(repo)
