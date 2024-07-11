from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from schema.user_task import CreateTaskRequest, PageResponse, CompleteTaskRequest, BaseResponse, BaseQueryRequest
from service.user_task_service import get_task_service, TaskService
from database.redis_base import get_client

router = APIRouter()


@router.get("/in_process/{user_id}")
async def in_process_tasks(user_id: int, task_service: TaskService = Depends(get_task_service)) -> BaseResponse:
    return await task_service.completed_or_in_process(user_id, True)


@router.get("/completed_or_overdue/{user_id}")
async def completed_or_overdue_tasks(user_id: int,
                                     task_service: TaskService = Depends(get_task_service)) -> BaseResponse:
    return await task_service.completed_or_in_process(user_id, False)


@router.post("/create_task")
async def create_task(req: CreateTaskRequest, task_service: TaskService = Depends(get_task_service),
                      redis_client: Redis = Depends(get_client)) -> PageResponse:
    return await task_service.create_task(req, redis_client)


@router.put("/task_done/{task_id}")
async def complete_task(task_id: int, req: CompleteTaskRequest,
                        task_service: TaskService = Depends(get_task_service)) -> BaseResponse:
    return await task_service.update_task(task_id, req)


@router.put("/task_update")
async def update_task(task_id: int, user_id: int, req: BaseQueryRequest,
                      task_service: TaskService = Depends(get_task_service),
                      redis_client: Redis = Depends(get_client)) -> BaseResponse:
    return await task_service.update_task(task_id, user_id, req, redis_client)


@router.delete("/delete_task")
async def delete_task(task_id: int, user_id: int, task_service: TaskService = Depends(get_task_service),
                      redis_client=Depends(get_client)):
    return await task_service.delete_task(task_id, user_id, redis_client)


@router.get("/warning/{user_id}")
async def warning_message(user_id: int, task_service: TaskService = Depends(get_task_service),
                          redis_client=Depends(get_client)) -> BaseResponse:
    return await task_service.overdue_warning(user_id, redis_client)
