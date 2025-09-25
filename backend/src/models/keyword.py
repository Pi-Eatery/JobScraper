from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .job import job_keywords_association
from .user import User


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    jobs = relationship(
        "Job", secondary=job_keywords_association, back_populates="keywords"
    )
    user = relationship("User", back_populates="keywords")

    def __repr__(self):
        return f"<Keyword(term='{self.term}')>"
