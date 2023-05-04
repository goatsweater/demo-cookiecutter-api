from datetime import datetime, date

from fastapi import APIRouter

from .schemas import response

###
# v1 routes
###
v1 = APIRouter(
    prefix="/v1",
    tags=["v1"]
)


@v1.get("/data/{db}/{interval}", response_model=response.Message)
def get_data(
    db: str,
    interval: str,
    series: str | None = None,
    refperiod: str | None = None,
    status: str | None = None,
    attributes: str = "all",
    updatedAfter: datetime | date | None = None,
    firstNObservations: int | None = None,
    lastNObservations: int | None = None):
    ...
