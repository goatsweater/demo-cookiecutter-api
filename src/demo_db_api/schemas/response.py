"""
Schemas used when generating responses.

These are primarily based on the SDMX-JSON specification, although not attempting to be
fully compliant.
"""
from datetime import datetime

from pydantic import BaseModel


class Sender(BaseModel):
    """Sender information for responses."""
    id: str = "DEMO"
    name: str | None = None


class Meta(BaseModel):
    """Metadata included in responses to GET queries."""
    id: str
    prepared: datetime = datetime.utcnow()
    sender: Sender = Sender()


class DataStructure(BaseModel):
    """Provides the structural metadata necessary to interpret the data contained in the message."""
    dimensions: list[str]
    measures: list[str] | None = None
    attributes: list[str] | None = None
    annotations: list[str] | None = None


class Data(BaseModel):
    """Data provided as part of a GET response."""
    structures: list[DataStructure] | None = None
    dataSets: list[dict[str, str | float | int | None]] | None = None


class Error(BaseModel):
    """Any errors encountered that need to be sent back to clients."""
    code: int
    title: str | None = None
    detail: str | None = None


class Message(BaseModel):
    """Common response object that holds metadata, data, and errors."""
    meta: Meta
    data: Data | None = None
    errors: list[Error] | None = None
