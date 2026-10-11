# nodes.py
from states import LoanState
from llm import llm

REQUIRED_DOCUMENTS = ["income_proof", "bank_statement", "id_proof"]

FALLBACK_MESSAGES = {
    "APPROVED": "Your home loan application has been approved.",
    "REJECTED": "We are unable to approve your home loan application at this time.",
}

MIN_CREDIT_SCORE = 600
GOOD_CREDIT_SCORE = 700
MIN_INCOME = 30000


def check_documents(state: LoanState) -> dict:

    missing_documents = [x for x in REQUIRED_DOCUMENTS if x not in state["documents"]]

    if missing_documents:
        reason = "Missing documents: " + ", ".join(missing_documents)
        verdict = "MORE_INFO"
    else:
        reason = "All documents clear"
        verdict = "PASS"

    return {
        "missing_documents": missing_documents,
        "check_results": [
            {
                "check": "documents",
                "verdict": verdict,
                "reasons": [reason],
            }
        ],
    }


def check_credit(state: LoanState) -> dict:
    credit_score = state["credit_score"]
    if credit_score < MIN_CREDIT_SCORE:
        reason = f"Credit score {credit_score} is below {MIN_CREDIT_SCORE}"
        verdict = "FAIL"
    elif credit_score < GOOD_CREDIT_SCORE:
        reason = f"Credit score {credit_score} is fair"
        verdict = "REVIEW"
    else:
        reason = f"Credit score {credit_score} is good"
        verdict = "PASS"

    return {
        "check_results": [{"check": "credit", "verdict": verdict, "reasons": [reason]}]
    }


def check_income_and_debt(state: LoanState) -> dict:
    income = state["income"]
    existing_debt = state["existing_debt"]
    loan_amount = state["loan_amount"]
    reasons = []

    verdict = "FAIL"

    if income < MIN_INCOME:
        reasons.append(f"Income {income} is less than minimum income {MIN_INCOME}")

    if existing_debt > income / 2:
        reasons.append(f"Existing debt {existing_debt} is more than 50% of {income}")

    if loan_amount > (income * 5):
        reasons.append(f"Loan amount {loan_amount} is 5x than income {income}")

    if not reasons:
        reasons.append("Income and debt are acceptable")
        verdict = "PASS"

    return {
        "check_results": [{"check": "income", "verdict": verdict, "reasons": reasons}]
    }


def decide(state: LoanState) -> dict:

    verdict = [r["verdict"] for r in state["check_results"]]

    if "FAIL" in verdict:
        return {"decision": "REJECTED", "message": "Loan rejected"}
    if "MORE_INFO" in verdict:
        return {"decision": "MORE_INFO_REQUIRED"}
    if "REVIEW" in verdict:
        return {"decision": "MANUAL_REVIEW"}

    return {"decision": "APPROVED", "message": "Loan approved"}


def request_documents(state: LoanState) -> dict:
    missing_docs = ", ".join(state["missing_documents"])
    message = f"Please upload: {missing_docs}"
    return {"message": message}


def human_review(state: LoanState) -> dict:
    return {"message": "Sent to loan reviewer department"}


def explain_decision(state: LoanState) -> dict:
    decision = state["decision"]
    prompt = f"""
    You are a home loan assistant at a bank.
    Write a short, polite message to the applicant.

    Decision: {decision}
    Findings: {state["check_results"]}

    Rules:
    - Do not change or question the decision.
    - Do not promise anything.
    - Maximum 3 sentences.
    - Provide the exact reason for which the loan was rejected, which you will get in the Findings section
    - Format the answer in short sentences and provide emojis
    """
    try:
        result = llm().invoke(prompt)
        message_to_customer = result.content
    except:
        message_to_customer = FALLBACK_MESSAGES[decision]

    return {"message": message_to_customer}
