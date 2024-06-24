from typing import Dict, List, Any

from fastapi import Depends
from loguru import logger
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import get_db
from model.task import Task


class TaskRepository:
    def __init__(self, db: AsyncSession):
        """
        Initialize the task repository
        :param db:
        """
        self.db = db

    async def get_task_by_user(self, user_id: int) -> Any:
        """
        Get all tasks
        :param user_id:
        :return:
        """
        try:
            results = await self.db.execute(select(Task).filter(Task.user_id == user_id))
            tasks = results.scalars().all()
            return tasks
        except Exception:
            raise Exception

    async def get_task_by_id(self, id: int) -> Any:
        try:
            result = await self.db.execute(select(Task).filter(Task.id == id))
            task = result.scalars().first()
            return task
        except Exception:
            raise Exception

    async def add_task(self, task: Task) -> None:
        try:
            self.db.add(task)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise Exception

    async def update_task(self, task_id: int, update_fields: Dict[str, any]) -> None:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalars().first()
        for key, value in update_fields.items():
            if hasattr(task, key) and value:
                setattr(task, key, value)
        try:
            await self.db.commit()
            logger.success("Update Successfully!")
        except Exception:
            await self.db.rollback()
            raise Exception


async def get_repository(db: AsyncSession = Depends(get_db)):
    """
    Get the task repository
    :param db:
    :return:
    """
    return TaskRepository(db)
