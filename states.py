# states.py
import operator
from typing import Annotated, Literal, TypedDict

Decision = Literal["APPROVED", "REJECTED", "MANUAL_REVIEW", "MORE_INFO_REQUIRED"]
Verdict = Literal["PASS", "FAIL", "MORE_INFO", "REVIEW"]

class CheckResult(TypedDict):
    check:str
    verdict: Verdict
    reasons: list[str]

class LoanState(TypedDict):
    credit_score: int
    income: float
    existing_debt: float
    loan_amount: float
    documents: list[str]
    missing_documents: list[str]
    decision: Decision
    check_results: Annotated[list[CheckResult], operator.add]
    message:str

