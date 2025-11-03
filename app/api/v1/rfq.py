from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.rfq import RFQ
from app.schemas.rfq import RFQCreate, RFQOut

router = APIRouter()

@router.post("/draft", response_model=RFQOut)
def create_draft(rfq_in: RFQCreate, db: Session = Depends(get_db)):
    rfq = RFQ(**rfq_in.dict(), status="draft")
    db.add(rfq)
    db.commit()
    db.refresh(rfq)
    return rfq