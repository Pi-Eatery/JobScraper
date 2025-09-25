import pytest
from sqlalchemy import Column, Integer, String, ForeignKey
from src.models.job import Job


def test_job_tablename():
    assert Job.__tablename__ == "jobs"


def test_job_column_definitions():
    # Test 'id' column
    id_column = Job.__table__.columns["id"]
    assert isinstance(id_column, Column)
    assert id_column.type.python_type == int
    assert id_column.primary_key is True
    assert id_column.index is True

    # Test 'title' column
    title_column = Job.__table__.columns["title"]
    assert isinstance(title_column, Column)
    assert title_column.type.python_type == str
    assert title_column.index is True

    # Test 'company' column
    company_column = Job.__table__.columns["company"]
    assert isinstance(company_column, Column)
    assert company_column.type.python_type == str
    assert company_column.index is True

    # Test 'description' column
    description_column = Job.__table__.columns["description"]
    assert isinstance(description_column, Column)
    assert description_column.type.python_type == str

    # Test 'application_link' column
    application_link_column = Job.__table__.columns["application_link"]
    assert isinstance(application_link_column, Column)
    assert application_link_column.type.python_type == str
    assert application_link_column.nullable is False

    # Test 'salary' column
    salary_column = Job.__table__.columns["salary"]
    assert isinstance(salary_column, Column)
    assert salary_column.type.python_type == str
    assert salary_column.nullable is True

    # Test 'status' column
    status_column = Job.__table__.columns["status"]
    assert isinstance(status_column, Column)
    assert status_column.type.python_type == str
    assert status_column.default.arg == "new"

    # Test 'user_id' column
    user_id_column = Job.__table__.columns["user_id"]
    assert isinstance(user_id_column, Column)
    assert user_id_column.type.python_type == int
    assert isinstance(user_id_column.foreign_keys, set)
    assert len(user_id_column.foreign_keys) == 1
    assert list(user_id_column.foreign_keys)[0].column.name == "id"
    assert list(user_id_column.foreign_keys)[0].column.table.name == "users"


def test_job_repr():
    job = Job(title="Software Engineer", company="Google")
    assert repr(job) == "<Job(title='Software Engineer', company='Google')>"
