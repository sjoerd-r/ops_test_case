from typing import Optional
from sqlmodel import SQLModel

class LocationAddress(SQLModel, table=False):
    address1: Optional[str] = None
    address2: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    province_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None