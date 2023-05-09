import pytest

import sqlalchemy as sa
from sqlalchemy import orm

from demo_db_api.database import Base
from demo_db_api import models


# Generate a session for use within this module
@pytest.fixture(scope="module")
def db_session(tmp_path_factory):
    temp_db = tmp_path_factory.mktemp("data") / "app.db"
    engine = sa.create_engine(f"sqlite:///{temp_db}", connect_args={"check_same_thread": False}, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


# Generate valid data for use in testing
@pytest.fixture(scope="module")
def db_data(db_session):
    # Create some tables
    wes_monthly_meta = models.get_table_instance("wes", "monthly", models.Meta)
    wes_monthly_data = models.get_table_instance("wes", "monthly", models.Data)
    wes_monthly_control = models.get_table_instance("wes", "monthly", models.Control)
    Base.metadata.create_all(db_session.get_bind())
    db_session.commit()

    # Stuff the db with sample metadata
    stmt = Base.metadata.tables["wes_monthly_Meta"].insert().values([
        {"series": "WES51", "attribute": "Basis", "value": "DAILY"},
        {"series": "WES51", "attribute": "Created", "value": "2017/07/03 04:36:10"},
        {"series": "WES51", "attribute": "Frequency", "value": "MONTHLY"},
        {"series": "WES51", "attribute": "LastUpdated", "value": "2022/05/06 10:19:16"},
        {"series": "WES51", "attribute": "Observed", "value": "SUMMED"}
    ])
    db_session.execute(stmt)
    db_session.commit()

    # Stuff the db with sample data
    stmt = Base.metadata.tables["wes_monthly_Data"].insert().values([
        {"series": "WES51", "refperiod": "2009m01", "value": "28267.73", "status": "A"},
        {"series": "WES51", "refperiod": "2009m02", "value": "29067.72", "status": "A"}
    ])
    db_session.execute(stmt)
    db_session.commit()
    
    return db_session


@pytest.mark.parametrize("table_type", [models.Meta, models.Data])
def test_get_table(db_data, table_type):
    tbl = models.get_table_instance("wes", "monthly", table_type)
    stmt = sa.select(tbl)

    row = db_data.execute(stmt).first()

    assert row.series == "WES51"


def test_get_invalid_table_type(db_data):
    """Request a table type that is not Meta, Data, or Control."""
    with pytest.raises(ValueError):
        tbl = models.get_table_instance("wes", "monthly", str)
