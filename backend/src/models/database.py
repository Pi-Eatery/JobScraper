from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL. The /// means it's a relative path to the current directory.
# You can change this to other database URLs (e.g., PostgreSQL, MySQL) as needed.
DATABASE_URL = "sqlite:///./sql_app.db"

# Create the SQLAlchemy engine
# The connect_args is specific to SQLite for handling concurrent requests
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
# Each instance of SessionLocal will be a database session
# The autocommit=False means that you'll have to explicitly commit transactions
# The autoflush=False prevents the session from flushing changes to the DB after every query
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base class for declarative models
# All your SQLAlchemy models will inherit from this Base
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()