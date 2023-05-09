from typing import List

from demo_db_api import crud


def test_list_tables_like(db_data):
    """Test fetching list of available tables based on string matches."""
    engine = db_data.get_bind()

    table_list = crud.get_table_names(engine, like="Control")

    assert isinstance(table_list, List)
    assert len(table_list) == 1


def test_list_tables_regex(db_data):
    """Test fetching a list of available tables based on a regex match."""
    engine = db_data.get_bind()

    table_list = crud.get_table_names(engine, regex="wes_monthly")

    assert isinstance(table_list, List)
    assert len(table_list) == 3


def test_list_tables_names(db_data):
    """Test fetching a list of available tables based on a specific list."""
    engine = db_data.get_bind()

    expected = ["wes_monthly_Data", "wes_monthly_Meta"]
    table_list = crud.get_table_names(engine, items=expected)

    assert isinstance(table_list, List)
    assert len(table_list) == 2
