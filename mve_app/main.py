from fastapi import FastAPI

from mve_app import routers
from mve_app.middlewares import SomeAsyncMiddleware


app = FastAPI()

app.add_middleware(SomeAsyncMiddleware)

app.include_router(routers.dummy_router)
