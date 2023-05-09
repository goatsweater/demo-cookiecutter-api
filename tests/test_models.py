import pytest

import sqlalchemy as sa

from demo_db_api import models


@pytest.mark.parametrize("table_type", [models.Meta, models.Data, models.Control])
def test_get_table(db_data, table_type):
    tbl = models.get_table_instance("wes", "monthly", table_type)
    stmt = sa.select(tbl)

    row = db_data.execute(stmt).first()

    # Control tables only have id and value fields
    if table_type == models.Control:
        assert row.id == "Addup_Number"
    else:
        assert row.series == "WES51"


def test_get_invalid_table_type(db_data):
    """Request a table type that is not Meta, Data, or Control."""
    with pytest.raises(ValueError):
        tbl = models.get_table_instance("wes", "monthly", str)
