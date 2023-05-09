import logging
from typing import Union

import sqlalchemy as sa
from sqlalchemy import orm

from .database import Base

logger = logging.getLogger(__name__)


class Meta(Base):
    # __tablename__ = "meta"
    __abstract__ = True  # This is a template of a table, not a table itself.

    series: orm.Mapped[str] = orm.mapped_column(sa.String(40), nullable=False, primary_key=True)
    attribute: orm.Mapped[str] = orm.mapped_column(sa.String(20), nullable=False, primary_key=True)
    value: orm.Mapped[str] = orm.mapped_column(nullable=False)


class Data(Base):
    # __tablename__ = "data"
    __abstract__ = True  # This is a template of a table, not a table itself.

    series: orm.Mapped[str] = orm.mapped_column(sa.String(40), nullable=False, primary_key=True)
    refperiod: orm.Mapped[str] = orm.mapped_column(sa.String(10), nullable=False, primary_key=True)
    value: orm.Mapped[float] = orm.mapped_column(nullable=False)
    status: orm.Mapped[str] = orm.mapped_column(sa.String(2))

class Control(Base):
    # __tablename__ = "control"
    __abstract__ = True  # This is a template of a table, not a table itself.

    id: orm.Mapped[str] = orm.mapped_column(sa.String(30), nullable=False, primary_key=True)
    value: orm.Mapped[str] = orm.mapped_column(nullable=True)


def get_table_instance(name: str, freq: str, base: Union[Meta, Data, Control]) -> Union[Meta, Data, Control]:
    """
    Retrieve an instance of a Meta, Data, or Control table to be used for interacting with the database.

    Tables in the database get loaded from an external system and are named according to their name, frequency, and type
    to with underscores (``_``) separating each term. i.e. wes_monthly_data.
    """
    table_suffix = ""
    if base == Meta:
        table_suffix = "Meta"
    elif base == Data:
        table_suffix = "Data"
    elif base == Control:
        table_suffix = "Control"
    else:
        raise ValueError("Invalid base type.")

    table_name = f"{name}_{freq}_{table_suffix}"
    logger.debug("Getting reference to table %s", table_name)

    # Look up the base metadata to see if this table is already registered
    if table_name in Base.metadata.tables:
        logger.debug("Found existing table reference in Base.")
        return Base.metadata.tables[table_name]
    
    # Instantiate a new table of the desired type
    table_instance = type(table_name, (base,), {
        "__tablename__": table_name
    })
    return table_instance