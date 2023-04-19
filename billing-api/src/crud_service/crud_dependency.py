from functools import lru_cache

from crud_service.crud_billing_sql import SqlCrudBilling
from crud_service.read_marketing_sql import SqlReadMarketing
from db.psql_async import session_psql_async


@lru_cache()
def get_crud_marketing() -> SqlReadMarketing:
    return SqlReadMarketing(session_psql_async)


@lru_cache()
def get_crud_billing() -> SqlCrudBilling:
    return SqlCrudBilling(session_psql_async)
