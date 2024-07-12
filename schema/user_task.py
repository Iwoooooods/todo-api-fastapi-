from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class BaseQueryRequest(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    brief: Optional[str] = None
    content: Optional[str] = None
    deadline: Optional[datetime] = None
    parent_id: Optional[int] = None
    is_completed: bool = False


class CreateTaskRequest(BaseQueryRequest):
    user_id: int
    title: str
    content: str


class CompleteTaskRequest(BaseQueryRequest):
    is_completed: bool = True


class BaseResponse(BaseModel):
    code: int
    message: str
    data: dict


class PageResponse(BaseResponse):
    page: int = 1
    per_page: int = 10
