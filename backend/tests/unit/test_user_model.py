import pytest
from backend.src.models.user import User
from backend.src.models.database import Base, engine, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    session = TestingSessionLocal()
    yield session
    session.close()

def test_create_user(db_session):
    new_user = User(username="testuser", email="test@example.com", password_hash="hashedpassword")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    assert new_user.id is not None
    assert new_user.username == "testuser"
    assert new_user.email == "test@example.com"
    assert new_user.password_hash == "hashedpassword"

def test_get_user_by_username(db_session):
    new_user = User(username="findme", email="findme@example.com", password_hash="hash")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    found_user = db_session.query(User).filter(User.username == "findme").first()
    assert found_user is not None
    assert found_user.username == "findme"

def test_get_user_by_email(db_session):
    new_user = User(username="emailuser", email="email@example.com", password_hash="hash")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    found_user = db_session.query(User).filter(User.email == "email@example.com").first()
    assert found_user is not None
    assert found_user.email == "email@example.com"

def test_unique_username(db_session):
    user1 = User(username="unique", email="unique1@example.com", password_hash="hash")
    user2 = User(username="unique", email="unique2@example.com", password_hash="hash")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()

def test_unique_email(db_session):
    user1 = User(username="user1", email="emailunique@example.com", password_hash="hash")
    user2 = User(username="user2", email="emailunique@example.com", password_hash="hash")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()