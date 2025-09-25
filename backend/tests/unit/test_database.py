import pytest
from unittest.mock import MagicMock, patch


def test_database_url():
    from backend.src.models.database import DATABASE_URL

    assert DATABASE_URL == "sqlite:///./sql_app.db"


def test_get_db_dependency():
    from backend.src.models.database import get_db

    mock_db_session = MagicMock()
    with patch(
        "backend.src.models.database.SessionLocal", return_value=mock_db_session
    ):
        db_generator = get_db()
        db = next(db_generator)
        assert db == mock_db_session
        with pytest.raises(StopIteration):
            next(db_generator)  # Ensure the generator yields only once
        mock_db_session.close.assert_called_once()
