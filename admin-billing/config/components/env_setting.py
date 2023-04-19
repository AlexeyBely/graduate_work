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
    admin_allowed_hosts: str = '127.0.0.1'
    allowed_hosts_parse: list[str] | None = None
    admin_csrf_trusted: str = 'http://127.0.0.1:8000'
    csrf_trusted_parse: list[str] | None = None

    @root_validator
    def parse_env_var(cls, values):
        val = values['admin_allowed_hosts']
        values['allowed_hosts_parse'] = [v for v in val.split(', ')]
        val = values['admin_csrf_trusted']
        values['csrf_trusted_parse'] = [v for v in val.split(', ')]
        return values

env_settings = EnvSettings()
