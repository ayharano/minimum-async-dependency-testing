from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from mve_app.dependencies import get_db_session
from mve_app.models import T1
from mve_app.schemas import T1Schema

dummy_router = APIRouter(prefix="/db-integration")


@dummy_router.get("/", response_model=list[str])
async def get_list(session: AsyncSession = Depends(get_db_session)):
    query = select(T1.name).order_by(T1.name)

    result_list = (await session.execute(query)).scalars().all()

    return result_list


@dummy_router.get("/{name}/", response_model=T1Schema)
async def get_detail(name: str, session: AsyncSession = Depends(get_db_session)):
    query = select(T1).where(T1.name == name).limit(1)

    try:
        result_instance = (await session.execute(query)).scalars().one()
    except NoResultFound:
        return JSONResponse(
            {"detail": f"{name} not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return result_instance
