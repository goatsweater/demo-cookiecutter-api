from datetime import datetime, date
from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy import orm

from . import crud
from .database import SessionLocal
from .schemas import response

###
# v1 routes
###
v1 = APIRouter(
    prefix="/v1",
    tags=["v1"]
)


# Generate a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@v1.get("/data/{db}/{interval}", response_model=response.Message)
def get_data(
    db: str,
    interval: str,
    series: Union[str, None] = None,
    refperiod: Union[str, None] = None,
    status: Union[str, None] = None,
    attributes: str = "all",
    updatedAfter: Union[datetime, date, None] = None,
    firstNObservations: Union[int, None] = None,
    lastNObservations: Union[int, None] = None):
    ...


@v1.get("/availability", tags=["availability"])
def list_dbs(db: orm.Session = Depends(get_db)):
    """Generate a list of all available databases and their frequency."""
    bound_engine = db.get_bind()
    table_match = "Meta"
    control_tables = crud.get_table_names(bound_engine, like=table_match)
    
    # Table names take the form of <db>_<freq>_<type>, so split each into components
    available = []
    for table in control_tables:
        # Strip the table type off
        table = table.rsplit("_", maxsplit=1)[0]
        
        db_name, freq = table.rsplit("_", maxsplit=1)
        available.append({"db": db_name, "freq": freq})
    
    return available
            