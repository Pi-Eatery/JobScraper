import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from backend.src.services import job_service
from backend.src.models.job import Job
from backend.src.models.keyword import Keyword

@pytest.fixture
def mock_db_session():
    session = MagicMock(spec=Session)
    return session

def test_create_job(mock_db_session):
    job_data = {"title": "Test Job", "company": "Test Co", "description": "Desc", "application_link": "http://example.com"}
    user_id = 1
    job = job_service.create_job(mock_db_session, job_data, user_id)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert job.title == "Test Job"
    assert job.user_id == user_id

def test_get_jobs(mock_db_session):
    user_id = 1
    mock_db_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = [
        Job(id=1, title="Job 1", company="Comp 1", user_id=user_id),
        Job(id=2, title="Job 2", company="Comp 2", user_id=user_id),
    ]
    jobs = job_service.get_jobs(mock_db_session, user_id)
    assert len(jobs) == 2
    assert jobs[0].user_id == user_id

def test_get_job(mock_db_session):
    user_id = 1
    job_id = 1
    mock_db_session.query.return_value.filter.return_value.first.return_value = Job(id=job_id, title="Job 1", company="Comp 1", user_id=user_id)
    job = job_service.get_job(mock_db_session, job_id, user_id)
    assert job.id == job_id
    assert job.user_id == user_id

def test_update_job_status(mock_db_session):
    user_id = 1
    job_id = 1
    new_status = "applied"
    mock_job = Job(id=job_id, title="Job 1", company="Comp 1", user_id=user_id, status="new")
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_job

    updated_job = job_service.update_job_status(mock_db_session, job_id, user_id, new_status)

    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert updated_job.status == new_status

def test_create_keyword(mock_db_session):
    term = "Python"
    keyword = job_service.create_keyword(mock_db_session, term)

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()
    assert keyword.term == term

def test_get_keywords(mock_db_session):
    mock_db_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        Keyword(id=1, term="Python"),
        Keyword(id=2, term="Java"),
    ]
    keywords = job_service.get_keywords(mock_db_session)
    assert len(keywords) == 2
    assert keywords[0].term == "Python"
