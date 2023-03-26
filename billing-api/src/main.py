from api.v1 import payment
from core.config import settings

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse


app = FastAPI(
    title=f'Сервис {settings.project_name}',
    docs_url='/billing/api/openapi',
    openapi_url='/billing/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Сервис выставления счетов',
    version='1.0.1',
)

app.include_router(payment.router, prefix='/billing/api/v1', tags=['test'])


import uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8999)