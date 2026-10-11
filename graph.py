# graph.py
from states import LoanState
from langgraph.graph import StateGraph, START, END
from nodes import (
    check_documents,
    check_credit,
    check_income_and_debt,
    decide,
    request_documents,
    human_review,
)
from router import route_after_decision
from langgraph.checkpoint.memory import InMemorySaver

builder = StateGraph(LoanState)

builder.add_node("check_documents", check_documents)
builder.add_node("check_credit", check_credit)
builder.add_node("check_income_and_debt", check_income_and_debt)
builder.add_node("decide", decide)
builder.add_node("request_documents", request_documents)
builder.add_node("human_review", human_review)

builder.add_edge(START, "check_documents")
builder.add_edge("check_documents", "check_credit")
builder.add_edge("check_credit", "check_income_and_debt")
builder.add_edge("check_income_and_debt", "decide")
builder.add_conditional_edges("decide", route_after_decision)
builder.add_edge("request_documents", END)
builder.add_edge("human_review", END)

graph = builder.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":

    config = {"configurable": {"thread_id": "APP-001"}}

    human_review_data = {
        "credit_score": 670,
        "income": 100000.0,
        "existing_debt": 20000.0,
        "loan_amount": 50000.0,
        "documents": ["income_proof", "bank_statement", "id_proof"],
    }

    result = graph.invoke(human_review_data, config)

    saved = graph.get_state(config)
    print(saved.values["decision"])
    print(saved.next)
