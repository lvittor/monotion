import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.settings import settings


class PostgresClient:
    log: logging.Logger = logging.getLogger(__name__)

    @classmethod
    def get_session(cls):
        """Return a Postgres session"""
        cls.log.info(
            f"POSTGRES_URI={settings.POSTGRES_URI}"
        )  # TODO: logger not working
        SessionLocal = sessionmaker(
            autocommit=True, autoflush=False, bind=create_engine(settings.POSTGRES_URI)
        )
        return SessionLocal()

    @classmethod
    def get_client(cls):
        """Yield an auto-clossing Postgres session"""
        session = cls.get_session()
        try:
            yield session
        finally:
            session.close()

    @classmethod
    async def ping(cls):
        try:
            session = cls.get_session()
            session.execute("SELECT 1")
        except SQLAlchemyError as e:
            cls.log.exception(e)
            return False
        return True
