from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from prompts import SUMMARY_PROMPT, SENTIMENT_PROMPT, COMPLIANCE_PROMPT, AGENT_PERFORMANCE_PROMPT, RISK_DETECTION_PROMPT
from schemas import CallSummary, SentimentAnalysis, ComplianceAnalysis, AgentPerformance, RiskDetection
from config import retriever
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# State
class CallState(TypedDict):
    transcript : str
    summary : Optional[CallSummary]
    sentiment_analysis : Optional[SentimentAnalysis]
    compliance_analysis : Optional[ComplianceAnalysis]
    agent_performance : Optional[AgentPerformance]
    risk_detection : Optional[RiskDetection]


# Model 
llm = ChatGroq(
      model = "llama-3.3-70b-versatile",
      temperature = 0,
      api_key = GROQ_API_KEY
)

# Node functions

def call_summary(state : CallState):
    structured_llm = llm.with_structured_output(CallSummary)
    response = structured_llm.invoke(SUMMARY_PROMPT.format(conversation = state.get("transcript")))
    
    return {
        "summary" : response
    }

def sentiment_analysis(state : CallState):
    structured_llm = llm.with_structured_output(SentimentAnalysis)
    response = structured_llm.invoke(SENTIMENT_PROMPT.format(conversation = state.get("transcript")))

    return {
        "sentiment_analysis" : response
    }

def compliance_analysis(state : CallState):
    # Retrieval 
    query = f"""
Analyze policies related to:
- refunds
- disputes
- identity verification
- escalation procedures

Conversation:
{state.get("transcript")}
"""
    retrieved_docs = retriever.invoke(query)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    structured_llm = llm.with_structured_output(ComplianceAnalysis)
    response = structured_llm.invoke(COMPLIANCE_PROMPT.format(conversation = state.get("transcript"), policies = context))
    
    return {
        "compliance_analysis" : response 
    }

def agent_performance(state : CallState):
    structured_llm = llm.with_structured_output(AgentPerformance)
    response = structured_llm.invoke(AGENT_PERFORMANCE_PROMPT.format(conversation = state.get("transcript"), sentiment_analysis = state.get("sentiment_analysis"), compliance_analysis = state.get("compliance_analysis")))

    return {
        "agent_performance" : response
    }

def risk_detection(state : CallState):
    structured_llm = llm.with_structured_output(RiskDetection)
    response = structured_llm.invoke(RISK_DETECTION_PROMPT.format(conversation = state.get("transcript"), sentiment_analysis = state.get("sentiment_analysis"), compliance_analysis = state.get("compliance_analysis"), agent_performance_analysis = state.get("agent_performance")))

    return {
        "risk_detection" : response
    }

# Build Graph

# Graph
graph = StateGraph(CallState)

# Nodes
graph.add_node("call_summarizer", call_summary)
graph.add_node("sentiment_analyzer", sentiment_analysis)
graph.add_node("compliance_analyzer", compliance_analysis)
graph.add_node("agent_performance_analyzer", agent_performance)
graph.add_node("risk_detector", risk_detection)

# Entry point
graph.set_entry_point("call_summarizer")

# Edges
graph.add_edge("call_summarizer", "sentiment_analyzer")
graph.add_edge("sentiment_analyzer", "compliance_analyzer")
graph.add_edge("compliance_analyzer", "agent_performance_analyzer")
graph.add_edge("agent_performance_analyzer", "risk_detector")
graph.add_edge("risk_detector", END)

# Compile Graph
app = graph.compile()

