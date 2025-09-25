from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..models.database import get_db
from ..services import job_service
from ..middleware.auth import get_current_user
from ..models.user import User as DBUser
from ..schemas.job import JobOut

router = APIRouter()


@router.get("/jobs/", response_model=List[JobOut])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jobs = job_service.get_jobs(db, int(current_user.id), skip=skip, limit=limit)
    return jobs


@router.post("/jobs/{job_id}/save", status_code=status.HTTP_200_OK)
async def save_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_job = job_service.update_job_status(db, job_id, int(current_user.id), "saved")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job saved successfully"}


@router.post("/jobs/{job_id}/apply", status_code=status.HTTP_200_OK)
async def apply_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_job = job_service.update_job_status(db, job_id, int(current_user.id), "applied")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job marked as applied"}


@router.post("/jobs/{job_id}/hide", status_code=status.HTTP_200_OK)
async def hide_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_job = job_service.update_job_status(db, job_id, int(current_user.id), "hidden")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job hidden successfully"}
