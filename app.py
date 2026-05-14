#from audio_processing import get_final_transcript
from graph import app
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Transcript
path = "data/calls/synthetic_bank_call.wav"
#final_transcript = get_final_transcript(path)
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

# Run Graph
result = app.invoke({
         "transcript" : final_transcript
})




st.set_page_config(layout="wide")

st.title("AI Call Center QA Copilot")



# Key Performance Indicators

sentiment = result["sentiment_analysis"]
compliance = result["compliance_analysis"]
performance = result["agent_performance"]
risk = result["risk_detection"]

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

card_style = """
background-color:#f3f4f6;
padding:20px;
border-radius:15px;
border:1px solid #d1d5db;
text-align:center;
box-shadow:0 2px 8px rgba(0,0,0,0.08);
"""

label_style = """
color:#6b7280;
font-size:14px;
font-weight:600;
margin-bottom:10px;
"""

value_style = """
color:#111827;
font-size:24px;
font-weight:700;
"""

with kpi1:
    st.markdown(
        f"""
        <div style="{card_style}">
            <div style="{label_style}">Overall Sentiment</div>
            <div style="{value_style}">
                {sentiment.overall_sentiment.capitalize()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div style="{card_style}">
            <div style="{label_style}">Agent Score</div>
            <div style="{value_style}">
                {performance.overall_score}/10
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div style="{card_style}">
            <div style="{label_style}">Compliance Status</div>
            <div style="{value_style}">
                {compliance.overall_compliance.capitalize()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div style="{card_style}">
            <div style="{label_style}">Escalation Risk</div>
            <div style="{value_style}">
                {risk.escalation_risk.capitalize()}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

left_col, right_col = st.columns([1, 2])


# Transcript

with left_col:

    st.subheader("Call Transcript")

    transcript_html = ""

    for segment in final_transcript:

        speaker = segment["speaker"]
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        transcript_html += f"""
        <div style="
            padding:10px;
            margin-bottom:10px;
            border-radius:10px;
            background-color:#1e1e1e;
            color:white;
        ">
            <b>{speaker}</b><br>
            <small>{start:.1f}s - {end:.1f}s</small>
            <p>{text}</p>
        </div>
        """

    st.markdown(
        f"""
        <div style="
            height:700px;
            overflow-y:scroll;
            padding-right:10px;
        ">
            {transcript_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# Summary

with right_col:

    st.subheader("Call Summary")

    summary = result["summary"]

    follow_up = "Yes" if summary.follow_up_needed else "No"

    st.markdown(
       f"""
    <div style="
        background-color:#111827;
        padding:20px;
        border-radius:15px;
        border:1px solid #374151;
        margin-bottom:20px;
    ">

    <h4 style="color:white;">Customer Issue</h4>
    <p style="color:#d1d5db;">
        {summary.customer_issue}
    </p>

    <hr style="border:1px solid #374151;">

    <div style="display:flex; gap:50px;">

    <div>
        <h5 style="color:#9ca3af;">Sentiment</h5>
        <p style="color:white; font-size:18px;">
            {summary.sentiment}
        </p>
    </div>

    <div>
        <h5 style="color:#9ca3af;">Resolution Status</h5>
        <p style="color:white; font-size:18px;">
            {summary.resolution_status}
        </p>
    </div>

    <div>
        <h5 style="color:#9ca3af;">Follow Up Needed</h5>
        <p style="color:white; font-size:18px;">
            {follow_up}
        </p>
    </div>

    </div>
    </div>
    """,
    unsafe_allow_html=True)

    
    # Agent Performance Radar Chart

    st.subheader("Agent Performance Analysis")

    performance = result["agent_performance"]

    categories = [
    "Professionalism",
    "Empathy",
    "Communication",
    "Resolution",
    "Policy Adherence"
    ]

    values = [
    performance.professionalism_score,
    performance.empathy_score,
    performance.communication_clarity_score,
    performance.resolution_effectiveness_score,
    performance.policy_adherence_score
    ]

    values += values[:1]
    categories += categories[:1]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Agent Performance'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 10]
        )
        
    ),
    showlegend=False,
    height=500
    )


    st.plotly_chart(fig, use_container_width=True)


    # Coaching Recommendations

    st.subheader("Agent Coaching Recommendations")

    strengths = performance.strengths
    improvements = performance.improvement_areas

    coach_col1, coach_col2 = st.columns(2)

    # Strengths Panel
    with coach_col1:

        strengths_html = ""

        for item in strengths:
            strengths_html += f"""
            <li style="margin-bottom:10px;">
                {item}
            </li>
            """

        st.markdown(
            f"""
            <div style="
                background-color:#ecfdf5;
                padding:20px;
                border-radius:15px;
                border:1px solid #10b981;
                height:250px;
            ">

            <h4 style="color:#065f46;">
                Strengths
            </h4>

            <ul style="
                color:#064e3b;
                padding-left:20px;
            ">
                {strengths_html}
            </ul>

            </div>
            """,
            unsafe_allow_html=True
        )

    # Improvements Panel
    with coach_col2:

        improvements_html = ""

        for item in improvements:
            improvements_html += f"""
            <li style="margin-bottom:10px;">
                {item}
            </li>
            """

        st.markdown(
            f"""
            <div style="
                background-color:#fef2f2;
                padding:20px;
                border-radius:15px;
                border:1px solid #ef4444;
                height:250px;
            ">

            <h4 style="color:#991b1b;">
                Improvement Areas
            </h4>

            <ul style="
                color:#7f1d1d;
                padding-left:20px;
            ">
                {improvements_html}
            </ul>

            </div>
            """,
            unsafe_allow_html=True
        )



    # =========================
    # RISK ANALYSIS
    # =========================

    st.subheader("Risk Analysis")

    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:

        components.html(f"""
        <div style="
            background-color:#fff7ed;
            padding:20px;
            border-radius:15px;
            border:1px solid #fdba74;
            text-align:center;
            height:140px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

            <div style="
                color:#9a3412;
                font-size:14px;
                font-weight:600;
                margin-bottom:15px;
            ">
                Customer Churn Risk
            </div>

            <div style="
                color:#7c2d12;
                font-size:24px;
                font-weight:700;
            ">
                {risk.customer_churn_risk.capitalize()}
            </div>

        </div>
        """, height=160)

    with risk_col2:

        components.html(f"""
        <div style="
            background-color:#fff7ed;
            padding:20px;
            border-radius:15px;
            border:1px solid #fdba74;
            text-align:center;
            height:140px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

            <div style="
                color:#9a3412;
                font-size:14px;
                font-weight:600;
                margin-bottom:15px;
            ">
                Fraud Risk
            </div>

            <div style="
                color:#7c2d12;
                font-size:24px;
                font-weight:700;
            ">
                {risk.fraud_risk.capitalize()}
            </div>

        </div>
        """, height=160)

    with risk_col3:

        components.html(f"""
        <div style="
            background-color:#fff7ed;
            padding:20px;
            border-radius:15px;
            border:1px solid #fdba74;
            text-align:center;
            height:140px;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

            <div style="
                color:#9a3412;
                font-size:14px;
                font-weight:600;
                margin-bottom:15px;
            ">
                Operational Risk
            </div>

            <div style="
                color:#7c2d12;
                font-size:24px;
                font-weight:700;
            ">
                {risk.operational_risk.capitalize()}
            </div>

        </div>
        """, height=160)

    urgent_followup = (
        "Yes"
        if risk.urgent_follow_up_required
        else "No"
    )

    detected_risks_html = ""

    for item in risk.detected_risk_factors:
        detected_risks_html += f"<li>{item}</li>"

    recommended_actions_html = ""

    for item in risk.recommended_actions:
        recommended_actions_html += f"<li>{item}</li>"

    components.html(f"""
    <div style="
        background-color:#111827;
        padding:25px;
        border-radius:15px;
        border:1px solid #374151;
        margin-top:20px;
    ">

        <h3 style="color:white;">
            Overall Risk Level: {risk.overall_risk_level.capitalize()}
        </h3>

        <p style="color:#d1d5db;">
            <b>Urgent Follow Up Required:</b> {urgent_followup}
        </p>

        <hr style="border:1px solid #374151;">

        <div style="
            display:flex;
            gap:50px;
        ">

            <div style="flex:1;">

                <h4 style="color:#fbbf24;">
                    Detected Risk Factors
                </h4>

                <ul style="
                    color:#e5e7eb;
                    padding-left:20px;
                ">
                    {detected_risks_html}
                </ul>

            </div>

            <div style="flex:1;">

                <h4 style="color:#60a5fa;">
                    Recommended Actions
                </h4>

                <ul style="
                    color:#e5e7eb;
                    padding-left:20px;
                ">
                    {recommended_actions_html}
                </ul>

            </div>

        </div>

    </div>
    """)

    # Compliance Analysis

    st.subheader("Compliance Analysis")

    compliance_col1, compliance_col2 = st.columns([1, 2])

    with compliance_col1:

        verification_status = (
            "Verified"
            if compliance.identity_verified
            else "Not Verified"
        )

        empathy_status = (
            "Shown"
            if compliance.empathy_shown
            else "Not Shown"
        )

        escalation_status = (
            "Handled Correctly"
            if compliance.escalation_handled_correctly
            else "Needs Review"
        )

        refund_policy_status = (
            "Followed"
            if compliance.refund_policy_followed
            else "Not Followed"
        )

        st.markdown(f"""
        <div style="
            background-color:#ecfeff;
            padding:25px;
            border-radius:15px;
            border:1px solid #67e8f9;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
        ">

            <h3 style="color:#0f172a;">
                Compliance Status
            </h3>

            <p><b>Identity Verification:</b> {verification_status}</p>

            <p><b>Empathy Shown:</b> {empathy_status}</p>

            <p><b>Escalation Handling:</b> {escalation_status}</p>

            <p><b>Refund Policy:</b> {refund_policy_status}</p>

            <p><b>Overall Compliance:</b>
            {compliance.overall_compliance.capitalize()}</p>

        </div>
        """, unsafe_allow_html=True)

    with compliance_col2:

        compliance_issues_html = ""

        for issue in compliance.compliance_issues:
            compliance_issues_html += f"<li>{issue}</li>"

        st.markdown(f"""
        <div style="
            background-color:#fef2f2;
            padding:25px;
            border-radius:15px;
            border:1px solid #fca5a5;
            box-shadow:0 2px 8px rgba(0,0,0,0.08);
            min-height:250px;
        ">

            <h3 style="color:#991b1b;">
                Compliance Issues
            </h3>

            <ul style="
                color:#7f1d1d;
                padding-left:20px;
            ">
                {compliance_issues_html}
            </ul>

        </div>
        """, unsafe_allow_html=True)


    # =========================
    # TALK RATIO PIE CHART
    # =========================

    st.subheader("Conversation Analytics")

    speaker_durations = {}

    for segment in final_transcript:

        speaker = segment["speaker"]

        duration = (
            segment["end"] - segment["start"]
        )

        if speaker not in speaker_durations:
            speaker_durations[speaker] = 0

        speaker_durations[speaker] += duration

    labels = list(speaker_durations.keys())
    values = list(speaker_durations.values())

    pie_fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4
            )
        ]
    )

    pie_fig.update_layout(
        height=500
    )

    st.plotly_chart(
        pie_fig,
        use_container_width=True
    )


    # Call Duration Metric

    total_call_duration = (
        final_transcript[-1]["end"]
        -
        final_transcript[0]["start"]
    )

    minutes = int(total_call_duration // 60)

    seconds = int(total_call_duration % 60)

    st.markdown(f"""
    <div style="
        background-color:#f3f4f6;
        padding:20px;
        border-radius:15px;
        border:1px solid #d1d5db;
        text-align:center;
        margin-top:20px;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
    ">

        <h3 style="color:#374151;">
            Total Call Duration
        </h3>

        <div style="
            font-size:32px;
            font-weight:700;
            color:#111827;
        ">
            {minutes}m {seconds}s
        </div>

    </div>
    """, unsafe_allow_html=True)


    # Sentiment Overview

    st.subheader("Sentiment Analysis")

    sentiment_col1, sentiment_col2, sentiment_col3 = st.columns(3)

    with sentiment_col1:

        st.markdown(f"""
        <div style="
            background-color:#ecfdf5;
            padding:20px;
            border-radius:15px;
            border:1px solid #6ee7b7;
            text-align:center;
        ">

            <h4 style="color:#065f46;">
                Overall Sentiment
            </h4>

            <div style="
                font-size:24px;
                font-weight:700;
                color:#064e3b;
            ">
                {sentiment.overall_sentiment.capitalize()}
            </div>

        </div>
        """, unsafe_allow_html=True)

    with sentiment_col2:

        st.markdown(f"""
        <div style="
            background-color:#eff6ff;
            padding:20px;
            border-radius:15px;
            border:1px solid #93c5fd;
            text-align:center;
        ">

            <h4 style="color:#1d4ed8;">
                Start Sentiment
            </h4>

            <div style="
                font-size:24px;
                font-weight:700;
                color:#1e40af;
            ">
                {sentiment.start_sentiment.capitalize()}
            </div>

        </div>
        """, unsafe_allow_html=True)

    with sentiment_col3:

        st.markdown(f"""
        <div style="
            background-color:#fff7ed;
            padding:20px;
            border-radius:15px;
            border:1px solid #fdba74;
            text-align:center;
        ">

            <h4 style="color:#9a3412;">
                End Sentiment
            </h4>

            <div style="
                font-size:24px;
                font-weight:700;
                color:#7c2d12;
            ">
                {sentiment.end_sentiment.capitalize()}
            </div>

        </div>
        """, unsafe_allow_html=True)