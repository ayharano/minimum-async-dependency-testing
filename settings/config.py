from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    All the variables in the respective environment file should be declared here
    including the type and an optional default value.
    """

    ENVIRONMENT: str = "mve"

    # testing-related settings
    INITIALIZE_TEST_DATABASE: bool = False

    # database-related
    # defaulting to an unusable string to force the use of a well-defined ENVIRONMENT.env file
    DATABASE_URL: str = ""
    DATABASE_DB: str = ""


@lru_cache()
def get_settings() -> Settings:
    app_settings = Settings()
    return Settings(  # type: ignore[call-arg]
        _env_file=f"settings/{app_settings.ENVIRONMENT}.env", _env_file_encoding="utf-8"
    )


settings: Settings = get_settings()
