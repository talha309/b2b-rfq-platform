from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# -------------------- USER SCHEMAS --------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# -------------------- TOKEN SCHEMA --------------------
class Token(BaseModel):
    access_token: str
    token_type: str


# -------------------- FACTORY SCHEMAS --------------------
class FactoryBase(BaseModel):
    name: str
    country: str
    contact_email: EmailStr


class FactoryCreate(FactoryBase):
    pass


class FactoryOut(FactoryBase):
    id: int

    class Config:
        from_attributes = True


# -------------------- PRODUCT SCHEMAS --------------------
class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    min_order_quantity: int
    price_range: Optional[str]


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True


# -------------------- RFQ SCHEMAS --------------------
class RFQBase(BaseModel):
    product_name: str
    specifications: Optional[str]
    quantity: int
    destination_country: Optional[str]


class RFQCreate(RFQBase):
    pass  # created directly by customer


class RFQOut(RFQBase):
    id: int
    status: str
    customer_id: int
    factory_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# -------------------- QUOTATION SCHEMAS --------------------
class QuotationBase(BaseModel):
    price_per_unit: float
    total_price: float
    currency: Optional[str] = "USD"
    notes: Optional[str]


class QuotationCreate(QuotationBase):
    rfq_id: int
    factory_id: int


class QuotationOut(QuotationBase):
    id: int
    created_at: datetime
    rfq_id: int
    factory_id: int

    class Config:
        from_attributes = True


# -------------------- ORDER SCHEMAS --------------------
class OrderBase(BaseModel):
    status: Optional[str] = "processing"


class OrderCreate(OrderBase):
    quotation_id: int
    customer_id: int


class OrderOut(OrderBase):
    id: int
    quotation_id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# utils/schemas.py

class RFQUpdate(BaseModel):
    product_name: str | None = None
    specifications: str | None = None
    quantity: int | None = None
    destination_country: str | None = None
    status: str | None = None

class AssignFactory(BaseModel):
    factory_id: int

class FinalQuotation(BaseModel):
    rfq_id: int
    factory_id: int
    price_per_unit: float
    total_price: float
    currency: str = "USD"
    notes: str | None = None
