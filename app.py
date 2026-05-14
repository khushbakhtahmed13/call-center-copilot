from audio_processing import get_final_transcript
from graph import app
from html import escape as h
import os
import streamlit as st
import streamlit.components.v1 as components

# ── Audio / transcript ────────────────────────────────────────────────────────
CALLS_DIR = "data/calls"
audio_files = [
    os.path.join(CALLS_DIR, f)
    for f in os.listdir(CALLS_DIR)
    if f.endswith(".wav")
]
if not audio_files:
    st.error("No audio files found in data/calls")
    st.stop()

latest_audio = max(audio_files, key=os.path.getctime)
final_transcript = get_final_transcript(latest_audio)

# ── Run graph ─────────────────────────────────────────────────────────────────
result = app.invoke({"transcript": final_transcript})

# ── Extract results ───────────────────────────────────────────────────────────
sentiment   = result["sentiment_analysis"]
compliance  = result["compliance_analysis"]
performance = result["agent_performance"]
risk        = result["risk_detection"]
summary     = result["summary"]

# ── Speaker roles ─────────────────────────────────────────────────────────────
speaker_order: list[str] = []
for seg in final_transcript:
    if seg["speaker"] not in speaker_order:
        speaker_order.append(seg["speaker"])

agent_id    = speaker_order[0] if len(speaker_order) > 0 else "SPEAKER_00"
customer_id = speaker_order[1] if len(speaker_order) > 1 else "SPEAKER_01"

def speaker_label(spk: str) -> str:
    if spk == agent_id:    return "Agent"
    if spk == customer_id: return "Customer"
    return h(spk)

# ── Derived values ────────────────────────────────────────────────────────────
total_duration = final_transcript[-1]["end"] - final_transcript[0]["start"]
minutes = int(total_duration // 60)
seconds = int(total_duration % 60)

speaker_durations: dict[str, float] = {}
for seg in final_transcript:
    spk = seg["speaker"]
    speaker_durations[spk] = speaker_durations.get(spk, 0) + (seg["end"] - seg["start"])
total_talk = sum(speaker_durations.values())

def talk_pct(spk_id: str) -> float:
    return round(speaker_durations.get(spk_id, 0) / total_talk * 100, 1) if total_talk else 0.0

agent_pct = talk_pct(agent_id)
cust_pct  = talk_pct(customer_id)

follow_up  = "Yes" if summary.follow_up_needed               else "No"
urgent_fu  = "Yes" if risk.urgent_follow_up_required         else "No"
id_status  = "✓ Verified"  if compliance.identity_verified            else "✗ Not verified"
emp_status = "✓ Shown"     if compliance.empathy_shown                else "✗ Not shown"
esc_status = "✓ Correct"   if compliance.escalation_handled_correctly else "✗ Needs review"
ref_status = "✓ Followed"  if compliance.refund_policy_followed       else "✗ Not followed"

def risk_cls(val: str) -> str:
    v = val.lower()
    if any(w in v for w in ("none", "low")):        return "r-green"
    if any(w in v for w in ("moderate", "medium")): return "r-amber"
    return "r-red"

_SENT_WIDTH = {
    "frustrated": 80, "angry": 90, "negative": 75, "very frustrated": 90,
    "neutral": 50,
    "satisfied": 40, "somewhat satisfied": 50, "positive": 35, "happy": 25,
}
_NEG_WORDS = ("frustrated", "angry", "negative", "very frustrated")

def sent_width(label: str) -> int:
    return _SENT_WIDTH.get(label.lower(), 60)

def sent_color(label: str) -> str:
    return "#ef4444" if label.lower() in _NEG_WORDS else "#22c55e"

call_id = os.path.splitext(os.path.basename(latest_audio))[0]

# ── HuggingFace dark color tokens ────────────────────────────────────────────
# Extracted from HF dark UI screenshot
BG        = "#0D1117"   # page background
CARD      = "#161B22"   # card / panel background
BORDER    = "#21262D"   # card borders
TEXT      = "#F1F1F1"   # primary text
MUTED     = "#888888"   # secondary / label text
ORANGE    = "#FF9D00"   # HF orange accent
ORANGE_DIM= "#2A1F00"   # orange tint bg
GREEN     = "#34D399"   # success green
GREEN_DIM = "#052E16"   # green tint bg
RED       = "#F87171"   # danger red
RED_DIM   = "#2D0A0A"   # red tint bg
AMBER     = "#FBBF24"   # amber / warning
AMBER_DIM = "#1C1400"   # amber tint bg

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="Call Center QA Copilot")

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background:{BG}; }}
[data-testid="stHeader"]           {{ display:none; }}
section[data-testid="stMain"] > div {{ padding-top:0 !important; }}
div[data-testid="stVerticalBlock"]  {{ gap:0 !important; }}

