from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.schemas.common import APIResponse
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.dependencies import get_current_user, RoleChecker
from app.services.email_service import EmailService
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from typing import List

router = APIRouter(prefix="/api/task", tags=["tasks"])
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
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
    user = db.query(User).filter(User.id == task.assigned_to).first()
    if not user:
        raise HTTPException(status_code=404, detail="Assigned user not found")

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Send email notification using background task
    background_tasks.add_task(
        EmailService.send_task_assigned_email,
        email=user.email,
        user_name=user.full_name,
        task_name=task.title
    )
    return new_task


#get all tasks
@router.get("/", response_model=APIResponse[List[TaskResponse]])
def list_tasks(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    tasks = db.query(Task).all()
    return APIResponse[List[TaskResponse]](data=tasks)



#get task by id
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if(task.assigned_to != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    return task



#update task
@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # if status is being updated, send email notification to project creator
    if task_update.status and task_update.status != task.status:
        user = db.query(User).filter(User.id == task.assigned_to).first()
        background_tasks.add_task(
            EmailService.send_task_status_update_email,
            email=user.email,
            user_name=user.full_name,
            task_name=task.title,
            status=task_update.status
        )

    for var, value in vars(task_update).items():
        if value is not None:
            setattr(task, var, value)

    db.commit()
    db.refresh(task)
    return task



# delete task by id
@router.delete("/{task_id}", response_model=APIResponse[None])
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if(task.assigned_to != current_user.id and current_user.role != "admin"):
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    return APIResponse[None](data=None)