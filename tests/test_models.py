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
    wes_monthly_meta = models.get_meta_instance("wes_monthly")
    wes_monthly_data = models.get_data_instance("wes_monthly")
    wes_monthly_control = models.get_control_instance("wes_montly")
    Base.metadata.create_all(db_session.get_bind())
    db_session.commit()

    # Stuff the db with sample metadata
    stmt = Base.metadata.tables["wes_monthly_meta"].insert().values([
        {"series": "WES51", "attribute": "Basis", "value": "DAILY"},
        {"series": "WES51", "attribute": "Created", "value": "2017/07/03 04:36:10"},
        {"series": "WES51", "attribute": "Frequency", "value": "MONTHLY"},
        {"series": "WES51", "attribute": "LastUpdated", "value": "2022/05/06 10:19:16"},
        {"series": "WES51", "attribute": "Observed", "value": "SUMMED"}
    ])
    db_session.execute(stmt)
    db_session.commit()

    # Stuff the db with sample data
    stmt = Base.metadata.tables["wes_monthly_data"].insert().values([
        {"series": "WES51", "refperiod": "2009m01", "value": "28267.73", "status": "A"},
        {"series": "WES51", "refperiod": "2009m02", "value": "29067.72", "status": "A"}
    ])
    db_session.execute(stmt)
    db_session.commit()
    
    return db_session


def test_get_meta_table(db_data):
    tbl = Base.metadata.tables["wes_monthly_meta"]
    stmt = sa.select(tbl)

    row = db_data.scalars(stmt).first()

    assert row == "WES51"
