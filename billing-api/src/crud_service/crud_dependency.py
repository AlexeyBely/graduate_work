from functools import lru_cache
from fastapi import Depends
from sqlalchemy.orm import Session

from crud_service.read_marketing_sql import SqlReadMarketing
from db.dependency import get_db_async


@lru_cache()
def get_crud_marketing(session: Session = Depends(get_db_async)) -> SqlReadMarketing:
    return SqlReadMarketing(session)
