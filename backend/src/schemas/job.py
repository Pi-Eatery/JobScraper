from pydantic import BaseModel
from typing import Optional, List


class JobBase(BaseModel):
    title: str
    company: str
    description: Optional[str] = None
    application_link: str
    salary: Optional[str] = None
    status: Optional[str] = "new"


class JobCreate(JobBase):
    pass


class JobOut(JobBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
