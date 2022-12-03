import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"

    MONGO_DB: str = os.getenv("MONGO_DB")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    MONGO_USER: str = os.getenv("MONGO_USER")
    MONGO_HOST: str = os.getenv("MONGO_HOST")
    MONGO_PORT: str = os.getenv("MONGO_PORT")

    MONGO_SERVER_SELECTION_TIMEOUT_MS: os.getenv("MONGO_SERVER_SELECTION_TIMEOUT_MS")

    MONGO_URI: str = "mongodb://{user}:{password}@{host}:{port}/{database}".format(
        host=MONGO_HOST,
        port=MONGO_PORT,
        user=MONGO_USER,
        password=MONGO_PASSWORD,
        database=MONGO_DB,
    )

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


settings = Settings()
