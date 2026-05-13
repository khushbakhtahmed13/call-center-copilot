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