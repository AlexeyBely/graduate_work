from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Session

from core.config import settings


sqlalchemy_asyncpg_url = 'postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}'.format(
    settings.psql_user,
    settings.psql_password,
    settings.psql_host,
    settings.psql_port,
    settings.psql_name,
)


engine_psql_async: AsyncEngine
session_psql_async: Session
