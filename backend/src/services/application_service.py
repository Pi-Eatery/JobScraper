from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.job_application import JobApplication
from ..models.keyword import Keyword
from datetime import date


class ApplicationService:
    def create_application(
        self,
        db: Session,
        user_id: int,
        job_title: str,
        company: str,
        application_date: date,
        status: str,
        job_board: Optional[str],
        url: Optional[str],
        notes: Optional[str],
    ):
        db_application = JobApplication(
            user_id=user_id,
            job_title=job_title,
            company=company,
            application_date=application_date,
            status=status,
            job_board=job_board,
            url=url,
            notes=notes,
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    def get_applications(
        self,
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        company: Optional[str] = None,
        job_board: Optional[str] = None,
        keyword_terms: Optional[List[str]] = None,
    ):
        query = db.query(JobApplication).filter(JobApplication.user_id == user_id)

        if status:
            query = query.filter(JobApplication.status == status)
        if company:
            query = query.filter(JobApplication.company.ilike(f"%{company}%"))
        if job_board:
            query = query.filter(JobApplication.job_board == job_board)
        if keyword_terms:
            query = query.join(JobApplication.keywords).filter(
                Keyword.term.in_(keyword_terms)
            )

        return query.offset(skip).limit(limit).all()

    def get_application(self, db: Session, application_id: int, user_id: int):
        return (
            db.query(JobApplication)
            .filter(
                JobApplication.id == application_id, JobApplication.user_id == user_id
            )
            .first()
        )

    def update_application(
        self,
        db: Session,
        application_id: int,
        user_id: int,
        job_title: Optional[str] = None,
        company: Optional[str] = None,
        application_date: Optional[date] = None,
        status: Optional[str] = None,
        job_board: Optional[str] = None,
        url: Optional[str] = None,
        notes: Optional[str] = None,
    ):
        db_application = self.get_application(db, application_id, user_id)
        if db_application:
            if job_title is not None:
                db_application.job_title = job_title
            if company is not None:
                db_application.company = company
            if application_date is not None:
                db_application.application_date = application_date
            if status is not None:
                db_application.status = status
            if job_board is not None:
                db_application.job_board = job_board
            if url is not None:
                db_application.url = url
            if notes is not None:
                db_application.notes = notes
            db.commit()
            db.refresh(db_application)
        return db_application

    def delete_application(self, db: Session, application_id: int, user_id: int):
        db_application = self.get_application(db, application_id, user_id)
        if db_application:
            db.delete(db_application)
            db.commit()
        return db_application
