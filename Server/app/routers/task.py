from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.common import APIResponse
from app.core.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.dependencies import get_current_user, RoleChecker
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from typing import List

router = APIRouter(prefix="/api/task", tags=["tasks"])
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        due_date=task.due_date,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=APIResponse[List[TaskResponse]])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = db.query(Task).all()
    return APIResponse[List[TaskResponse]](data=tasks)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for var, value in vars(task_update).items():
        if value is not None:
            setattr(task, var, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", response_model=APIResponse[None])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return APIResponse[None](data=None)