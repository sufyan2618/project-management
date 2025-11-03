from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.common import APIResponse
from app.core.database import get_db
from app.models.task import Task
from app.models.project import Project
from app.dependencies import get_current_user, RoleChecker
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectListResponse
from typing import List

router = APIRouter(prefix="/api/project", tags=["projects"])
@router.post("/", response_model=ProjectResponse)
#only admin can create projects
@Depends(RoleChecker(allowed_roles=["admin"]))
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = Project(
        title=project.title,
        description=project.description,
        created_by=project.created_by
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=APIResponse[ProjectListResponse])
def list_projects( db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    # return the tasks associated with the projects
    tasks = db.query(Task).filter(Task.project_id.in_([project.id for project in projects])).all()

    return APIResponse[ProjectListResponse](data=ProjectListResponse(projects=projects, total=len(projects), tasks=tasks))


#get project by id
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    elif project.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to access this project")
    return project


#update project
@router.patch("/{project_id}", response_model=ProjectResponse)
#only admin can update projects
@Depends(RoleChecker(allowed_roles=["admin"]))
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for var, value in vars(project_update).items():
        if value is not None:
            setattr(project, var, value)

    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", response_model=APIResponse[None])
#only admin can delete projects
@Depends(RoleChecker(allowed_roles=["admin"]))
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return APIResponse[None](data=None, message="Project deleted successfully")