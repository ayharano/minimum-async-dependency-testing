from mve_app.database import SessionLocal


async def get_db_session():
    async with SessionLocal() as session:
        yield session
