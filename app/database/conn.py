import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.common.config import LocalConfig
from app.core.settings.setting import AppSettings, get_env


class SQLAlchemy:
    database_url = None

    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(
            self,
            app=None,
            env_const: AppSettings = get_env(),
            **kwargs
    ) -> None:
        config = LocalConfig()

        database_url = f'mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}/' \
                       f'{config.DB_SCHEMA}?charset={config.DB_CHARSET}'

        self._engine = create_engine(
            database_url,
            # echo=config.DB_ECHO,
            echo=False,
            pool_recycle=config.DB_POOL_RECYCLE,
            pool_pre_ping=True
        )
        self._session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine
        )

        @app.on_event('startup')
        def startup():
            self._engine.connect()
            logging.info("DB Connected")

        @app.on_event('shutdown')
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB Disconnected")

    def get_db(self):
        if self._session is None:
            raise Exception("Must be Called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
