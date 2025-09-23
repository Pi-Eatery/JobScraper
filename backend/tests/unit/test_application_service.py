import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.models.database import Base
from backend.src.models.user import User
from backend.src.models.job_application import JobApplication
from backend.src.services.application_service import ApplicationService

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
def db_session(setup_database, request):
    session = TestingSessionLocal()
    # Ensure a user exists for foreign key constraint
    unique_username = f"testuser_app_service_{request.node.name}"
    unique_email = f"test_app_service_{request.node.name}@example.com"
    user = User(username=unique_username, email=unique_email, password_hash="hashedpassword")
    session.add(user)
    session.commit()
    session.refresh(user)
    yield session
    session.close()

@pytest.fixture
def application_service():
    return ApplicationService()

@pytest.fixture
def test_user(db_session, request):
    # Retrieve the user created in db_session fixture. The username is now dynamic.
    unique_username = f"testuser_app_service_{request.node.name}"
    return db_session.query(User).filter(User.username == unique_username).first()

def test_create_application(db_session, application_service, test_user):
    new_application = application_service.create_application(
        db=db_session,
        user_id=test_user.id,
        job_title="Software Engineer",
        company="Tech Corp",
        application_date=date.today(),
        status="Applied",
        job_board="LinkedIn",
        url="http://linkedin.com/job/123",
        notes="First application",
        keywords="Python, FastAPI"
    )

    assert new_application.id is not None
    assert new_application.user_id == test_user.id
    assert new_application.job_title == "Software Engineer"
    assert new_application.company == "Tech Corp"
    assert new_application.application_date == date.today()

def test_get_applications(db_session, application_service, test_user):
    application_service.create_application(db_session, test_user.id, "App 1", "Comp A", date.today(), "Applied", "Board 1", "url1", "notes1", "keys1")
    application_service.create_application(db_session, test_user.id, "App 2", "Comp B", date.today(), "Interview", "Board 2", "url2", "notes2", "keys2")

    applications = application_service.get_applications(db_session, test_user.id)
    assert len(applications) == 2
    assert applications[0].job_title == "App 1"
    assert applications[1].job_title == "App 2"

    applications_limit_1 = application_service.get_applications(db_session, test_user.id, limit=1)
    assert len(applications_limit_1) == 1
    assert applications_limit_1[0].job_title == "App 1"

def test_get_application(db_session, application_service, test_user):
    created_app = application_service.create_application(db_session, test_user.id, "Single App", "Single Comp", date.today(), "Applied", "Board", "url", "notes", "keys")

    found_app = application_service.get_application(db_session, created_app.id, test_user.id)
    assert found_app is not None
    assert found_app.id == created_app.id
    assert found_app.job_title == "Single App"

    not_found_app = application_service.get_application(db_session, 999, test_user.id)
    assert not_found_app is None

    # Test getting an application belonging to another user
    other_user = User(username=f"otheruser_{request.node.name}", email=f"other_{request.node.name}@example.com", password_hash="hash")
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)
    not_found_app_other_user = application_service.get_application(db_session, created_app.id, other_user.id)
    assert not_found_app_other_user is None


def test_update_application(db_session, application_service, test_user):
    created_app = application_service.create_application(db_session, test_user.id, "Old Title", "Old Company", date.today(), "Applied", "Old Board", "old_url", "old_notes", "old_keys")

    updated_app = application_service.update_application(
        db=db_session,
        application_id=created_app.id,
        user_id=test_user.id,
        job_title="New Title",
        status="Interviewing",
        notes="Updated notes"
    )

    assert updated_app is not None
    assert updated_app.job_title == "New Title"
    assert updated_app.status == "Interviewing"
    assert updated_app.notes == "Updated notes"
    assert updated_app.company == "Old Company" # Unchanged

    not_found_updated_app = application_service.update_application(db_session, 999, test_user.id, job_title="Non Existent")
    assert not_found_updated_app is None

def test_delete_application(db_session, application_service, test_user):
    created_app = application_service.create_application(db_session, test_user.id, "Delete Me", "Delete Corp", date.today(), "Applied", "Board", "url", "notes", "keys")

    deleted_app = application_service.delete_application(db_session, created_app.id, test_user.id)
    assert deleted_app is not None
    assert deleted_app.id == created_app.id

    # Verify it's actually deleted
    assert db_session.query(JobApplication).filter(JobApplication.id == created_app.id).first() is None

    not_found_deleted_app = application_service.delete_application(db_session, 999, test_user.id)
    assert not_found_deleted_app is None