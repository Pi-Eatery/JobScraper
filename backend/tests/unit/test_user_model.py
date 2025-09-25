import pytest
from src.models.user import User
from src.models.database import Base, engine, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
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


@pytest.fixture
def unique_user_generator(request):
    """Fixture to generate unique usernames and emails for each test function."""
    counter = 0

    def _generator():
        nonlocal counter
        counter += 1
        username = f"testuser_{request.node.name}_{counter}"
        email = f"test_{request.node.name}_{counter}@example.com"
        return username, email

    return _generator


def test_create_user(db_session, unique_user_generator):
    username, email = unique_user_generator()
    new_user = User(username=username, email=email, password_hash="hashedpassword")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    assert new_user.id is not None
    assert new_user.username == username
    assert new_user.email == email
    assert new_user.password_hash == "hashedpassword"


def test_get_user_by_username(db_session, unique_user_generator):
    username, email = unique_user_generator()
    new_user = User(username=username, email=email, password_hash="hash")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    found_user = db_session.query(User).filter(User.username == username).first()
    assert found_user is not None
    assert found_user.username == username


def test_get_user_by_email(db_session, unique_user_generator):
    username, email = unique_user_generator()
    new_user = User(username=username, email=email, password_hash="hash")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    found_user = db_session.query(User).filter(User.email == email).first()
    assert found_user is not None
    assert found_user.email == email


def test_unique_username(db_session, unique_user_generator):
    username, email1 = unique_user_generator()
    _, email2 = (
        unique_user_generator()
    )  # Generate another unique email for the second user
    user1 = User(username=username, email=email1, password_hash="hash")
    user2 = User(username=username, email=email2, password_hash="hash")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()


def test_unique_email(db_session, unique_user_generator):
    username1, email = unique_user_generator()
    username2, _ = (
        unique_user_generator()
    )  # Generate another unique username for the second user
    user1 = User(username=username1, email=email, password_hash="hash")
    user2 = User(username=username2, email=email, password_hash="hash")
    db_session.add(user1)
    db_session.commit()

    with pytest.raises(Exception):
        db_session.add(user2)
        db_session.commit()
