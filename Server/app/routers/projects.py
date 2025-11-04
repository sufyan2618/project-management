from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.common import APIResponse
from app.core.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.dependencies import get_current_user, RoleChecker
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectListResponse, ProjectDetailResponse, ProjectWithTaskCount
from app.core.logger import get_logger
from typing import List, Optional
import math

router = APIRouter(prefix="/api/project", tags=["projects"])
logger = get_logger(__name__)


@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    current_user=Depends(get_current_user),
    admin_check=Depends(RoleChecker(["admin"])),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.id} is creating project: {project.title}")
    
    new_project = Project(
        title=project.title,
        description=project.description,
        created_by=current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    logger.info(f"Project created successfully with ID: {new_project.id}")
    return new_project


@router.get("/", response_model=APIResponse[ProjectListResponse], response_model_exclude_none=True)
def list_projects(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    created_by: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} fetching projects - page: {page}, size: {size}, search: {search}, created_by: {created_by}")
    
    query = db.query(
        Project,
        func.count(Task.id).label('task_count')
    ).outerjoin(Task, Project.id == Task.project_id)
    
    if search:
        query = query.filter(
            (Project.title.ilike(f"%{search}%")) | 
            (Project.description.ilike(f"%{search}%"))
        )
    
    if created_by:
        query = query.filter(Project.created_by == created_by)
    
    query = query.group_by(Project.id)
    
    total = query.count()
    total_pages = math.ceil(total / size)
    
    projects_with_count = query.offset((page - 1) * size).limit(size).all()
    
    projects_list = []
    for project, task_count in projects_with_count:
        project_dict = {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "created_by": project.created_by,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "task_count": task_count
        }
        projects_list.append(ProjectWithTaskCount(**project_dict))
    
    logger.info(f"Retrieved {len(projects_list)} projects out of {total} total")
    
    return APIResponse[ProjectListResponse](
        success=True,
        data=ProjectListResponse(
            projects=projects_list,
            total=total,
            page=page,
            size=size,
            total_pages=total_pages
        )
    )


#get project by id with its tasks
@router.get("/{project_id}", response_model=APIResponse[ProjectDetailResponse], response_model_exclude_none=True)
def get_project(
    project_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.id} fetching project with ID: {project_id}")
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        logger.warning(f"Project with ID {project_id} not found")
        raise HTTPException(status_code=404, detail="Project not found")
    
    tasks = db.query(Task).filter(Task.project_id == project_id).all()
    
    project_detail = ProjectDetailResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        created_by=project.created_by,
        created_at=project.created_at,
        updated_at=project.updated_at,
        tasks=tasks
    )
    
    logger.info(f"Project {project_id} retrieved with {len(tasks)} tasks")
    
    return APIResponse[ProjectDetailResponse](success=True, data=project_detail)


@router.patch("/{project_id}", response_model=ProjectResponse, dependencies=[Depends(RoleChecker(["admin"]))])
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"User {current_user.id} attempting to update project {project_id}")
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        logger.warning(f"Project with ID {project_id} not found for update")
        raise HTTPException(status_code=404, detail="Project not found")

    for var, value in vars(project_update).items():
        if value is not None:
            setattr(project, var, value)

    db.commit()
    db.refresh(project)
    
    logger.info(f"Project {project_id} updated successfully")
    return project

@router.delete("/{project_id}", response_model=APIResponse[None], dependencies=[Depends(RoleChecker(["admin"]))])
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    logger.info(f"User {current_user.id} attempting to delete project {project_id}")
    
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        logger.warning(f"Project with ID {project_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    
    logger.info(f"Project {project_id} deleted successfully")
    return APIResponse[None](success=True, data=None, message="Project deleted successfully")