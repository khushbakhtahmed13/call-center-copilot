from pydantic import BaseModel

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