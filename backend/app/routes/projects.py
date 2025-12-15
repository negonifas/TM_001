from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from loguru import logger

from .. import auth
from .. import db
from ..schemas import Project, ProjectCreate, ProjectUpdate

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=List[Project])
async def list_projects(
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
) -> List[Project]:
    projects = await db.fetch_projects(current_user["id"])
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(current_user["id"]),
        nick=current_user.get("nickname", "-"),
    ).info("event=projects_listed count={count}", count=len(projects))
    return [Project(**project) for project in projects]


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
) -> Project:
    project = await db.fetch_project(project_id, current_user["id"])
    if not project:
        raise HTTPException(status_code=404, detail="Not found")
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(current_user["id"]),
        nick=current_user.get("nickname", "-"),
    ).info("event=project_read id={id}", id=project_id)
    return Project(**project)


@router.post(
    "/",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth.csrf_protect)],
)
async def create_project(
    payload: ProjectCreate,
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
) -> Project:
    project = await db.create_project(payload.model_dump(), current_user["id"])
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(current_user["id"]),
        nick=current_user.get("nickname", "-"),
    ).info("event=project_created id={id}", id=project["id"])
    return Project(**project)


@router.put(
    "/{project_id}",
    response_model=Project,
    dependencies=[Depends(auth.csrf_protect)],
)
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
) -> Project:
    updated = await db.update_project(project_id, payload.model_dump(exclude_unset=True), current_user["id"])
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(current_user["id"]),
        nick=current_user.get("nickname", "-"),
    ).info("event=project_updated id={id}", id=project_id)
    return Project(**updated)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth.csrf_protect)],
)
async def delete_project(
    project_id: int,
    request: Request,
    current_user: dict = Depends(auth.get_current_user),
) -> None:
    deleted = await db.delete_project(project_id, current_user["id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Not found")
    logger.bind(
        req=getattr(request.state, "req_id", "-"),
        user=str(current_user["id"]),
        nick=current_user.get("nickname", "-"),
    ).info("event=project_deleted id={id}", id=project_id)
