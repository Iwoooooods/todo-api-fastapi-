from typing import Dict, List, Any

from fastapi import Depends, HTTPException
from loguru import logger
from sqlalchemy import text, select
from sqlalchemy.exc import SQLAlchemyError
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
            if not tasks:
                raise HTTPException(status_code=404, detail="Task not found")
            return tasks
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def get_task_by_id(self, id: int) -> Any:
        try:
            result = await self.db.execute(select(Task).filter(Task.id == id))
            task = result.scalars().first()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            return task
        except SQLAlchemyError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def add_task(self, task: Task) -> None:
        try:
            self.db.add(task)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update_task(self, task_id: int, update_fields: Dict[str, any]) -> None:
        result = await self.db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        for key, value in update_fields.items():
            if hasattr(task, key) and value:
                setattr(task, key, value)
        try:
            await self.db.commit()
            logger.success("Update Successfully!")
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(str(e))
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_task(self, task_id: int) -> None:
        try:
            result = await self.db.execute(select(Task).where(Task.id == task_id))
            task = result.scalars().first()
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            await self.db.delete(task)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))


async def get_repository(db: AsyncSession = Depends(get_db)):
    """
    Get the task repository
    :param db:
    :return:
    """
    return TaskRepository(db)
