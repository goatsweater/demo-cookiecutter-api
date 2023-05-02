import sqlalchemy as sa
from sqlalchemy import orm

from .database import Base


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


def get_meta_instance(name: str) -> Meta:
    """Produce a named instance of the desired table template."""
    tblname = f"{name}_meta"
    class_name = f"Meta"
    Model = type(class_name, (Meta,), {
        '__tablename__': tblname
    })
    return Model

def get_data_instance(name: str) -> Data:
    """Produce a named instance of the desired table template."""
    tblname = f"{name}_data"
    class_name = f"Data"
    Model = type(class_name, (Data,), {
        '__tablename__': tblname
    })
    return Model

def get_control_instance(name: str) -> Control:
    """Produce a named instance of the desired table template."""
    tblname = f"{name}_control"
    class_name = f"Control"
    Model = type(class_name, (Control,), {
        '__tablename__': tblname
    })
    return Model
