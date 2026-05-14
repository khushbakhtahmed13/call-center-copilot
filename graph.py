from prompts import SUMMARY_PROMPT, SENTIMENT_PROMPT, COMPLIANCE_PROMPT, AGENT_PERFORMANCE_PROMPT, RISK_DETECTION_PROMPT
from schemas import CallSummary, SentimentAnalysis, ComplianceAnalysis, AgentPerformance, RiskDetection
from config import retriever, llm
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END



# State
class CallState(TypedDict):
    transcript : str
    summary : Optional[CallSummary]
    sentiment_analysis : Optional[SentimentAnalysis]
    compliance_analysis : Optional[ComplianceAnalysis]
    agent_performance : Optional[AgentPerformance]
    risk_detection : Optional[RiskDetection]


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






