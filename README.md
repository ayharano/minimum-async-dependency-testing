# Minimum async dependency testing

This repo was created as a Minimum Viable Example (MVE) for a particular [issue](https://github.com/tiangolo/fastapi/issues/4719)/[discussion](https://github.com/tiangolo/fastapi/discussions/8443) from [the FastAPI repository](https://github.com/tiangolo/fastapi).

As the goal is to validate the testing of async SQLAlchemy models during FastAPI async dependency injection, this repo uses aiosqlite to not require any external database configuration.

# Python version
3.10+

# Required packages

- [aiosqlite](https://github.com/omnilib/aiosqlite)
- [fastapi](https://github.com/tiangolo/fastapi)
- [httpx](https://github.com/encode/httpx/)
- [pydantic](https://github.com/pydantic/pydantic)
- [pytest](https://github.com/pytest-dev/pytest)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)
- [starlette](https://github.com/encode/starlette)

# Installation

```shell
PIP_REQUIRE_VIRTUALENV=1 pip install -U pip
PIP_REQUIRE_VIRTUALENV=1 pip install -r requirements.txt
```

# Running the tests

```shell
ENVIRONMENT=mve pytest tests/
```
