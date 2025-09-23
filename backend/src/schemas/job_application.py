from pydantic import BaseModel
from typing import Optional
from datetime import date


class JobApplicationBase(BaseModel):
    job_title: str
    company: str
    application_date: date
    status: str
    job_board: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None
    keywords: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationUpdate(JobApplicationBase):
    job_title: Optional[str] = None
    company: Optional[str] = None
    application_date: Optional[date] = None
    status: Optional[str] = None


class JobApplicationOut(JobApplicationBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
