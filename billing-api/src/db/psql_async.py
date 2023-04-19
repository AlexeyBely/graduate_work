from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool

from core.config import settings

sqlalchemy_asyncpg_url = 'postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
    settings.psql_user,
    settings.psql_password,
    settings.psql_host,
    settings.psql_port,
    settings.psql_name,
)


engine_psql_async = create_async_engine(
    sqlalchemy_asyncpg_url,
    future=True,
    poolclass=NullPool,
    echo=False
)

session_psql_async = async_sessionmaker(
    engine_psql_async,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()
