from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..services.auth_service import AuthService
from ..schemas.user import UserCreate, UserLogin, UserOut, Token

router = APIRouter()
auth_service = AuthService()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = auth_service.register_user(db, user.username, user.email, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Error registering user"
        )
    return db_user


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = auth_service.authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real application, you'd generate a JWT token here
    access_token = ""  # Placeholder: Replace with actual JWT generation
    return {"access_token": access_token, "token_type": "bearer"}
