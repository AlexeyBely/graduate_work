from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from crud_service.read_marketing_sql import SqlReadMarketing
from crud_service.crud_billing_sql import SqlCrudBilling
from db.psql_async import session_psql_async


@lru_cache()
def get_crud_marketing() -> SqlReadMarketing:
    return SqlReadMarketing(session_psql_async)


@lru_cache()
def get_crud_billing() -> SqlCrudBilling:
    return SqlCrudBilling(session_psql_async)
