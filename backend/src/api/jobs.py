from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.src.models.database import get_db
from backend.src.services import job_service
from backend.src.middleware.auth import get_current_user
from backend.src.models.user import User as DBUser

router = APIRouter()

@router.post("/jobs/{job_id}/save", status_code=status.HTTP_200_OK)
async def save_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_job = job_service.update_job_status(db, job_id, current_user.id, "saved")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job saved successfully"}

@router.post("/jobs/{job_id}/apply", status_code=status.HTTP_200_OK)
async def apply_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_job = job_service.update_job_status(db, job_id, current_user.id, "applied")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job marked as applied"}

@router.post("/jobs/{job_id}/hide", status_code=status.HTTP_200_OK)
async def hide_job(
    job_id: int,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_job = job_service.update_job_status(db, job_id, current_user.id, "hidden")
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found or not authorized")
    return {"message": "Job hidden successfully"}
