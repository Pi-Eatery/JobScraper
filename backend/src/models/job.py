from sqlalchemy import Column, Integer, String, ForeignKey
from backend.src.models.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(String)
    application_link = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    status = Column(String, default="new")
    user_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>""
