import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    POSTGRES_URI: str = (
        "postgresql://{user}:{password}@{host}:{port}/{database}".format(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB"),
        )
    )


settings = Settings()
