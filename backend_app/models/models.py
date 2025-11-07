from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from database.data_base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="customer")  # customer | admin | factory_user

    # Relationships
    rfqs = relationship("RFQ", back_populates="customer")
    orders = relationship("Order", back_populates="customer")


class Factory(Base):
    __tablename__ = "factories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    contact_email = Column(String, unique=True, nullable=False)

    # Relationships
    rfqs = relationship("RFQ", back_populates="factory")
    quotations = relationship("Quotation", back_populates="factory")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    min_order_quantity = Column(Integer, nullable=False)
    price_range = Column(String)  # Example: "$1 - $3 per unit"

    # No direct relationship required now (Products mostly used for display)


class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    specifications = Column(String)
    quantity = Column(Integer, nullable=False)
    destination_country = Column(String)
    status = Column(String, default="pending")  # pending | assigned | quoted | closed

    customer_id = Column(Integer, ForeignKey("users.id"))
    factory_id = Column(Integer, ForeignKey("factories.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("User", back_populates="rfqs")
    factory = relationship("Factory", back_populates="rfqs")
    quotations = relationship("Quotation", back_populates="rfq")


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"))
    factory_id = Column(Integer, ForeignKey("factories.id"))

    price_per_unit = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    notes = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    rfq = relationship("RFQ", back_populates="quotations")
    factory = relationship("Factory", back_populates="quotations")
    order = relationship("Order", back_populates="quotation", uselist=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String, default="processing")  # processing | shipped | completed | canceled
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    quotation = relationship("Quotation", back_populates="order")
    customer = relationship("User", back_populates="orders")
