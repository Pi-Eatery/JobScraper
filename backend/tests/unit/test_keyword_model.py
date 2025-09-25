import pytest
from sqlalchemy import Column, Integer, String
from src.models.keyword import Keyword


def test_keyword_tablename():
    assert Keyword.__tablename__ == "keywords"


def test_keyword_column_definitions():
    # Test 'id' column
    id_column = Keyword.__table__.columns["id"]
    assert isinstance(id_column, Column)
    assert id_column.type.python_type == int
    assert id_column.primary_key is True
    assert id_column.index is True

    # Test 'term' column
    term_column = Keyword.__table__.columns["term"]
    assert isinstance(term_column, Column)
    assert term_column.type.python_type == str
    assert term_column.unique is True
    assert term_column.index is True


def test_keyword_repr():
    keyword = Keyword(term="Python")
    assert repr(keyword) == "<Keyword(term='Python')>"
