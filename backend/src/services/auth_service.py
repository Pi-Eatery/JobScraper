from sqlalchemy.orm import Session
from ..models.user import User
from passlib.context import CryptContext # For password hashing, assuming installation

# For password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class AuthService:
    def register_user(self, db: Session, username: str, email: str, password: str):
        hashed_password = get_password_hash(password)
        db_user = User(username=username, email=email, password_hash=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate_user(self, db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user