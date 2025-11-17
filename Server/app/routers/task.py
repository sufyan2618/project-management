from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas.common import APIResponse
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.dependencies import get_current_user, RoleChecker
from app.services.email_service import EmailService
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskListResponse
from app.core.logger import get_logger
from typing import List, Optional
import math
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape



TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "email"

# Setup Jinja2 environment
env = Environment(
    loader=FileSystemLoader(searchpath=str(TEMPLATES_DIR)),
    autoescape=select_autoescape(['html', 'xml'])
)


router = APIRouter(prefix="/api/task", tags=["tasks"])
logger = get_logger(__name__)
@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} creating task: {task.title} for project {task.project_id}")
    
    new_task = Task(
        title=task.title,
        description=task.description,
        project_id=task.project_id,
        assigned_to=task.assigned_to,
        due_date=task.due_date,
    )
    user = db.query(User).filter(User.id == task.assigned_to).first()
    if not user:
        logger.warning(f"User with ID {task.assigned_to} not found for task assignment")
        raise HTTPException(status_code=404, detail="Assigned user not found")

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info(f"Task {new_task.id} created and assigned to user {user.id}")

    # Send task assignment email
    template = env.get_template('task-assigned.html')
    html = template.render(
        user_name=user.first_name,
        task_name=new_task.title
    )
    task = EmailService.send_email.delay(
        to_email=user.email,
        subject="New Task Assigned",
        html_content=html
    )
    return new_task


@router.get("/assigned", response_model=APIResponse[TaskListResponse], response_model_exclude_none=True)
def get_assigned_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} fetching their assigned tasks - page: {page}, size: {size}, status: {status}")
    
    query = db.query(Task).filter(Task.assigned_to == current_user.id)
    
    if status:
        query = query.filter(Task.status == status)
    
    total = query.count()
    total_pages = math.ceil(total / size)
    
    tasks = query.offset((page - 1) * size).limit(size).all()
    
    logger.info(f"Retrieved {len(tasks)} assigned tasks out of {total} total for user {current_user.id}")
    
    return APIResponse[TaskListResponse](
        success=True,
        data=TaskListResponse(
            tasks=tasks,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )
    )





@router.get("/", response_model=APIResponse[TaskListResponse], response_model_exclude_none=True)
def list_tasks(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    project_id: Optional[int] = Query(None),
    assigned_to: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} fetching tasks - page: {page}, size: {size}, search: {search}, status: {status}, project_id: {project_id}, assigned_to: {assigned_to}")
    
    query = db.query(Task)
    
    if search:
        query = query.filter(
            (Task.title.ilike(f"%{search}%")) |
            (Task.description.ilike(f"%{search}%"))
        )
    
    if status:
        query = query.filter(Task.status == status)
    
    if project_id:
        query = query.filter(Task.project_id == project_id)
    
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    
    total = query.count()
    total_pages = math.ceil(total / size)
    
    tasks = query.offset((page - 1) * size).limit(size).all()
    
    logger.info(f"Retrieved {len(tasks)} tasks out of {total} total")
    
    return APIResponse[TaskListResponse](
        success=True,
        data=TaskListResponse(
            tasks=tasks,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )
    )





@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} fetching task with ID: {task_id}")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    if(task.assigned_to != current_user.id and current_user.role != "admin"):
        logger.warning(f"User {current_user.id} unauthorized to access task {task_id}")
        raise HTTPException(status_code=403, detail="Not authorized to access this task")

    logger.info(f"Task {task_id} retrieved successfully")
    return task





@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} attempting to update task {task_id}")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning(f"Task with ID {task_id} not found for update")
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task.status
    
    for var, value in vars(task_update).items():
        if value is not None:
            setattr(task, var, value)

    db.commit()
    db.refresh(task)

    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    if task_update.status and task_update.status != old_status:
        logger.info(f"Task {task_id} status changed from {old_status} to {task_update.status}")
        project = db.query(Project).filter(Project.id == task.project_id).first()
        if project:
            user = db.query(User).filter(User.id == project.created_by).first()
            if user:
                template = env.get_template('task-status-update.html')
                html = template.render(
                    user_name=user.first_name,
                    task_name=task.title,
                    previous_status=old_status,
                    new_status=task_update.status,
                    task_id=task.id,
                    timestamp=timestamp
                )
                email_task = EmailService.send_email.delay(
                    to_email=user.email,
                    subject="Task Status Updated",
                    html_content=html
                )
                logger.info(f"Email notification queued for project creator {user.email}")
            else:
                logger.warning(f"Project creator user not found for project {project.id}")
        else:
            logger.warning(f"Project not found for task {task_id}")

    logger.info(f"Task {task_id} updated successfully")
    return task



@router.delete("/{task_id}", response_model=APIResponse[None], response_model_exclude_none=True)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} attempting to delete task {task_id}")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.warning(f"Task with ID {task_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Task not found")

    if(task.assigned_to != current_user.id and current_user.role != "admin"):
        logger.warning(f"User {current_user.id} unauthorized to delete task {task_id}")
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    db.delete(task)
    db.commit()
    
    logger.info(f"Task {task_id} deleted successfully")
    return APIResponse[None](success=True, data=None, message="Task deleted successfully")