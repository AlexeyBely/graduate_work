from pydantic import BaseModel, Field, UUID4
from fastapi import Query

from core.config import settings


class TestStripe(BaseModel):
    amount: float = 12

