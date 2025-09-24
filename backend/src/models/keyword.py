from sqlalchemy import Column, Integer, String
from backend.src.models.database import Base


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<Keyword(term='{self.term}')>"
