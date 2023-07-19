import asyncio
from collections.abc import AsyncGenerator

import aiosqlite
import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from mve_app.database import Base, engine
from mve_app.dependencies import get_db_session
from mve_app.main import app
from settings.config import settings


# This fixture is required to avoid `ScopeMismatch: You tried to access the function scoped fixture event_loop with a session scoped request object, involved factories:`
# Adapted from https://github.com/tortoise/tortoise-orm/issues/638#issuecomment-1264434398
@pytest.fixture(scope="session")
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Rationale: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.mark.asyncio
@pytest.fixture(scope="session", autouse=True)
async def setup_db(request):
    """
    Drop and create a fresh copy of a local test database with the latest schema before we run a new test suite.

    Check the full list of gathered tests for ANY tests that are marked "database" (using pytest.mark.database).
    """
    gathered_tests = request.node.items
    includes_tests_requiring_db = any(
        [test.get_closest_marker("database") for test in gathered_tests]
    )

    if includes_tests_requiring_db and settings.INITIALIZE_TEST_DATABASE:

        async def get_meta_connection():
            """
            Get connection to SQLite in which we can create/drop the test database.
            """
            return await aiosqlite.connect(":memory:")

        # create db
        db_ = await get_meta_connection()

        async with engine.begin() as connection:
            # initialize full data model with SQLAlchemy; don't worry about Alembic for migrations
            await connection.run_sync(Base.metadata.create_all)

        yield

        # drop the schema
        await engine.dispose()

        await db_.close()
    else:
        yield


@pytest.fixture(scope="function", autouse=True)
async def session():
    # Adapted from https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites

    connection = await engine.connect()
    transaction = await connection.begin()

    transactional_session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    # Adapted from
    # https://www.core27.co/post/transactional-unit-tests-with-pytest-and-async-sqlalchemy
    # https://gist.github.com/sidravic/785376313cbcfface398b9bc14ad6eac#file-db-py
    nested = await connection.begin_nested()

    @event.listens_for(transactional_session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
        transactional_session_maker = async_sessionmaker(
            bind=connection,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint",
        )
        async with transactional_session_maker() as session:
            yield session

    # override get_db_session dependency
    app.dependency_overrides[get_db_session] = get_db_session

    yield transactional_session

    await transactional_session.close()
    await transaction.rollback()
    await connection.close()