.card {{
    background:{CARD};
    border:1px solid {BORDER};
    border-radius:10px;
    padding:14px 16px;
    margin-bottom:10px;
}}
.sec-label {{
    font-size:10px;font-weight:700;letter-spacing:.08em;
    text-transform:uppercase;color:{MUTED};margin-bottom:8px;
}}
.kpi-wrap  {{ display:flex;align-items:center;gap:10px; }}
.kpi-icon  {{ width:34px;height:34px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0; }}
.kpi-label {{ font-size:11px;color:{MUTED};margin-bottom:2px; }}
.kpi-val   {{ font-size:15px;font-weight:700;color:{TEXT}; }}

.bar-row   {{ display:flex;align-items:center;gap:8px;margin-bottom:6px; }}
.bar-label {{ font-size:11px;color:{MUTED};width:80px;flex-shrink:0; }}
.bar-track {{ flex:1;height:6px;background:#2D2D2D;border-radius:3px;overflow:hidden; }}
.bar-fill  {{ height:100%;border-radius:3px;background:{ORANGE}; }}
.bar-score {{ font-size:11px;color:{MUTED};width:24px;text-align:right; }}

.coach-item {{ display:flex;align-items:flex-start;gap:7px;font-size:12px;color:#D1D1D1;margin-bottom:5px;line-height:1.4; }}
.coach-dot  {{ width:7px;height:7px;border-radius:50%;flex-shrink:0;margin-top:4px; }}

.comp-row {{ display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid {BORDER};font-size:12px; }}
.comp-row:last-child {{ border-bottom:none; }}
.comp-key  {{ color:{MUTED}; }}
.comp-pass {{ color:{GREEN};font-weight:600; }}
.comp-fail {{ color:{RED};font-weight:600; }}

.risk-grid  {{ display:grid;grid-template-columns:1fr 1fr;gap:7px; }}
.risk-pill  {{ padding:8px 10px;border-radius:8px;text-align:center; }}
.risk-label {{ font-size:10px;margin-bottom:3px; }}
.risk-val   {{ font-size:13px;font-weight:700; }}
.r-amber {{ background:{AMBER_DIM}; }}
.r-amber .risk-label {{ color:{AMBER}; }}
.r-amber .risk-val   {{ color:{AMBER}; }}
.r-green {{ background:{GREEN_DIM}; }}
.r-green .risk-label {{ color:{GREEN}; }}
.r-green .risk-val   {{ color:{GREEN}; }}
.r-red   {{ background:{RED_DIM}; }}
.r-red   .risk-label {{ color:{RED}; }}
.r-red   .risk-val   {{ color:{RED}; }}

.tag {{ display:inline-block;font-size:10px;padding:2px 8px;border-radius:20px;border:1px solid;margin:2px 2px 0 0; }}
.tag-amber {{ background:{AMBER_DIM};color:{AMBER};border-color:#3D2E00; }}
.tag-orange {{ background:{ORANGE_DIM};color:{ORANGE};border-color:#3D2900; }}
.tag-red   {{ background:{RED_DIM};color:{RED};border-color:#5C1A1A; }}
.tag-green {{ background:{GREEN_DIM};color:{GREEN};border-color:#065F46; }}

.topbar       {{ display:flex;align-items:center;justify-content:space-between;padding:14px 4px 12px; }}
.topbar-title {{ font-size:18px;font-weight:700;color:{TEXT}; }}
.topbar-meta  {{ font-size:12px;color:{MUTED}; }}
.live-badge   {{ display:inline-flex;align-items:center;gap:5px;font-size:11px;background:{ORANGE_DIM};color:{ORANGE};border:1px solid #3D2900;border-radius:20px;padding:3px 10px;font-weight:600; }}

.stat-mini    {{ text-align:center;padding:8px;background:#141414;border-radius:7px;border:1px solid {BORDER}; }}
.stat-mini .sl {{ font-size:10px;color:{MUTED};margin-bottom:2px; }}
.stat-mini .sv {{ font-size:13px;font-weight:700; }}

.sent-row   {{ display:flex;align-items:center;gap:7px;margin-bottom:5px; }}
.sent-label {{ font-size:11px;color:{MUTED};width:50px;flex-shrink:0; }}
.sent-track {{ flex:1;height:7px;background:#2D2D2D;border-radius:4px;overflow:hidden; }}
.sent-fill  {{ height:100%;border-radius:4px; }}
.sent-val   {{ font-size:10px;color:{MUTED};min-width:80px; }}

.talk-row   {{ display:flex;align-items:center;gap:7px;margin-bottom:5px; }}
.talk-label {{ font-size:11px;color:{MUTED};width:70px;flex-shrink:0; }}
.talk-track {{ flex:1;height:8px;background:#2D2D2D;border-radius:4px;overflow:hidden; }}
.talk-fill  {{ height:100%;border-radius:4px; }}
.talk-pct   {{ font-size:11px;color:{MUTED};min-width:36px;text-align:right; }}
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:10px;">
    <span class="topbar-title">Call Center QA Copilot</span>
    <span class="live-badge">&#9679; Live review</span>
  </div>
  <div class="topbar-meta">Call: {h(call_id)} &nbsp;·&nbsp; {minutes}m {seconds}s</div>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
def kpi_card(icon, icon_bg, icon_color, label, value):
    return f"""
    <div class="card" style="margin-bottom:10px;margin-top:14px;">
      <div class="kpi-wrap">
        <div class="kpi-icon" style="background:{icon_bg};color:{icon_color};">{icon}</div>
        <div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-val">{h(str(value))}</div>
        </div>
      </div>
    </div>"""

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(kpi_card("😤", ORANGE_DIM, ORANGE,
        "Overall sentiment", sentiment.overall_sentiment.capitalize()),
        unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card("⭐", ORANGE_DIM, ORANGE,
        "Agent score", f"{performance.overall_score}/10"),
        unsafe_allow_html=True)
with k3:
    st.markdown(kpi_card("✅", GREEN_DIM, GREEN,
        "Compliance", compliance.overall_compliance.capitalize()),
        unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card("⚠️", AMBER_DIM, AMBER,
        "Escalation risk", risk.escalation_risk.capitalize()),
        unsafe_allow_html=True)

# ── Main layout ───────────────────────────────────────────────────────────────
left, right = st.columns([1, 2.4], gap="small")
with left:
    st.markdown("<div style='margin-top:38px'></div>", unsafe_allow_html=True)
    bubbles = ""

# ── LEFT: Transcript ──────────────────────────────────────────────────────────
# FIX: use components.html() with a fully self-contained HTML document.
# This renders in an iframe so it never depends on external CSS classes.
with left:
    bubbles = ""
    for seg in final_transcript:
        is_agent = seg["speaker"] == agent_id
        label    = "Agent" if is_agent else "Customer"
        bg       = "#1E1600" if is_agent else "#1A1A1A"
        border   = "#3D2900" if is_agent else "#2D2D2D"
        name_col = ORANGE    if is_agent else "#888888"

        bubbles += f"""
        <div style="background:{bg};border:1px solid {border};border-radius:10px;
                    padding:8px 10px;margin-bottom:6px;">
          <div style="font-size:10px;font-weight:700;color:{name_col};margin-bottom:2px;">{label}</div>
          <div style="font-size:10px;color:#666;margin-bottom:3px;">{seg['start']:.1f}s – {seg['end']:.1f}s</div>
          <div style="font-size:12px;color:#E5E5E5;line-height:1.5;">{h(seg['text'])}</div>
        </div>"""

    components.html(f"""
    <!DOCTYPE html><html><head><style>
      * {{ margin:0;padding:0;box-sizing:border-box; }}
      body {{ background:{CARD};padding:50px 16px 14px 16px;font-family:system-ui,sans-serif; }}
      .hdr {{ font-size:10px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
              color:{MUTED};margin-bottom:10px; }}
    </style></head>
    <body>
      <div class="hdr">Transcript</div>
      {bubbles}
    </body></html>
    """, height=860, scrolling=True)

# ── RIGHT: Analysis ───────────────────────────────────────────────────────────
with right:

    # ── Summary ───────────────────────────────────────────────────────────────
    res_tag_cls = "tag-green" if "resolv" in summary.resolution_status.lower() else "tag-orange"
    fu_tag_cls  = "tag-red"   if follow_up == "Yes" else "tag-green"

    st.markdown(f"""
    <div class="card" style="margin-top:14px;">
      <div class="sec-label">Issue summary</div>
      <div style="font-size:14px;font-weight:700;color:{TEXT};margin-bottom:6px;">{h(summary.customer_issue)}</div>
      <div>
        <span class="tag tag-amber">Sentiment: {h(sentiment.overall_sentiment.capitalize())}</span>
        <span class="tag {res_tag_cls}">{h(summary.resolution_status)}</span>
        <span class="tag {fu_tag_cls}">Follow-up: {follow_up}</span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px;">
        <div class="stat-mini">
          <div class="sl">Sentiment</div>
          <div class="sv" style="color:{ORANGE};">{h(summary.sentiment)}</div>
        </div>
        <div class="stat-mini">
          <div class="sl">Resolution</div>
          <div class="sv" style="color:{GREEN};">{h(summary.resolution_status)}</div>
        </div>
        <div class="stat-mini">
          <div class="sl">Follow-up needed</div>
          <div class="sv" style="color:{'#F87171' if follow_up=='Yes' else '#34D399'};">{follow_up}</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    pc1, pc2, pc3 = st.columns(3, gap="small")

    # ── Agent Performance ─────────────────────────────────────────────────────
    perf_data = [
        ("Professionalism", performance.professionalism_score),
        ("Empathy",         performance.empathy_score),
        ("Communication",   performance.communication_clarity_score),
        ("Resolution",      performance.resolution_effectiveness_score),
        ("Policy",          performance.policy_adherence_score),
    ]
    bars_html = "".join(f"""
        <div class="bar-row">
          <span class="bar-label">{lbl}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{score/10*100:.0f}%;"></div></div>
          <span class="bar-score">{score}</span>
        </div>""" for lbl, score in perf_data)

    strengths_html = "".join(
        f'<div class="coach-item"><div class="coach-dot" style="background:{GREEN};"></div>{h(s)}</div>'
        for s in performance.strengths)

    improvements_html = "".join(
        f'<div class="coach-item"><div class="coach-dot" style="background:{AMBER};"></div>{h(s)}</div>'
        for s in performance.improvement_areas)

    with pc1:
        st.markdown(f"""
        <div class="card" style="height:500px;overflow-y:auto;margin-top:14px;">
          <div class="sec-label">Agent performance</div>
          <div style="display:flex;align-items:baseline;gap:5px;margin-bottom:12px;">
            <span style="font-size:28px;font-weight:700;color:{TEXT};">{performance.overall_score}</span>
            <span style="font-size:13px;color:{MUTED};">/ 10</span>
          </div>
          {bars_html}
          <div style="margin-top:14px;">
            <div class="sec-label">Coaching</div>
            {strengths_html}
            {improvements_html}
          </div>
        </div>""", unsafe_allow_html=True)

    # ── Risk ──────────────────────────────────────────────────────────────────
    risk_factors_html = "".join(
        f'<div class="coach-item"><div class="coach-dot" style="background:{AMBER};"></div>{h(r)}</div>'
        for r in risk.detected_risk_factors)

    actions_html = "".join(
        f'<div class="coach-item"><div class="coach-dot" style="background:{ORANGE};"></div>{h(a)}</div>'
        for a in risk.recommended_actions)

    with pc2:
        st.markdown(f"""
        <div class="card" style="height:500px;overflow-y:auto;margin-top:14px;">
          <div class="sec-label">Risk analysis</div>
          <div class="risk-grid" style="margin-bottom:12px;">
            <div class="risk-pill {risk_cls(risk.customer_churn_risk)}">
              <div class="risk-label">Churn</div>
              <div class="risk-val">{h(risk.customer_churn_risk.capitalize())}</div>
            </div>
            <div class="risk-pill {risk_cls(risk.fraud_risk)}">
              <div class="risk-label">Fraud</div>
              <div class="risk-val">{h(risk.fraud_risk.capitalize())}</div>
            </div>
            <div class="risk-pill {risk_cls(risk.operational_risk)}">
              <div class="risk-label">Operational</div>
              <div class="risk-val">{h(risk.operational_risk.capitalize())}</div>
            </div>
            <div class="risk-pill {risk_cls(risk.overall_risk_level)}">
              <div class="risk-label">Overall</div>
              <div class="risk-val">{h(risk.overall_risk_level.capitalize())}</div>
            </div>
          </div>
          <div style="font-size:11px;margin-bottom:12px;">
            <span style="color:{MUTED};">Urgent follow-up: </span>
            <span style="font-weight:700;color:{'#F87171' if urgent_fu=='Yes' else '#34D399'};">{urgent_fu}</span>
          </div>
          <div class="sec-label">Detected risk factors</div>
          {risk_factors_html}
          <div class="sec-label" style="margin-top:12px;">Recommended actions</div>
          {actions_html}
        </div>""", unsafe_allow_html=True)

    # ── Compliance + Talk ratio + Duration + Sentiment shift ──────────────────
    # FIX: overflow-y:auto instead of overflow:hidden so content isn't clipped
    compliance_issues_html = "".join(
        f'<div class="coach-item"><div class="coach-dot" style="background:{RED};"></div>{h(i)}</div>'
        for i in compliance.compliance_issues
    ) or f'<div style="font-size:12px;color:{GREEN};">No issues detected</div>'

    with pc3:
        st.markdown(f"""
        <div class="card" style="height:500px;overflow-y:auto;margin-top:14px;">
          <div class="sec-label">Compliance</div>
          <div class="comp-row">
            <span class="comp-key">Identity verification</span>
            <span class="{'comp-pass' if compliance.identity_verified else 'comp-fail'}">{id_status}</span>
          </div>
          <div class="comp-row">
            <span class="comp-key">Empathy shown</span>
            <span class="{'comp-pass' if compliance.empathy_shown else 'comp-fail'}">{emp_status}</span>
          </div>
          <div class="comp-row">
            <span class="comp-key">Escalation handling</span>
            <span class="{'comp-pass' if compliance.escalation_handled_correctly else 'comp-fail'}">{esc_status}</span>
          </div>
          <div class="comp-row">
            <span class="comp-key">Refund policy</span>
            <span class="{'comp-pass' if compliance.refund_policy_followed else 'comp-fail'}">{ref_status}</span>
          </div>
          <div class="comp-row" style="border-bottom:none;">
            <span class="comp-key">Overall</span>
            <span class="{'comp-pass' if compliance.overall_compliance.lower()=='compliant' else 'comp-fail'}">{h(compliance.overall_compliance.capitalize())}</span>
          </div>

          <div class="sec-label" style="margin-top:12px;">Issues</div>
          {compliance_issues_html}

          <div class="sec-label" style="margin-top:14px;">Talk ratio</div>
          <div class="talk-row">
            <span class="talk-label">Agent</span>
            <div class="talk-track"><div class="talk-fill" style="width:{agent_pct}%;background:{ORANGE};"></div></div>
            <span class="talk-pct">{agent_pct}%</span>
          </div>
          <div class="talk-row">
            <span class="talk-label">Customer</span>
            <div class="talk-track"><div class="talk-fill" style="width:{cust_pct}%;background:#555555;"></div></div>
            <span class="talk-pct">{cust_pct}%</span>
          </div>

          <div style="margin-top:14px;background:#141414;border-radius:8px;padding:10px;text-align:center;border:1px solid {BORDER};">
            <div style="font-size:10px;color:{MUTED};margin-bottom:3px;">Total call duration</div>
            <div style="font-size:20px;font-weight:700;color:{TEXT};">{minutes}m {seconds}s</div>
          </div>

          <div class="sec-label" style="margin-top:14px;">Sentiment shift</div>
          <div class="sent-row">
            <span class="sent-label">Start</span>
            <div class="sent-track"><div class="sent-fill" style="width:{sent_width(sentiment.start_sentiment)}%;background:{sent_color(sentiment.start_sentiment)};"></div></div>
            <span class="sent-val">{h(sentiment.start_sentiment.capitalize())}</span>
          </div>
          <div class="sent-row">
            <span class="sent-label">End</span>
            <div class="sent-track"><div class="sent-fill" style="width:{sent_width(sentiment.end_sentiment)}%;background:{sent_color(sentiment.end_sentiment)};"></div></div>
            <span class="sent-val">{h(sentiment.end_sentiment.capitalize())}</span>
          </div>
        </div>""", unsafe_allow_html=True)