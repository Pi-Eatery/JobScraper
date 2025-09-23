from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..models.database import get_db
from ..services.application_service import ApplicationService
from ..schemas.job_application import JobApplicationCreate, JobApplicationUpdate, JobApplicationOut

router = APIRouter()
application_service = ApplicationService()

# Placeholder for current user authentication
# In a real app, this would decode a JWT and return the user ID
def get_current_user_id():
    return 1 # For now, assume user with ID 1 is logged in

@router.post("/applications/", response_model=JobApplicationOut, status_code=status.HTTP_201_CREATED)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return application_service.create_application(
        db=db,
        user_id=user_id,
        job_title=application.job_title,
        company=application.company,
        application_date=application.application_date,
        status=application.status,
        job_board=application.job_board,
        url=application.url,
        notes=application.notes,
        keywords=application.keywords
    )

@router.get("/applications/", response_model=List[JobApplicationOut])
def read_applications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    applications = application_service.get_applications(db, user_id=user_id, skip=skip, limit=limit)
    return applications

@router.get("/applications/{application_id}", response_model=JobApplicationOut)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    application = application_service.get_application(db, application_id=application_id, user_id=user_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.put("/applications/{application_id}", response_model=JobApplicationOut)
def update_application(
    application_id: int,
    application_update: JobApplicationUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    updated_application = application_service.update_application(
        db=db,
        application_id=application_id,
        user_id=user_id,
        job_title=application_update.job_title,
        company=application_update.company,
        application_date=application_update.application_date,
        status=application_update.status,
        job_board=application_update.job_board,
        url=application_update.url,
        notes=application_update.notes,
        keywords=application_update.keywords
    )
    if not updated_application:
        raise HTTPException(status_code=404, detail="Application not found or not authorized")
    return updated_application

@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    deleted_application = application_service.delete_application(db, application_id=application_id, user_id=user_id)
    if not deleted_application:
        raise HTTPException(status_code=404, detail="Application not found or not authorized")
    return