from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    # Those two additional settings are related to SQLite:
    # https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#using-a-memory-database-in-multiple-threads
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    # Construct from https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-orm
    pass
