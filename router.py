# router.py
from states import LoanState
from langgraph.graph import END

def route_after_decision(state: LoanState) -> str:
    
    next_node = END

    if state['decision'] == "MANUAL_REVIEW":
        next_node = "human_review"
    if state["decision"] == "MORE_INFO_REQUIRED":
        next_node = "request_documents"

    return next_node
