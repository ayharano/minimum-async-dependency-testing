import io
from unittest.mock import patch

from fastapi import APIRouter
from httpx import AsyncClient
from starlette import status
from starlette.responses import JSONResponse

from mve_app.main import app

middleware_testing_router = APIRouter(prefix="/test-middleware")


@middleware_testing_router.get("/")
async def get_root():
    return JSONResponse("ok", status_code=status.HTTP_200_OK)


app.include_router(middleware_testing_router)


@patch("sys.stdout", new_callable=io.StringIO)
async def test_SomeAsyncMiddleware_dispatch(mock_stdout):
    async with AsyncClient(app=app, base_url="http://example.com") as ac:
        response = await ac.get("/test-middleware/")

    assert response.json() == "ok"
    assert response.status_code == 200

    assert mock_stdout.getvalue() == "line from async middleware\n"
