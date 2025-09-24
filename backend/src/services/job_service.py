from sqlalchemy.orm import Session
from backend.src.models.job import Job
from backend.src.models.keyword import Keyword

def create_job(db: Session, job_data: dict, user_id: int):
    db_job = Job(**job_data, user_id=user_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Job).filter(Job.user_id == user_id).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int, user_id: int):
    return db.query(Job).filter(Job.id == job_id, Job.user_id == user_id).first()

def update_job_status(db: Session, job_id: int, user_id: int, new_status: str):
    db_job = get_job(db, job_id, user_id)
    if db_job:
        db_job.status = new_status
        db.commit()
        db.refresh(db_job)
    return db_job

def create_keyword(db: Session, term: str):
    db_keyword = Keyword(term=term)
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword

def get_keywords(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Keyword).offset(skip).limit(limit).all()
