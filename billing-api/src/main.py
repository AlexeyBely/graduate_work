from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.v1 import payment, offer, marketing
from core.config import settings
from db import psql_async


app = FastAPI(
    title=f'Сервис {settings.project_name}',
    docs_url='/billing/api/openapi',
    openapi_url='/billing/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис выставления счетов',
    version='1.0.1',
)


@app.on_event('startup')
async def startup():
    psql_async.engine_psql_async = create_async_engine(psql_async.sqlalchemy_asyncpg_url,
                                                       echo=True)
    psql_async.session_psql_async = sessionmaker(psql_async.engine_psql_async,
                                                 expire_on_commit=False,
                                                 class_=AsyncSession)


@app.on_event('shutdown')
async def shutdown():
    await psql_async.engine_psql_async.dispose()


app.include_router(payment.router, prefix='/billing/api/v1/payment', tags=['payment'])
app.include_router(offer.router, prefix='/billing/api/v1/offer', tags=['offer'])
app.include_router(marketing.router, prefix='/billing/api/v1/marketing', tags=['marketing'])


import uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8999)