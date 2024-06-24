from fastapi import APIRouter, Depends

from schema.user_task import BaseQueryRequest, BaseTaskResponse
from schema.orm import TaskInDBBase
from service.user_task_service import get_task_service, TaskService


router = APIRouter()

@router.get("/home", response_model=BaseTaskResponse)
async def index(user_id: int, task_service: TaskService = Depends(get_task_service)) -> BaseTaskResponse :
    return task_service.get_tasks(user_id)