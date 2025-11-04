from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from app.db.base import Base
from datetime import datetime
import enum

class RFQStatus(str, enum.Enum):
    draft = "draft"
    review = "review"
    approved = "approved"
    sent_to_factory = "sent_to_factory"
    quoted = "quoted"
    customer_sent = "customer_sent"
    accepted = "accepted"
    rejected = "rejected"

class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    product_spec = Column(String)
    quantity = Column(Integer)
    destination_country = Column(String)
    customer_email = Column(String, index=True)
    customer_name = Column(String, nullable=True)
    collected_data = Column(JSON, nullable=True)
    status = Column(Enum(RFQStatus), default=RFQStatus.draft)
    factory_id = Column(Integer, nullable=True)
    factory_quote = Column(JSON, nullable=True)
    final_quote = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)