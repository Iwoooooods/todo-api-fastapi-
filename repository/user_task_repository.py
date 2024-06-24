from fastapi import Depends
from sqlalchemy.orm import Session

from database.base import get_db
from model.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        """
        Initialize the task repository
        :param db:
        """
        self.db = db

    def get_task_by_id(self, user_id: int) -> Task:
        """
        Get all tasks
        :param user_id:
        :return:
        """
        return self.db.query(Task).where(Task.user_id == user_id).all()

def get_repository(db: Session = Depends(get_db)):
    """
    Get the task repository
    :param db:
    :return:
    """
    return TaskRepository(db)
