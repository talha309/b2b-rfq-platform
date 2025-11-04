from typing import TypedDict, List, Dict, Optional
from langchain_core.messages import BaseMessage

class ChatState(TypedDict):
    messages: List[BaseMessage]
    collected: Dict[str, str]
    rfq_ready: bool
    rfq_data: Optional[Dict]