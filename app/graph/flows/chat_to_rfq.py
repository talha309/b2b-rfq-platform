from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from app.schemas.rfq import RFQCreate
import json

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def extract_rfq_data(state):
    prompt = """
    Extract from conversation:
    - product_spec
    - quantity
    - destination_country
    - customer_email
    - customer_name (optional)

    Return JSON. If missing, respond naturally and ask.
    """
    messages = [m.content if isinstance(m, (HumanMessage, AIMessage)) else str(m) for m in state["messages"]]
    result = llm.invoke(prompt + "\n\nConversation:\n" + "\n".join(messages))
    try:
        data = json.loads(result.content)
        return {
            "collected": data,
            "rfq_ready": all(k in data for k in ["product_spec", "quantity", "destination_country", "customer_email"]),
            "rfq_data": data
        }
    except:
        return {"messages": state["messages"] + [AIMessage(content=result.content)]}

graph = StateGraph(ChatState)
graph.add_node("extract", extract_rfq_data)
graph.add_edge(START, "extract")
graph.add_conditional_edges(
    "extract",
    lambda s: "done" if s.get("rfq_ready") else "continue",
    {"done": END, "continue": "extract"}
)
chat_to_rfq_flow = graph.compile()