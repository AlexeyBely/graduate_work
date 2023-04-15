from pydantic import BaseSettings, Field, root_validator


class EnvSettings(BaseSettings):
    secret_key: str = Field('django-insecure-', env='admin_billing_dj_secret_key')
    debug: bool = Field(True, env='admin_billing_debug')
    psql_name: str = Field('billing_database', env='billing_postgres_db')
    psql_user: str = Field('app', env='billing_postgres_name')
    psql_password: str = Field('123qwe', env='billing_postgres_password')
    psql_port: int = Field(5432, env='billing_postgres_port')
    psql_host: str = Field('127.0.0.1', env='billing_postgres_host')  
    admin_timezone: str = 'Europe/Moscow'
    auth_grpc_port: int = 50051
    auth_grpc_host: str = '127.0.0.1'


env_settings = EnvSettings()
