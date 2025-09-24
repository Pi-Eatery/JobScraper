import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.src.main import app
from backend.src.models.database import Base, get_db
from backend.src.models.job import Job
from backend.src.models.user import User as DBUser
from backend.src.middleware.auth import get_current_user

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session

    def override_get_current_user():
        # Mock a user for testing purposes
        return DBUser(id=1, username="testuser", password_hash="hashedpassword", email="test@example.com")

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_save_job(client: TestClient, session: Session):
    # Create a dummy job in the test database
    job = Job(title="Test Job", company="Test Co", description="Desc", application_link="http://example.com", user_id=1)
    session.add(job)
    session.commit()
    session.refresh(job)

    response = client.post(f"/api/jobs/{job.id}/save")
    assert response.status_code == 200
    assert response.json() == {"message": "Job saved successfully"}
    updated_job = session.query(Job).filter(Job.id == job.id).first()
    assert updated_job.status == "saved"

def test_apply_job(client: TestClient, session: Session):
    job = Job(title="Test Job 2", company="Test Co 2", description="Desc 2", application_link="http://example2.com", user_id=1)
    session.add(job)
    session.commit()
    session.refresh(job)

    response = client.post(f"/api/jobs/{job.id}/apply")
    assert response.status_code == 200
    assert response.json() == {"message": "Job marked as applied"}
    updated_job = session.query(Job).filter(Job.id == job.id).first()
    assert updated_job.status == "applied"

def test_hide_job(client: TestClient, session: Session):
    job = Job(title="Test Job 3", company="Test Co 3", description="Desc 3", application_link="http://example3.com", user_id=1)
    session.add(job)
    session.commit()
    session.refresh(job)

    response = client.post(f"/api/jobs/{job.id}/hide")
    assert response.status_code == 200
    assert response.json() == {"message": "Job hidden successfully"}
    updated_job = session.query(Job).filter(Job.id == job.id).first()
    assert updated_job.status == "hidden"

def test_job_not_found(client: TestClient):
    response = client.post("/api/jobs/999/save")
    assert response.status_code == 404
    assert response.json() == {"message": "Job not found or not authorized"}
