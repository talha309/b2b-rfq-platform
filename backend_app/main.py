from fastapi import FastAPI
<<<<<<< HEAD
from backend_app.api.v1 import chat, rfq, customer, factory
from backend_app.db.base import Base
from backend_app.db.session import engine
=======
from app.api.v1 import chat, rfq
from app.db.base import Base
from app.db.session import engine
>>>>>>> 251535d81599a3c8027c686bd2947fd0a43f4133

app = FastAPI(title="B2B RFQ Platform", version="0.1.0")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
<<<<<<< HEAD
app.include_router(rfq.router, prefix="/v1/rfq", tags=["rfq"])
app.include_router(customer.router, prefix="/v1/customer", tags=["customer"])
app.include_router(factory.router, prefix="/v1/factory", tags=["factory"])
=======
app.include_router(rfq.router, prefix="/v1/rfq", tags=["rfq"])
>>>>>>> 251535d81599a3c8027c686bd2947fd0a43f4133
