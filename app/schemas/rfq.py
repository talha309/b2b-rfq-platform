from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class RFQCreate(BaseModel):
    product_spec: str
    quantity: int
    destination_country: str
    customer_email: EmailStr
    customer_name: Optional[str] = None

class RFQOut(RFQCreate):
    id: int
    status: str
    created_at: datetime
    factory_id: Optional[int] = None

    class Config:
        from_attributes = True