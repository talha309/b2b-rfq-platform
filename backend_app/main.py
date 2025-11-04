from fastapi import FastAPI
from app.api.v1 import chat, rfq
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title="B2B RFQ Platform", version="0.1.0")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/v1/chat", tags=["chat"])
app.include_router(rfq.router, prefix="/v1/rfq", tags=["rfq"])