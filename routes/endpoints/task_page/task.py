from fastapi import APIRouter, Depends

from schema.user_task import CreateTaskRequest, PageResponse, CompleteTaskRequest, BaseResponse, BaseQueryRequest
from service.user_task_service import get_task_service, TaskService


router = APIRouter()

@router.get("/home")
async def index(user_id: int, task_service: TaskService = Depends(get_task_service)) -> PageResponse :
    return await task_service.get_tasks(user_id)

@router.post("/create_task")
async def create_task(req: CreateTaskRequest, task_service: TaskService = Depends(get_task_service)) -> PageResponse:
    return await task_service.create_task(req)

@router.put("/task_done/{task_id}")
async def complete_task(task_id: int, req: CompleteTaskRequest, task_service: TaskService = Depends(get_task_service)) -> BaseResponse:
    return await task_service.update_task(task_id, req)

@router.put("/task_update/{task_id}")
async def update_task(task_id: int, req: BaseQueryRequest, task_service: TaskService = Depends(get_task_service)) -> BaseResponse:
    return await task_service.update_task(task_id, req)

@router.delete("/delete_task/{task_id}")
async def delete_task(task_id: int, task_service: TaskService = Depends(get_task_service)):
    return await task_service.delete_task(task_id)