from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    created_by: EmailStr

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    created_by: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total: int

    class Config:
        orm_mode = True
