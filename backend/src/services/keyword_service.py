from sqlalchemy.orm import Session
from ..models.keyword import Keyword


class KeywordService:
    def create_keyword(self, db: Session, term: str, user_id: int):
        db_keyword = Keyword(term=term, user_id=user_id)
        db.add(db_keyword)
        db.commit()
        db.refresh(db_keyword)
        return db_keyword

    def get_keyword(self, db: Session, keyword_id: int, user_id: int):
        return (
            db.query(Keyword)
            .filter(Keyword.id == keyword_id, Keyword.user_id == user_id)
            .first()
        )

    def get_keyword_by_term(self, db: Session, term: str):
        return db.query(Keyword).filter(Keyword.term == term).first()

    def get_keywords(self, db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(Keyword)
            .filter(Keyword.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete_keyword(self, db: Session, keyword_id: int, user_id: int):
        db_keyword = (
            db.query(Keyword)
            .filter(Keyword.id == keyword_id, Keyword.user_id == user_id)
            .first()
        )
        if db_keyword:
            db.delete(db_keyword)
            db.commit()
            return True
        return False
