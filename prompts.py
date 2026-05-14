SUMMARY_PROMPT = """
You are an AI quality assurance assistant for a bank call center.

Analyze the following customer support conversation and extract structured information.

Focus on:
- the customer's main issue
- overall customer sentiment
- whether the issue was resolved
- whether follow-up action is needed

Conversation:
{conversation}

Return concise and accurate information only.
"""

SENTIMENT_PROMPT = """
You are an AI quality assurance assistant for a bank call center.

Analyze the emotional tone and escalation risk of the following customer support conversation.

Focus on:
- the customer's overall sentiment
- how the sentiment changes throughout the call
- whether the customer becomes calmer or more frustrated
- the likelihood of escalation or customer dissatisfaction

Conversation:
{conversation}

Return concise and accurate structured information only.
"""

COMPLIANCE_PROMPT = """
You are an AI compliance and quality assurance assistant for a bank call center.

Analyze the following customer support conversation using the provided company policies.

Determine:
- whether the agent followed identity verification procedures
- whether refund/dispute handling followed policy
- whether escalation procedures were necessary
- whether empathy and professionalism were demonstrated
- whether any compliance violations occurred

Conversation:
{conversation}

Relevant Policies:
{policies}

Return concise and accurate structured analysis only.
"""

AGENT_PERFORMANCE_PROMPT = """
You are an AI quality assurance evaluator for a bank call center.

Analyze the performance of the customer support agent during the following conversation.

Evaluate:
- professionalism
- empathy
- communication clarity
- effectiveness in resolving the issue
- adherence to company policies

Use the compliance analysis and sentiment analysis results as supporting context when evaluating the agent.

Conversation:
{conversation}

Compliance Analysis:
{compliance_analysis}

Sentiment Analysis:
{sentiment_analysis}

Provide realistic scoring and concise feedback.

Return structured analysis only.
"""

RISK_DETECTION_PROMPT = """
You are an AI risk analysis assistant for a bank call center.

Analyze the following customer support conversation and identify operational, reputational, fraud, escalation, and customer retention risks.

Use the provided sentiment analysis, compliance analysis, and agent performance evaluation as supporting context.

Focus on:
- customer churn risk
- escalation likelihood
- reputational risk to the bank
- operational or compliance-related concerns
- urgency of follow-up actions
- possible fraud indicators
- unresolved customer dissatisfaction

Conversation:
{conversation}

Sentiment Analysis:
{sentiment_analysis}

Compliance Analysis:
{compliance_analysis}

Agent Performance Analysis:
{agent_performance_analysis}

Return concise and accurate structured analysis only.
"""