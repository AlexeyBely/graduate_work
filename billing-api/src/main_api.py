from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from api.v1 import payment, marketing
from core.config import settings
from db import psql_async


app = FastAPI(
    title=f'{settings.project_name} service',
    docs_url='/billing/api/openapi',
    openapi_url='/billing/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Offer calculation and subscription billing',
    version='1.0.1',
)


@app.on_event('startup')
async def startup():
    pass


@app.on_event('shutdown')
async def shutdown():
    await psql_async.engine_psql_async.dispose()


app.include_router(payment.router, prefix='/billing/api/v1/payment', tags=['payment'])
app.include_router(marketing.router, prefix='/billing/api/v1/marketing', tags=['marketing'])


import uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8999)