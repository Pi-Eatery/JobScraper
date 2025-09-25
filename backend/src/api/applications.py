from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..models.database import get_db
from ..models.keyword import Keyword
from ..models.user import User
from ..services.application_service import ApplicationService
from ..services.keyword_service import KeywordService
from ..schemas.job_application import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationOut,
)
from ..middleware.auth import get_current_user

router = APIRouter()
application_service = ApplicationService()
keyword_service = KeywordService()


@router.post(
    "/applications/",
    response_model=JobApplicationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_application = application_service.create_application(
        db=db,
        user_id=int(current_user.id),
        job_title=application.job_title,
        company=application.company,
        application_date=application.application_date,
        status=application.status,
        job_board=application.job_board,
        url=application.url,
        notes=application.notes,
    )

    for term in application.keywords:
        keyword = keyword_service.get_keyword_by_term(db, term=term)
        if not keyword:
            keyword = keyword_service.create_keyword(
                db, term=term, user_id=int(current_user.id)
            )
        db_application.keywords.append(keyword)
    db.commit()
    db.refresh(db_application)
    return db_application


@router.get("/applications/", response_model=List[JobApplicationOut])
def read_applications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    company: Optional[str] = None,
    job_board: Optional[str] = None,
    keyword_terms: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    applications = application_service.get_applications(
        db,
        user_id=int(current_user.id),
        skip=skip,
        limit=limit,
        status=status,
        company=company,
        job_board=job_board,
        keyword_terms=keyword_terms,
    )
    return applications


@router.get("/applications/{application_id}", response_model=JobApplicationOut)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    application = application_service.get_application(
        db, application_id=application_id, user_id=int(current_user.id)
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.put("/applications/{application_id}", response_model=JobApplicationOut)
def update_application(
    application_id: int,
    application_update: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Get existing application and its keywords
    db_application = application_service.get_application(
        db, application_id=application_id, user_id=int(current_user.id)
    )
    if not db_application:
        raise HTTPException(
            status_code=404, detail="Application not found or not authorized"
        )

    # Update basic application fields
    updated_application_data = application_update.model_dump(exclude_unset=True)
    for key, value in updated_application_data.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)
    return db_application


@router.delete("/applications/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_application = application_service.delete_application(
        db, application_id=application_id, user_id=int(current_user.id)
    )
    if not deleted_application:
        raise HTTPException(
            status_code=404, detail="Application not found or not authorized"
        )
    return