if __name__ == "__main__":
    final_transcript =  [
    {"speaker": "SPEAKER_00", "start": 0.0, "end": 2.3, "text": "Thank you for calling Horizon National Bank."},
    {"speaker": "SPEAKER_00", "start": 2.3, "end": 3.8, "text": "My name is Sarah."},
    {"speaker": "SPEAKER_00", "start": 3.8, "end": 7.9, "text": "This call may be recorded for quality and security purposes."},
    {"speaker": "SPEAKER_00", "start": 7.9, "end": 9.9, "text": "How may I assist you today?"},
    {"speaker": "SPEAKER_01", "start": 9.9, "end": 11.0, "text": "Yeah, hi."},
    {"speaker": "SPEAKER_01", "start": 11.0, "end": 18.5, "text": "I'm calling because I noticed I was charged twice for the same Uber transaction yesterday. And honestly, this is getting really frustrating."},
    {"speaker": "SPEAKER_00", "start": 18.5, "end": 25.9, "text": "I'm sorry to hear that. I'll definitely look into it for you. Before we begin, may I verify your full name?"},
    {"speaker": "SPEAKER_01", "start": 25.9, "end": 27.6, "text": "Daniel Ahmed."},
    {"speaker": "SPEAKER_00", "start": 27.6, "end": 33.1, "text": "Thank you, Mr. Ahmed. And can you confirm the last four digits of your debit card?"},
    {"speaker": "SPEAKER_01", "start": 33.1, "end": 35.7, "text": "4,821."},
    {"speaker": "SPEAKER_00", "start": 35.7, "end": 41.4, "text": "Great. For security purposes, can you also confirm your billing zip code?"},
    {"speaker": "SPEAKER_01", "start": 41.4, "end": 43.3, "text": "44,000."},
    {"speaker": "SPEAKER_00", "start": 43.3, "end": 52.8, "text": "Perfect. Thank you. I've pulled up your account. You mentioned a duplicate Uber transaction. Do you know the amount that was charged?"},
    {"speaker": "SPEAKER_01", "start": 52.8, "end": 59.9, "text": "Yes, it was around $43 in some change. I got charged once in the afternoon and then again late at night."},
    {"speaker": "SPEAKER_00", "start": 59.9, "end": 65.0, "text": "Understood. Give me just a moment while I review the transaction history."},
    {"speaker": "SPEAKER_01", "start": 65.0, "end": 66.3, "text": "Sure."},
    {"speaker": "SPEAKER_00", "start": 66.3, "end": 79.4, "text": "Thank you for waiting. I can see two charges from Uber for $43.72 posted approximately six hours apart. One appears completed and the other is currently pending."},
    {"speaker": "SPEAKER_01", "start": 79.4, "end": 85.8, "text": "Okay, but this is exactly what happened last month, too. I ended up waiting over a week to get my money back."},
    {"speaker": "SPEAKER_00", "start": 85.9, "end": 98.1, "text": "I understand your frustration and I apologize for the inconvenience. Pending charges can sometimes occur due to merchant authorization issues, especially with ride share services."},
    {"speaker": "SPEAKER_01", "start": 98.1, "end": 103.9, "text": "I get that, but it's becoming a pattern now. I'm honestly starting to lose confidence in this bank."},
    {"speaker": "SPEAKER_00", "start": 103.9, "end": 113.9, "text": "I completely understand your concern. What I can do is submit a dispute review immediately so the pending transaction can be investigated faster."},
    {"speaker": "SPEAKER_01", "start": 114.0, "end": 116.3, "text": "How long is that supposed to take?"},
    {"speaker": "SPEAKER_00", "start": 116.3, "end": 128.2, "text": "Typically, pending authorizations fall off automatically within three to five business days. However, once I escalate the review, the disputes team may resolve it sooner."},
    {"speaker": "SPEAKER_01", "start": 128.2, "end": 133.9, "text": "Three to five days is still ridiculous. That money was supposed to cover another payment today."},
    {"speaker": "SPEAKER_00", "start": 133.9, "end": 140.0, "text": "I understand. Let me see if there are any provisional credit options available on your account."},
    {"speaker": "SPEAKER_01", "start": 140.0, "end": 141.6, "text": "Okay."},
    {"speaker": "SPEAKER_00", "start": 141.6, "end": 151.0, "text": "Thank you for your patience. Based on your account history, I can request a temporary provisional credit while the investigation is ongoing."},
    {"speaker": "SPEAKER_01", "start": 151.0, "end": 153.5, "text": "So the money would be available today?"},
    {"speaker": "SPEAKER_00", "start": 153.5, "end": 161.6, "text": "In most cases, yes. It usually reflects within a few business hours, though I cannot guarantee the exact timing."},
    {"speaker": "SPEAKER_01", "start": 161.6, "end": 164.1, "text": "Fine. Please do that then."},
    {"speaker": "SPEAKER_00", "start": 164.1, "end": 170.1, "text": "Absolutely. I've submitted the request and marked the dispute as high priority."},
    {"speaker": "SPEAKER_01", "start": 170.1, "end": 171.5, "text": "All right."},
    {"speaker": "SPEAKER_00", "start": 171.5, "end": 179.6, "text": "You'll also receive a confirmation email within the next 15 minutes. Is your email ending in gmail.com still correct?"},
    {"speaker": "SPEAKER_01", "start": 179.6, "end": 181.6, "text": "Yes, that's correct."},
    {"speaker": "SPEAKER_00", "start": 181.6, "end": 186.1, "text": "Perfect. Is there anything else I can assist you with today?"},
    {"speaker": "SPEAKER_01", "start": 186.1, "end": 190.7, "text": "Honestly, I just hope I don't have to keep calling about the same thing every month."},
    {"speaker": "SPEAKER_00", "start": 190.7, "end": 202.3, "text": "I understand. And I truly apologize for the repeated inconvenience. I'll also attach notes recommending a review of recurring merchant authorization issues on your account."},
    {"speaker": "SPEAKER_01", "start": 202.3, "end": 204.5, "text": "All right. Thanks."},
    {"speaker": "SPEAKER_00", "start": 204.5, "end": 211.3, "text": "You're welcome, Mr. Ahmed. Thank you for calling Horizon National Bank and enjoy the rest of your day."},
    {"speaker": "SPEAKER_01", "start": 211.3, "end": 212.3, "text": "Yeah, you too."}
]
    
    initial_state = {
        "transcript" : final_transcript
    }

    result = app.invoke(initial_state)
    print(result)




