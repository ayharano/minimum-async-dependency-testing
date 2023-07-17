import pytest
from fastapi import APIRouter
from httpx import AsyncClient
from starlette import status
from starlette.responses import JSONResponse

from mve_app.main import app
from mve_app.models import T1

middleware_testing_router = APIRouter(prefix="/test-middleware")


@middleware_testing_router.get("/")
async def get_root():
    return JSONResponse("ok", status_code=status.HTTP_200_OK)


app.include_router(middleware_testing_router)


@pytest.mark.asyncio
@pytest.mark.database
async def test_get_list(session):
    async with session.begin():
        session.add_all(
            [
                T1(name="omega", character="Ω"),
                T1(name="alpha", character="Α"),
                T1(name="nu", character="Ν"),
            ]
        )

    async with AsyncClient(app=app, base_url="http://example.com") as ac:
        response = await ac.get("/db-integration/")

    assert response.json() == [
        "alpha",
        "nu",
        "omega",
    ]
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.database
async def test_get_detail(session):
    async with session.begin():
        session.add_all(
            [
                T1(name="delta", character="Δ"),
            ]
        )

    async with AsyncClient(app=app, base_url="http://example.com") as ac:
        response = await ac.get("/db-integration/delta/")

    assert response.json() == {
        "name": "delta",
        "character": "Δ",
    }
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.database
async def test_get_detail_for_nonexistant(session):
    async with AsyncClient(app=app, base_url="http://example.com") as ac:
        response = await ac.get("/db-integration/kappa/")

    assert response.json() == {
        "detail": "kappa not found",
    }
    assert response.status_code == 404
