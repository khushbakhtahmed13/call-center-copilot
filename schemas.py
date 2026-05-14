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

class AgentPerformance(BaseModel):
    professionalism_score: int
    empathy_score: int
    communication_clarity_score: int
    resolution_effectiveness_score: int
    policy_adherence_score: int
    overall_score: int
    strengths: list[str]
    improvement_areas: list[str]

class RiskDetection(BaseModel):
    customer_churn_risk: str
    escalation_risk: str
    fraud_risk: str
    reputational_risk: str
    operational_risk: str
    urgent_follow_up_required: bool
    detected_risk_factors: List[str]
    recommended_actions: List[str]
    overall_risk_level: str