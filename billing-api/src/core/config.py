from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field


logging_config.dictConfig(LOGGING)


class ApiSettings(BaseSettings):
    project_name: str = 'Movies billing'    
    psql_name: str = Field('billing_database', env='billing_postgres_db')
    psql_user: str = Field('app', env='billing_postgres_name')
    psql_password: str = Field('123qwe', env='billing_postgres_password')
    psql_port: int = Field(5432, env='billing_postgres_port')
    psql_host: str = Field('127.0.0.1', env='billing_postgres_host')
    access_token_secret_key: str = '256-bit-secret-key-1'
    token_algoritm: str = 'HS256'
    payment_currency: str = 'usd'
    payment_success_url: str = 'https://ya.ru/'
    payment_smallest_currency: int = 100
    payment_hours_refund: int = 1
    stripe_api_key: str = 'sk_test_51MmcI4EDsXu7ZV5DF1l10mZuZC5iGb8W41FrYxXXgMzbS5lQ1w34alOaCNAInpHzHcnIc7hXhabNh8HqlafoCM3O002ye80K06'
    stripe_id_product: str = 'prod_NaetpznQ9m7dyF'
    auth_grpc_port: int = 50051
    auth_grpc_host: str = '127.0.0.1'
    rabbitmq_default_user: str = 'guest'
    rabbitmq_default_pass: str = 'guest'
    rabbitmq_default_vhost: str = ''
    billing_rabbitmq_host: str = '127.0.0.1'
    billing_rabbitmq_port: int = 5672


settings = ApiSettings()
