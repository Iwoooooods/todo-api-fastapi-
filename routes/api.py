from fastapi import APIRouter

from .endpoints.task_page import task

router = APIRouter()

router.include_router(task.router, prefix="/tasks", tags=["tasks"])