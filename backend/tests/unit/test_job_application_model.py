import pytest
from datetime import date
from src.models.job_application import JobApplication
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
def db_session(setup_database, request):
    session = TestingSessionLocal()
    # Ensure a user exists for foreign key constraint
    unique_email = f"testuser_{request.node.name}@example.com"
    user = User(
        username=f"testuser_{request.node.name}",
        email=unique_email,
        password_hash="hashedpassword",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    yield session
    session.close()


def test_create_job_application(db_session, request):
    user = (
        db_session.query(User)
        .filter(User.username == f"testuser_{request.node.name}")
        .first()
    )
    new_application = JobApplication(
        user_id=user.id,
        job_title="Software Engineer",
        company="Tech Corp",
        application_date=date.today(),
        status="Applied",
        job_board="LinkedIn",
        url="http://linkedin.com/job/123",
        notes="First application",
        keywords="Python, FastAPI",
    )
    db_session.add(new_application)
    db_session.commit()
    db_session.refresh(new_application)

    assert new_application.id is not None
    assert new_application.user_id == user.id
    assert new_application.job_title == "Software Engineer"
    assert new_application.company == "Tech Corp"
    assert new_application.application_date == date.today()
    assert new_application.status == "Applied"
    assert new_application.job_board == "LinkedIn"
    assert new_application.url == "http://linkedin.com/job/123"
    assert new_application.notes == "First application"
    assert new_application.keywords == "Python, FastAPI"


def test_get_job_application_by_id(db_session, request):
    user = (
        db_session.query(User)
        .filter(User.username == f"testuser_{request.node.name}")
        .first()
    )
    new_application = JobApplication(
        user_id=user.id,
        job_title="Data Scientist",
        company="Data Co",
        application_date=date.today(),
        status="Interviewing",
        job_board="Indeed",
        url="http://indeed.com/job/456",
        notes="Second application",
        keywords="R, SQL",
    )
    db_session.add(new_application)
    db_session.commit()
    db_session.refresh(new_application)

    found_application = (
        db_session.query(JobApplication)
        .filter(JobApplication.id == new_application.id)
        .first()
    )
    assert found_application is not None
    assert found_application.job_title == "Data Scientist"


def test_update_job_application(db_session, request):
    user = (
        db_session.query(User)
        .filter(User.username == f"testuser_{request.node.name}")
        .first()
    )
    new_application = JobApplication(
        user_id=user.id,
        job_title="DevOps Engineer",
        company="Cloud Solutions",
        application_date=date.today(),
        status="Applied",
        job_board="Glassdoor",
        url="http://glassdoor.com/job/789",
        notes="Third application",
        keywords="AWS, Docker",
    )
    db_session.add(new_application)
    db_session.commit()
    db_session.refresh(new_application)

    new_application.status = "Offer"
    new_application.notes = "Received offer!"
    db_session.add(new_application)
    db_session.commit()
    db_session.refresh(new_application)

    updated_application = (
        db_session.query(JobApplication)
        .filter(JobApplication.id == new_application.id)
        .first()
    )
    assert updated_application.status == "Offer"
    assert updated_application.notes == "Received offer!"


def test_delete_job_application(db_session, request):
    user = (
        db_session.query(User)
        .filter(User.username == f"testuser_{request.node.name}")
        .first()
    )
    new_application = JobApplication(
        user_id=user.id,
        job_title="QA Engineer",
        company="Test Co",
        application_date=date.today(),
        status="Applied",
        job_board="Monster",
        url="http://monster.com/job/101",
        notes="Fourth application",
        keywords="Automation",
    )
    db_session.add(new_application)
    db_session.commit()
    db_session.refresh(new_application)

    db_session.delete(new_application)
    db_session.commit()

    deleted_application = (
        db_session.query(JobApplication)
        .filter(JobApplication.id == new_application.id)
        .first()
    )
    assert deleted_application is None


def test_job_applications_relationship_with_user(db_session, request):
    user = (
        db_session.query(User)
        .filter(User.username == f"testuser_{request.node.name}")
        .first()
    )
    app1 = JobApplication(
        user_id=user.id,
        job_title="Jr. Dev",
        company="A",
        application_date=date.today(),
        status="Applied",
    )
    app2 = JobApplication(
        user_id=user.id,
        job_title="Sr. Dev",
        company="B",
        application_date=date.today(),
        status="Applied",
    )
    db_session.add_all([app1, app2])
    db_session.commit()
    db_session.refresh(user)

    assert len(user.applications) == 2
    assert app1 in user.applications
    assert app2 in user.applications
