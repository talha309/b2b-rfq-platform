from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.graph.flows.chat_to_rfq import chat_to_rfq_flow
from app.api.v1.rfq import create_draft
from app.db.session import get_db

router = APIRouter()

class ChatMessage(BaseModel):
    content: str
    session_id: str

@router.post("/")
async def chat(msg: ChatMessage, db=Depends(get_db)):
    # In real app: load session history from DB
    initial_state = {
        "messages": [{"role": "user", "content": msg.content}],
        "collected": {},
        "rfq_ready": False,
        "rfq_data": None
    }

    result = chat_to_rfq_flow.invoke(initial_state)

    if result.get("rfq_ready"):
        rfq_in = RFQCreate(**result["rfq_data"])
        rfq = create_draft(rfq_in, db)
        return {"response": "RFQ created!", "rfq_id": rfq.id}

    return {"response": result["messages"][-1].content}