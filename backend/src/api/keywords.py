from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..models.user import User
from ..schemas.job_application import KeywordBase, KeywordOut
from ..services.keyword_service import KeywordService
from ..middleware.auth import get_current_user

router = APIRouter()
keyword_service = KeywordService()


@router.post(
    "/keywords/", response_model=KeywordOut, status_code=status.HTTP_201_CREATED
)
def create_keyword(
    keyword: KeywordBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_keyword = keyword_service.get_keyword_by_term(db, term=keyword.term)
    if db_keyword:
        raise HTTPException(status_code=400, detail="Keyword already registered")
    return keyword_service.create_keyword(
        db=db, term=keyword.term, user_id=int(current_user.id)
    )


@router.get("/keywords/", response_model=List[KeywordOut])
def read_keywords(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    keywords = keyword_service.get_keywords(
        db, user_id=int(current_user.id), skip=skip, limit=limit
    )
    return keywords


@router.get("/keywords/{keyword_id}", response_model=KeywordOut)
def read_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    keyword = keyword_service.get_keyword(
        db, keyword_id=keyword_id, user_id=int(current_user.id)
    )
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword


@router.delete("/keywords/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_keyword(
    keyword_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = keyword_service.delete_keyword(
        db, keyword_id=keyword_id, user_id=int(current_user.id)
    )
    if not deleted:
        raise HTTPException(
            status_code=404, detail="Keyword not found or not authorized"
        )
    return
