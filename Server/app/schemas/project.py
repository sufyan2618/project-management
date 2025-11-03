from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

from app.schemas.task import TaskResponse

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    created_by: int

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str] = None
    created_by: int
    created_at: datetime
    updated_at: datetime


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    projects: list[ProjectResponse]
    total: int
    tasks: list[TaskResponse]

