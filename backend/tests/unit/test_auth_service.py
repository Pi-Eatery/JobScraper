import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.database import Base
from src.models.user import User
from src.services.auth_service import AuthService, get_password_hash, verify_password

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
def unique_email_generator(request):
    """Fixture to generate unique emails for each test function."""
    counter = 0

    def _generator():
        nonlocal counter
        counter += 1
        return f"user_{request.node.name}_{counter}@example.com"

    return _generator


@pytest.fixture
def auth_service():
    return AuthService()


def test_get_password_hash():
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)
    assert len(hashed_password) > 0
    assert hashed_password != password  # Should not be plain text


def test_verify_password():
    password = "testpassword"
    hashed_password = get_password_hash(password)

    assert verify_password(password, hashed_password)
    assert not verify_password("wrongpassword", hashed_password)


def test_register_user(db_session, auth_service, unique_email_generator):
    username = "newuser"
    email = unique_email_generator()
    password = "newpassword"

    user = auth_service.register_user(db_session, username, email, password)

    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(password, user.password_hash)

    # Verify user is in the database
    db_user = db_session.query(User).filter(User.username == username).first()
    assert db_user is not None
    assert db_user.email == email


def test_authenticate_user_success(db_session, auth_service, unique_email_generator):
    username = "authuser"
    email = unique_email_generator()
    password = "authpassword"
    auth_service.register_user(db_session, username, email, password)

    authenticated_user = auth_service.authenticate_user(db_session, username, password)
    assert authenticated_user is not None
    assert authenticated_user.username == username


def test_authenticate_user_wrong_password(
    db_session, auth_service, unique_email_generator
):
    username = "wrongpassuser"
    email = unique_email_generator()
    password = "correctpassword"
    auth_service.register_user(db_session, username, email, password)

    authenticated_user = auth_service.authenticate_user(
        db_session, username, "wrongpassword"
    )
    assert authenticated_user is None


def test_authenticate_user_not_found(db_session, auth_service):
    authenticated_user = auth_service.authenticate_user(
        db_session, "nonexistentuser", "anypassword"
    )
    assert authenticated_user is None


def test_register_duplicate_username(db_session, auth_service, unique_email_generator):
    username = "duplicate"
    email1 = unique_email_generator()
    email2 = unique_email_generator()
    password = "password"

    auth_service.register_user(db_session, username, email1, password)

    with pytest.raises(Exception):  # Assuming integrity error from SQLAlchemy
        auth_service.register_user(db_session, username, email2, password)


def test_register_duplicate_email(db_session, auth_service, unique_email_generator):
    username1 = "duplicate_email1"
    username2 = "duplicate_email2"
    email = unique_email_generator()
    password = "password"

    auth_service.register_user(db_session, username1, email, password)

    with pytest.raises(Exception):  # Assuming integrity error from SQLAlchemy
        auth_service.register_user(db_session, username2, email, password)
