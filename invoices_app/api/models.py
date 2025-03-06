from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class Invoice(BaseModel):
    nip: str
    seller_name: str
    address: str
    number: str
    date: datetime
    gross: Decimal
    vat_rate: Decimal
    net: Decimal
    vat: Decimal
    user_id: str

    class Config:
        alias_generator = to_camel
        populate_by_name = True
