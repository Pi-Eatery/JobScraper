from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between jobs and keywords
job_keywords_association = Table(
    "job_keywords_association",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id"), primary_key=True),
    Column("keyword_id", Integer, ForeignKey("keywords.id"), primary_key=True),
)


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

    keywords = relationship(
        "Keyword", secondary=job_keywords_association, back_populates="jobs"
    )

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}')>"
