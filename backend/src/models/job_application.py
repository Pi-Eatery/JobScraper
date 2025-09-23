from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_title = Column(String)
    company = Column(String)
    application_date = Column(Date)
    status = Column(String)
    job_board = Column(String)
    url = Column(String)
    notes = Column(Text)
    keywords = Column(
        String
    )  # Storing as String for now, could be improved with array type or separate table

    user = relationship("User", back_populates="applications")
