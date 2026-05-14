from pydantic import BaseModel
from typing import List

class CallSummary(BaseModel):
    customer_issue : str
    sentiment : str
    resolution_status : str
    follow_up_needed : bool

class SentimentAnalysis(BaseModel):
    overall_sentiment: str
    start_sentiment: str
    end_sentiment: str
    escalation_risk: str

class ComplianceAnalysis(BaseModel):
    identity_verified: bool
    empathy_shown: bool
    escalation_needed: bool
    escalation_handled_correctly: bool
    refund_policy_followed: bool
    compliance_issues: List[str]
    overall_compliance: str