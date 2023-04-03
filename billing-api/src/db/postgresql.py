from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings


sqlalchemy_database_url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    settings.psql_user,
    settings.psql_password,
    settings.psql_host,
    settings.psql_port,
    settings.psql_name,
)
engine_psql = create_engine(sqlalchemy_database_url)
session_psql = sessionmaker(autocommit=False, autoflush=False, bind=engine_psql)


Base = declarative_base()
