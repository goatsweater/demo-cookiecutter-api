import sqlalchemy as sa
from sqlalchemy import orm

from .config import get_settings


# Get the settings so we can create an engine
cfg = get_settings()

engine = sa.create_engine(cfg.DB_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(orm.DeclarativeBase):
    ...
