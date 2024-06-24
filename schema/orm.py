from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    brief: Optional[str] = None
    content: Optional[str] = None
    is_completed: Optional[bool] = False
    deadline: Optional[datetime] = None

class TaskInDBBase(TaskBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True