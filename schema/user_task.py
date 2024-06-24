from pydantic import BaseModel

class BaseQueryRequest(BaseModel):
    user_id: int

class BaseTaskResponse(BaseModel):
    code: int
    message: str
    data: dict