from sqlalchemy.orm import Session
from ..models.job_application import JobApplication
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
        job_board: str,
        url: str,
        notes: str,
        keywords: str,
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
            keywords=keywords,
        )
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    def get_applications(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ):
        return (
            db.query(JobApplication)
            .filter(JobApplication.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

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
        job_title: str = None,
        company: str = None,
        application_date: date = None,
        status: str = None,
        job_board: str = None,
        url: str = None,
        notes: str = None,
        keywords: str = None,
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
            if keywords is not None:
                db_application.keywords = keywords
            db.commit()
            db.refresh(db_application)
        return db_application

    def delete_application(self, db: Session, application_id: int, user_id: int):
        db_application = self.get_application(db, application_id, user_id)
        if db_application:
            db.delete(db_application)
            db.commit()
        return db_application
