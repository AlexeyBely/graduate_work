from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)


class ApiSettings(BaseSettings):
    project_name: str = 'Movies billing'    
    #psql_name: str = Field('modify_database', env='notify_postgres_db')
    #psql_user: str = Field('app', env='notify_postgres_name')
    #psql_password: str = Field('123qwe', env='notify_postgres_password')
    #psql_port: int = Field(5432, env='notify_postgres_port')
    #psql_host: str = Field('127.0.0.1', env='notify_postgres_host')
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'
    payment_currency: str = 'usd'
    payment_success_url: str = 'https://ya.ru/'
    stripe_api_key: str = 'sk_test_51MmcI4EDsXu7ZV5DF1l10mZuZC5iGb8W41FrYxXXgMzbS5lQ1w34alOaCNAInpHzHcnIc7hXhabNh8HqlafoCM3O002ye80K06'
    stripe_smallest_currency: float = 0.01
    stripe_id_product: str = 'prod_NaetpznQ9m7dyF'


settings = ApiSettings()