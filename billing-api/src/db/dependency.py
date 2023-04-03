from db.postgresql import session_psql
from db import psql_async


def get_db():
    db = session_psql()
    try:
        yield db
    finally:
        db.close()


def get_db_async():
    db = psql_async.session_psql_async()
    try:
        yield db
    finally:
        db.close()
