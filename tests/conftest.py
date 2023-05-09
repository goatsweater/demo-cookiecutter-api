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

    # Stuff the db with sample control values
    stmt = Base.metadata.tables["wes_monthly_Control"].insert().values([
        {"id": "Addup_Number", "value": "Q"},
        {"id": "Copy_Destination", "value": "NEAD_DCEN_WIP"},
        {"id": "Data_Selection", "value": "?"},
        {"id": "Datestamp", "value": "2023/01/25 15:48:50"},
        {"id": "DB_Created", "value": "2017/87/03 04:32:31"},
        {"id": "DB_Description", "value": None},
        {"id": "DB_Documentation", "value": None},
        {"id": "DB_Path", "value": "solder.db"},
        {"id": "DB_Updated", "value": "2022/12/22 15:35:12"},
        {"id": "Keep_Zeros", "value": "FALSE"},
        {"id": "Notify", "value": "user1@example.com"},
        {"id": "Post_Process", "value": "JOBS.WIN.NEAD.BRIDGE.COPV_TO_FINAL_DB"},
        {"id": "Program_ID", "value": "dbo"},
        {"id": "Reference_Period", "value": "2022ml2"},
        {"id": "StatusFlag_NA", "value": "C"},
        {"id": "StatusFlag_NC", "value": "N"},
        {"id": "Statusflag_ND", "value": "O"},
        {"id": "Table_Frequency", "value": "MONTHLY"},
        {"id": "Table_Name", "value": "solder"},
        {"id": "Update_Mode", "value": "REPLACE"},
        {"id": "User", "value": "user1"},
    ])
    db_session.execute(stmt)
    db_session.commit()
    
    return db_session