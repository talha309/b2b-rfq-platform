# Admin Routes — 6 routes
# GET /rfqs → View all RFQs
# PUT /rfq/{id} → Edit/update RFQ details
# POST /rfq/{id}/assign → Assign RFQ to specific factory
# GET /factories → Manage factories (list, add, or remove)
# GET /analytics → View analytics dashboard (trends, demand, etc.)
# POST /quotation/finalize → Send final quotation to customer
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.data_base import get_db
from models.models import RFQ, Factory, Quotation
from utils.schemas import RFQUpdate, AssignFactory, FinalQuotation
from utils.deps import admin_required

router = APIRouter(prefix="/admin", tags=["Admin"])

# 1) GET /admin/rfqs → View all RFQs
@router.get("/rfqs")
def get_rfqs(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(RFQ).all()


# 2) PUT /admin/rfq/{id} → Update RFQ details
@router.put("/rfq/{id}")
def update_rfq(id: int, data: RFQUpdate, db: Session = Depends(get_db), admin=Depends(admin_required)):
    rfq = db.query(RFQ).filter(RFQ.id == id).first()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
    
    for field, value in data.dict(exclude_unset=True).items():
        setattr(rfq, field, value)

    db.commit()
    db.refresh(rfq)
    return {"message": "RFQ updated successfully", "rfq": rfq}


# 3) POST /admin/rfq/{id}/assign → Assign RFQ to factory
@router.post("/rfq/{id}/assign")
def assign_factory(id: int, data: AssignFactory, db: Session = Depends(get_db), admin=Depends(admin_required)):
    rfq = db.query(RFQ).filter(RFQ.id == id).first()
    factory = db.query(Factory).filter(Factory.id == data.factory_id).first()
    if not rfq:
        raise HTTPException(status_code=404, detail="RFQ not found")
    if not factory:
        raise HTTPException(status_code=404, detail="Factory not found")

    rfq.factory_id = data.factory_id
    rfq.status = "assigned"
    db.commit()
    return {"message": "Factory assigned successfully", "rfq_id": id, "factory_id": data.factory_id}


# 4) GET /admin/factories → List all factories
@router.get("/factories")
def get_factories(db: Session = Depends(get_db), admin=Depends(admin_required)):
    return db.query(Factory).all()


# 5) GET /admin/analytics → (Simple Example Analytics)
@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), admin=Depends(admin_required)):
    total_rfqs = db.query(RFQ).count()
    total_factories = db.query(Factory).count()
    total_quotations = db.query(Quotation).count()

    return {
        "total_rfqs": total_rfqs,
        "total_factories": total_factories,
        "total_quotations": total_quotations
    }


# 6) POST /admin/quotation/finalize → Create/Send Final Quotation
@router.post("/quotation/finalize")
def finalize_quotation(data: FinalQuotation, db: Session = Depends(get_db), admin=Depends(admin_required)):
    quotation = Quotation(**data.dict())
    db.add(quotation)
    db.commit()
    db.refresh(quotation)
    return {"message": "Quotation finalized and sent to customer", "quotation": quotation}
