from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: int
    project_id: int
    due_date: Optional[str] = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str] = None
    assigned_to: int
    project_id: int
    status: str
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    project_id: Optional[int] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    page: int
    size: int
    total_pages: int


    
