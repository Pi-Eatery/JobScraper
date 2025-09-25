from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class KeywordBase(BaseModel):
    term: str


class KeywordOut(KeywordBase):
    id: int

    class Config:
        orm_mode = True


class JobApplicationBase(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    application_date: Optional[date] = None
    status: Optional[str] = None
    job_board: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    job_title: str
    company: str
    application_date: date
    status: str
    keywords: List[str] = Field(default_factory=list)


class JobApplicationUpdate(JobApplicationBase):
    job_title: Optional[str] = None
    company: Optional[str] = None
    application_date: Optional[date] = None
    status: Optional[str] = None


class JobApplicationOut(JobApplicationBase):
    id: int
    user_id: int
    keywords: List[KeywordOut] = Field(default_factory=list)

    class Config:
        orm_mode = True
