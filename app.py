import streamlit as st
from openai import OpenAI
import json
import datetime
from duckduckgo_search import DDGS
from replit import db

# === AGENTS CONFIG ===
# All agent definitions live in agents_config.py.
# To add a new agent to the marketplace, edit that file — no changes needed here.
from agents_config import AGENTS


# ====================== PAGE CONFIG ======================
# MUST be the very first Streamlit call — before any markdown, CSS, or other commands.
st.set_page_config(page_title="Agent-in-a-Box Hub", page_icon="🧬", layout="wide")


# ====================== STYLING ======================
# All visual styling (fonts, colors, card layouts, hero banner, guardrail panels)
# lives here as a single CSS block so it's easy to find and edit.
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    /* ── Typography ── */
    html, body, [class*="css"], .stMarkdown, .stTextInput, .stTextArea,
    .stButton, .stExpander, p, h1, h2, h3, h4, label, div {
        font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif !important;
    }
    /* ── Layout ── */
    .main > div { padding-top: 0rem; }
    .block-container { padding: 2rem 3rem 3rem; max-width: 980px; margin: auto; }
    body { background-color: #f9fafb; }
    /* ── Hero ── */
    .hero {
        background: linear-gradient(140deg, #0a0f1e 0%, #0f2044 55%, #102a52 100%);
        border-radius: 18px;
        padding: 3.2rem 3rem 2.8rem;
        margin-bottom: 2.5rem;
        text-align: center;
        color: #ffffff;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .hero .badge {
        display: inline-block;
        background: rgba(251,191,36,0.12);
        color: #fbbf24;
        border: 1px solid rgba(251,191,36,0.35);
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.3rem 1rem;
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 0 0 0.85rem;
        line-height: 1.12;
        color: #ffffff;
    }
    .hero p {
        font-size: 1.05rem;
        color: #8fa8c8;
        max-width: 580px;
        margin: 0 auto;
        line-height: 1.75;
        font-weight: 400;
    }
    /* ── Feature cards ── */
    .card {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 14px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 2px 8px rgba(10,20,50,0.06);
    }
    .card h3 {
        font-size: 0.98rem;
        font-weight: 700;
        color: #0d1b2e;
        margin: 0 0 0.45rem;
        letter-spacing: -0.01em;
    }
    .card p {
        color: #5a6880;
        font-size: 0.9rem;
        margin: 0;
        line-height: 1.65;
        font-weight: 400;
    }
    /* ── ReAct step pills ── */
    /* These coloured labels (Plan / Act / Reflect) show the agent's reasoning steps */
    .step-pill {
        display: inline-block;
        border-radius: 6px;
        padding: 0.2rem 0.7rem;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .step-plan { background:#eef2ff; color:#3730a3; border:1px solid #c7d2fe; }
    .step-action { background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; }
    .step-reflect{ background:#fff7ed; color:#92400e; border:1px solid #fde68a; }
    /* ── Section labels ── */
    .section-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #8fa0b5;
        margin: 2.2rem 0 0.75rem;
    }
    /* ── API key panel ── */
    .key-panel {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 4px rgba(10,20,50,0.04);
    }
    /* ── Streamlit overrides ── */
    div.stButton > button[kind="primary"] {
        background: #2563eb !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.55rem 1.4rem !important;
        font-size: 0.93rem !important;
        letter-spacing: -0.01em !important;
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover { background: #1d4ed8 !important; }
    div.stButton > button[kind="secondary"] {
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.88rem !important;
    }
    .stTextInput input, .stTextArea textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.93rem !important;
        border-radius: 9px !important;
        border-color: #d1dae6 !important;
        color: #0d1b2e !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }
    .stExpander { border-radius: 12px !important; border-color: #e5e9f0 !important; }
    .stAlert { border-radius: 10px !important; }
    /* ── Safety Guardrails panel ── */
    .guardrails-panel {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 14px;
        padding: 1.2rem 1.4rem 1.1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(10,20,50,0.04);
    }
    .guardrails-title {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #3b82f6;
        margin-bottom: 0.1rem;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }
    .guardrails-sub {
        font-size: 0.78rem;
        color: #8fa0b5;
        margin-bottom: 0.8rem;
        font-weight: 400;
    }
    .cost-badge {
        display: inline-block;
        background: #f0fdf4;
        color: #166534;
        border: 1px solid #bbf7d0;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.18rem 0.7rem;
        margin-left: 0.4rem;
    }
    .cost-badge-warn {
        background: #fff7ed;
        color: #92400e;
        border-color: #fde68a;
    }
    .cost-badge-danger {
        background: #fef2f2;
        color: #991b1b;
        border-color: #fecaca;
    }
    .guardrail-trace {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
        border-radius: 6px;
        padding: 0.18rem 0.65rem;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    /* ── Onboarding Tour ── */
    .tour-wrap {
        background: linear-gradient(140deg, #0a0f1e 0%, #0f2044 55%, #102a52 100%);
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.09);
        padding: 2.6rem 2.8rem 2.2rem;
        margin-bottom: 2rem;
        color: #ffffff;
        text-align: center;
    }
    .tour-step-label {
        display: inline-block;
        background: rgba(251,191,36,0.12);
        color: #fbbf24;
        border: 1px solid rgba(251,191,36,0.35);
        border-radius: 999px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.28rem 1rem;
        margin-bottom: 1.2rem;
    }
    .tour-wrap h2 {
        font-size: 1.65rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0 0 0.7rem;
        color: #ffffff;
    }
    .tour-wrap p {
        font-size: 0.98rem;
        color: #8fa8c8;
        max-width: 520px;
        margin: 0 auto 1.4rem;
        line-height: 1.75;
    }
    .tour-trace-demo {
        display: inline-flex;
        gap: 0.5rem;
        align-items: center;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.85rem 1.4rem;
        margin-bottom: 1.5rem;
        font-size: 0.82rem;
        font-weight: 600;
        flex-wrap: wrap;
        justify-content: center;
    }
    .tour-trace-demo .tp { background:#eef2ff; color:#3730a3; border-radius:6px; padding:0.2rem 0.65rem; }
    .tour-trace-demo .ta { background:#ecfdf5; color:#065f46; border-radius:6px; padding:0.2rem 0.65rem; }
    .tour-trace-demo .tr { background:#fff7ed; color:#92400e; border-radius:6px; padding:0.2rem 0.65rem; }
    .tour-trace-demo .arr { color: rgba(255,255,255,0.35); font-weight:400; }
    .tour-prompt-box {
        background: rgba(255,255,255,0.06);
        border: 1px dashed rgba(255,255,255,0.18);
        border-radius: 10px;
        padding: 0.9rem 1.2rem;
        font-size: 0.93rem;
        color: #c8d8ec;
        font-style: italic;
        margin-bottom: 1.5rem;
        text-align: left;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
    }
    .tour-safety-list {
        list-style: none;
        padding: 0;
        margin: 0 auto 1.5rem;
        max-width: 420px;
        text-align: left;
    }
    .tour-safety-list li {
        color: #8fa8c8;
        font-size: 0.93rem;
        padding: 0.38rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .tour-safety-list li:last-child { border-bottom: none; }
    .tour-dots {
        display: flex;
        justify-content: center;
        gap: 0.45rem;
        margin-bottom: 1.2rem;
    }
    .tour-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: rgba(255,255,255,0.18);
        display: inline-block;
    }
    .tour-dot.active { background: #fbbf24; }
    /* ── Session Results Box ── */
    .results-box {
        background: #ffffff;
        border: 1px solid #e5e9f0;
        border-radius: 14px;
        padding: 1.4rem 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 2px 8px rgba(10,20,50,0.06);
        display: flex;
        align-items: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    .results-box .rb-title {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #2563eb;
        margin-bottom: 0.9rem;
        display: block;
        width: 100%;
    }
    .results-box .rb-stat {
        display: flex;
        flex-direction: column;
        min-width: 110px;
    }
    .results-box .rb-number {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0d1b2e;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    .results-box .rb-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #8fa0b5;
        margin-top: 0.25rem;
    }
    .results-box .rb-divider {
        width: 1px;
        height: 40px;
        background: #e5e9f0;
        flex-shrink: 0;
    }
    .results-box .rb-message {
        font-size: 0.93rem;
        color: #5a6880;
        font-weight: 500;
        flex: 1;
        min-width: 160px;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ====================== HERO BANNER ======================
# The big header users see first. Edit the text here to customise your branding.
st.markdown(
    """
<div class="hero">
    <div class="badge">NEW v3 • Multi-Template Hub</div>
    <h1>Agent-in-a-Box</h1>
    <p>Fork → Run → Instantly experience real agentic AI.<br>
    Switch between 4 ready-to-use agents. Watch them plan, call tools, act, and reflect.<br>
    Literacy Mode teaches you how agents actually work.</p>
</div>
""",
    unsafe_allow_html=True,
)


# ====================== ONBOARDING TOUR ======================
# A 3-step guided tour shown to first-time users.
# Once the user clicks "Let's go", onboarding_done is set to True and the tour disappears.
if "onboarding_done" not in st.session_state:
    st.session_state.onboarding_done = False
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

_TOUR_CARDS = [
    {
        "label": "Step 1 of 3 • What is an Agent?",
        "title": "Meet your AI agent",
        "body": (
            "Unlike a simple chatbot, an agent can <strong style='color:#fff'>plan</strong>, "
            "take <strong style='color:#fff'>actions</strong> (like searching the web or saving notes), "
            "and <strong style='color:#fff'>reflect</strong> on what it did — all on its own."
        ),
        "extra": """
<div class="tour-trace-demo">
  <span class="tp">📋 Plan</span>
  <span class="arr">→</span>
  <span class="ta">🔧 Act</span>
  <span class="arr">→</span>
  <span class="tr">💡 Reflect</span>
</div>
<p style="font-size:0.82rem;color:rgba(143,168,200,0.7);margin-top:-0.8rem;">
  Every response you see below follows this pattern — that's what makes it an agent, not just a chatbot.
</p>""",
    },
    {
        "label": "Step 2 of 3 • Try your first agent",
        "title": "Send your first message",
        "body": (
            "Pick any agent from the sidebar, paste your API key, then try this starter prompt — "
            "or write your own. The agent will plan, search the web if needed, and reply in seconds."
        ),
        "extra": """
<div class="tour-prompt-box">
  💬 "What are 3 things I should do this week to feel more on top of my life?"
</div>""",
    },
    {
        "label": "Step 3 of 3 • Stay safe",
        "title": "Built-in guardrails protect you",
        "body": (
            "Before the agent can do anything risky, these rules kick in automatically. "
            "You can adjust them any time in the sidebar."
        ),
        "extra": """
<ul class="tour-safety-list">
  <li>🛡️ Never spend money or make purchases</li>
  <li>✉️ Always ask before sending any email</li>
  <li>🔒 Never share your personal information</li>
  <li>💰 Session budget limit stops runaway costs</li>
</ul>""",
    },
]

if not st.session_state.onboarding_done:
    _step = st.session_state.onboarding_step
    _card = _TOUR_CARDS[_step]

    _dots_html = "".join(
        f'<span class="tour-dot{"  active" if i == _step else ""}"></span>'
        for i in range(len(_TOUR_CARDS))
    )

    st.markdown(
        f"""
<div class="tour-wrap">
  <div class="tour-step-label">{_card["label"]}</div>
  <h2>{_card["title"]}</h2>
  <p>{_card["body"]}</p>
  {_card["extra"]}
  <div class="tour-dots">{_dots_html}</div>
</div>
""",
        unsafe_allow_html=True,
    )

    _btn_cols = st.columns([1, 1, 4])
    with _btn_cols[0]:
        if _step > 0:
            if st.button("← Back", key="tour_back"):
                st.session_state.onboarding_step -= 1
                st.rerun()
    with _btn_cols[1]:
        if _step < len(_TOUR_CARDS) - 1:
            if st.button("Next →", key="tour_next", type="primary"):
                st.session_state.onboarding_step += 1
                st.rerun()
        else:
            if st.button("Let's go ✓", key="tour_done", type="primary"):
                st.session_state.onboarding_done = True
                st.rerun()


# ====================== SESSION RESULTS BOX ======================
# Shows the user how many tasks they've completed and how much API credit was used.
# This resets whenever the user clicks "Clear Memory & Trace".
_tasks = st.session_state.get("tasks_completed", 0)
_cost  = st.session_state.get("session_cost", 0.0)
_mins  = _tasks * 5
_msg   = (
    f"Your agent just helped you with {_tasks} task{'s' if _tasks != 1 else ''}!"
    if _tasks > 0
    else "Complete your first task to see your results here."
)
st.markdown(
    f"""
<div class="results-box">
  <span class="rb-title">⚡ Your Results This Session</span>
  <div class="rb-stat">
    <span class="rb-number">{_mins} min</span>
    <span class="rb-label">Time Saved</span>
  </div>
  <div class="rb-divider"></div>
  <div class="rb-stat">
    <span class="rb-number">${_cost:.4f}</span>
    <span class="rb-label">API Cost Used</span>
  </div>
  <div class="rb-divider"></div>
  <div class="rb-message">✅ {_msg}</div>
</div>
""",
    unsafe_allow_html=True,
)

# ====================== AGENT CARDS ======================
# One card per agent, displayed in a 4-column grid.
# Cards are generated automatically from the AGENTS dictionary in agents_config.py.
st.markdown(
    '<div class="section-label">Choose your agent below — each one is fully agentic</div>',
    unsafe_allow_html=True,
)
cols = st.columns(4)
for i, (name, data) in enumerate(AGENTS.items()):
    with cols[i]:
        st.markdown(
            f"""
        <div class="card">
            <h3>{data["icon"]} {name}</h3>
            <p>{data.get("tagline", "Ready-to-run personal agent that plans, uses real tools, and reflects.")}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# ====================== SESSION STATE DEFAULTS ======================
# Sets safe default values for all session variables on first load.
# Using .setdefault() keeps this clean: values are only set if not already present.
for _k, _v in {
    "grok_key": "",
    "onboarding_done": False,
    "onboarding_step": 0,
    "guardrail_no_spend": True,
    "guardrail_ask_email": True,
    "guardrail_no_personal": True,
    "guardrail_max_spend": 0.50,
    "guardrail_approve_risky": False,
    "session_cost": 0.0,
    "tasks_completed": 0,
    "pending_input": None,
    "pending_confirmed": False,
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ====================== COST TRACKING ======================
# Grok token pricing. Update these if x.ai changes their rates.
GROK_COST_INPUT  = 5.0  / 1_000_000   # $ per input token
GROK_COST_OUTPUT = 15.0 / 1_000_000   # $ per output token

def add_cost(usage):
    """Add the cost of one API call to the running session total."""
    if usage:
        st.session_state.session_cost += (
            getattr(usage, "prompt_tokens", 0)    * GROK_COST_INPUT +
            getattr(usage, "completion_tokens", 0) * GROK_COST_OUTPUT
        )

def cost_badge_class(cost, limit):
    """Return a CSS class that colours the cost badge green / amber / red."""
    if cost >= limit:
        return "cost-badge cost-badge-danger"
    if cost >= limit * 0.75:
        return "cost-badge cost-badge-warn"
    return "cost-badge"


# ====================== GUARDRAILS ======================
# Safety rules that run BEFORE the agent ever sees the user's message.
# If a rule fires, the message is blocked or paused for confirmation.
SPEND_KEYWORDS  = ["buy", "purchase", "order", "pay", "charge", "subscribe", "checkout", "spend"]
EMAIL_KEYWORDS  = ["send email", "email to", "draft email", "compose email", "mail to", "send a message to"]
RISKY_KEYWORDS  = SPEND_KEYWORDS + ["delete", "remove", "post", "submit", "transfer", "share", "send"]

def input_contains(text, keywords):
    low = text.lower()
    return any(kw in low for kw in keywords)

def check_guardrails(user_text):
    """
    Returns (blocked: bool, reason: str | None).
    A blocked message is shown to the user as an error and never sent to the agent.
    """
    if st.session_state.guardrail_no_spend and input_contains(user_text, SPEND_KEYWORDS):
        return True, "Never spend money or make purchases guardrail triggered."
    if st.session_state.guardrail_no_personal and any(
        kw in user_text.lower() for kw in ["my address", "my ssn", "my password", "my card", "my bank"]
    ):
        return True, "Never share personal info guardrail triggered."
    if st.session_state.session_cost >= st.session_state.guardrail_max_spend:
        return True, f"Session budget of ${st.session_state.guardrail_max_spend:.2f} reached."
    return False, None

def needs_email_confirmation(user_text):
    """Returns True if the message looks like it wants to send an email."""
    return st.session_state.guardrail_ask_email and input_contains(user_text, EMAIL_KEYWORDS)

def needs_risky_confirmation(user_text):
    """Returns True if the message contains a high-risk action and the user has enabled extra approval."""
    return st.session_state.guardrail_approve_risky and input_contains(user_text, RISKY_KEYWORDS)


# ====================== SIDEBAR ======================
# The sidebar is the control panel: API key, guardrails, agent picker, and utilities.
with st.sidebar:

    # --- API Key ---
    st.header("🔑 Get Started")
    st.markdown(
        """
<div style="font-size:0.85rem;color:#5a6880;line-height:1.55;margin-bottom:0.6rem;">
  <strong style="color:#0d1b2e;">First time? Get a free key in 30 seconds:</strong><br>
  1. Open <a href="https://x.ai/api" target="_blank" style="color:#2563eb;font-weight:600;">x.ai/api</a> and sign in<br>
  2. Click <em>Create API Key</em><br>
  3. Copy the key and paste it below
</div>
""",
        unsafe_allow_html=True,
    )
    grok_key = st.text_input(
        "Paste your API key here",
        type="password",
        value=st.session_state.grok_key,
        help=(
            "Your key is kept only in this session's memory and is sent directly to x.ai "
            "to talk to your agent. It's not saved to disk or shared with anyone else by this app."
        ),
        placeholder="xai-...",
    )
    if grok_key:
        st.session_state.grok_key = grok_key
        st.success("✅ Key saved for this session")

    # --- Safety Guardrails ---
    st.markdown(
        """
<div class="guardrails-panel">
  <div class="guardrails-title">🛡️ Your Safety Settings</div>
  <div class="guardrails-sub">All on by default to keep you safe — adjust any time.</div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.session_state.guardrail_no_spend = st.toggle(
        "Never spend money or make purchases",
        value=st.session_state.guardrail_no_spend,
    )
    st.session_state.guardrail_ask_email = st.toggle(
        "Always ask before sending emails",
        value=st.session_state.guardrail_ask_email,
    )
    st.session_state.guardrail_no_personal = st.toggle(
        "Never share personal info",
        value=st.session_state.guardrail_no_personal,
    )

    _cost      = st.session_state.session_cost
    _limit     = st.session_state.guardrail_max_spend
    _badge_cls = cost_badge_class(_cost, _limit)
    _cost_display = "less than 1¢" if _cost < 0.01 else f"${_cost:.2f}"
    st.markdown(
        f'**Session spend** <span class="{_badge_cls}">{_cost_display} of ${_limit:.2f}</span>',
        unsafe_allow_html=True,
    )
    st.caption("💡 Each message costs a fraction of a cent — you're very unlikely to hit this limit.")
    st.session_state.guardrail_max_spend = st.slider(
        "Budget limit ($)",
        min_value=0.10,
        max_value=5.00,
        value=st.session_state.guardrail_max_spend,
        step=0.10,
        format="$%.2f",
        label_visibility="collapsed",
    )

    st.session_state.guardrail_approve_risky = st.checkbox(
        "Approve high-risk actions before running",
        value=st.session_state.guardrail_approve_risky,
        help="Agent will pause and ask for your confirmation before any action flagged as high-risk.",
    )

    st.divider()

    # --- Agent Selector ---
    # Choosing a new agent resets the conversation and trace automatically (see SESSION STATE below).
    selected_agent_name = st.selectbox(
        "Choose your Agent",
        options=list(AGENTS.keys()),
        format_func=lambda x: f"{AGENTS[x]['icon']} {x}",
    )
    selected_agent = AGENTS[selected_agent_name]

    # --- Agent Literacy Mode ---
    # When ON: every trace step shows a plain-English explanation of what the agent just did.
    # This is the core educational feature — users learn ReAct patterns by watching them live.
    literacy_mode = st.toggle("🧠 Agent Literacy Mode (show explanations)", value=True)

    st.divider()

    # --- Controls ---
    st.header("Controls")
    if st.button("Clear Memory & Trace"):
        st.session_state.trace = []
        st.session_state.session_cost = 0.0
        st.session_state.tasks_completed = 0
        st.session_state.pending_input = None
        st.session_state.pending_confirmed = False
        st.session_state.messages = [
            {"role": "system", "content": selected_agent["system_prompt"]}
        ]
        st.rerun()

    st.divider()

    # --- Premium Upgrade ---
    if "show_premium" not in st.session_state:
        st.session_state.show_premium = False

    if st.button("🚀 Make this agent always-on (Premium)", use_container_width=True, type="primary"):
        st.session_state.show_premium = not st.session_state.show_premium

    if st.session_state.show_premium:
        st.markdown(
            """
<div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border: 1px solid #e94560;
            border-radius: 12px;
            padding: 16px;
            margin-top: 8px;">
  <div style="font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 6px;">
    ⚡ Always-On Agent — $9/month
  </div>
  <div style="font-size: 0.85rem; color: #c9d1d9; margin-bottom: 12px; line-height: 1.5;">
    Deploy your chosen agent 24/7 in the cloud.<br><br>
    <strong style="color: #f0f0f0;">No more clicking Run every time</strong> — your agent works quietly in the background, handling tasks, monitoring updates, and acting on your behalf around the clock.
  </div>
  <a href="/upgrade" target="_blank" style="
    display: block;
    text-align: center;
    background: #e94560;
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 10px 0;
    border-radius: 8px;
    text-decoration: none;
    letter-spacing: 0.03em;">
    Upgrade — $9/month
  </a>
  <div style="font-size: 0.75rem; color: #8b949e; text-align: center; margin-top: 8px;">
    Cancel anytime. No contracts.
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    # --- Share Button ---
    import streamlit.components.v1 as components
    components.html(
        """
<style>
  .share-btn {
    width: 100%;
    padding: 10px 0;
    background: #ffffff;
    color: #1a1a2e;
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
    font-size: 0.88rem;
    font-weight: 600;
    border: 1.5px solid #d0d7de;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
  }
  .share-btn:hover {
    background: #f0f6ff;
    border-color: #0969da;
  }
  .share-btn.copied {
    background: #d4f7e7;
    border-color: #2da44e;
    color: #1a7f37;
  }
  .share-note {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
    font-size: 0.75rem;
    color: #6e7781;
    text-align: center;
    margin-top: 6px;
  }
</style>
<button class="share-btn" id="shareBtn" onclick="copyLink()">🔗 Share this template</button>
<p class="share-note" id="shareNote">Send this to a friend — they can fork it instantly</p>
<script>
  function copyLink() {
    var link = "https://replit.com/@YourUsername/agent-in-a-box";
    navigator.clipboard.writeText(link).then(function() {
      var btn = document.getElementById("shareBtn");
      var note = document.getElementById("shareNote");
      btn.textContent = "✅ Link copied!";
      btn.classList.add("copied");
      note.textContent = "Paste it anywhere to share";
      setTimeout(function() {
        btn.textContent = "🔗 Share this template";
        btn.classList.remove("copied");
        note.textContent = "Send this to a friend — they can fork it instantly";
      }, 2500);
    }).catch(function() {
      var btn = document.getElementById("shareBtn");
      btn.textContent = "⚠️ Copy manually";
      setTimeout(function() { btn.textContent = "🔗 Share this template"; }, 2500);
    });
  }
</script>
""",
        height=80,
        scrolling=False,
    )


# ====================== API CLIENT ======================
# OpenAI-compatible client pointed at x.ai's Grok endpoint.
# "dummy" is used as a placeholder so the app loads even before a key is pasted.
client = OpenAI(
    api_key=st.session_state.grok_key or "dummy", base_url="https://api.x.ai/v1"
)


# ====================== TOOLS ======================
# These are the real-world actions the agent can take.
# Each function here maps to a tool definition in the `tools` list below.
# When the agent decides to call a tool, the matching function runs and returns a result.

def web_search(query: str) -> str:
    """Search DuckDuckGo and return the top 3 results as plain text."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except:
        return "Web search failed — using cached knowledge."


def get_current_datetime() -> str:
    """Return the current date and time as a string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_to_memory(key: str, value: str) -> str:
    """Persist a key-value pair to Replit's built-in database (survives restarts)."""
    db[key] = value
    return f"Saved '{key}' to long-term memory."


def load_from_memory(key: str) -> str:
    """Retrieve a previously saved value from Replit's database."""
    return db.get(key, "No data found for that key.")


# Tool schema — this is what gets sent to the Grok API so it knows which tools are available.
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_memory",
            "description": "Save information to long-term memory",
            "parameters": {
                "type": "object",
                "properties": {"key": {"type": "string"}, "value": {"type": "string"}},
                "required": ["key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "load_from_memory",
            "description": "Load information from long-term memory",
            "parameters": {
                "type": "object",
                "properties": {"key": {"type": "string"}},
                "required": ["key"],
            },
        },
    },
]

# Maps tool names (strings) to the actual Python functions above.
tool_map = {
    "web_search": web_search,
    "get_current_datetime": get_current_datetime,
    "save_to_memory": save_to_memory,
    "load_from_memory": load_from_memory,
}


# ====================== MEMORY / CONVERSATION STATE ======================
# messages holds the full conversation history sent to the API each turn.
# trace holds a human-readable log of what the agent did — shown in the UI.
# Both reset automatically when the user switches agents.
if (
    "messages" not in st.session_state
    or st.session_state.get("current_agent") != selected_agent_name
):
    st.session_state.messages = [
        {"role": "system", "content": selected_agent["system_prompt"]}
    ]
    st.session_state.current_agent = selected_agent_name
    st.session_state.trace = []


# ====================== CHAT INPUT ======================
# This is the text box at the bottom of the page.
# Input flows through guardrails before anything is sent to the agent.
user_input = st.chat_input("What do you need help with today?")

# Step 1: Check guardrails — block or flag the message before the agent sees it.
if user_input:
    if not st.session_state.grok_key:
        st.error("Please paste your Grok API key in the sidebar first.")
    else:
        blocked, block_reason = check_guardrails(user_input)
        if blocked:
            st.session_state.trace.append(
                {"step": "Guardrail Applied", "content": block_reason}
            )
        elif needs_email_confirmation(user_input) or needs_risky_confirmation(user_input):
            # Pause and ask the user to confirm before proceeding.
            st.session_state.pending_input = user_input
            st.session_state.pending_confirmed = False
        else:
            # Safe to proceed immediately.
            st.session_state.pending_input = user_input
            st.session_state.pending_confirmed = True

# Step 2: If the message is waiting for human confirmation, show the approval UI.
if st.session_state.pending_input and not st.session_state.pending_confirmed:
    _pending = st.session_state.pending_input
    _is_email = needs_email_confirmation(_pending)
    _is_risky = needs_risky_confirmation(_pending)
    _label = "email" if _is_email else "high-risk action"
    st.warning(
        f"⚠️ **Guardrail pause** — your request involves a {_label}.\n\n"
        f"> *\"{_pending}\"*\n\nDo you want to proceed?"
    )
    col_yes, col_no, _ = st.columns([1, 1, 4])
    with col_yes:
        if st.button("✅ Confirm", type="primary"):
            st.session_state.pending_confirmed = True
            st.session_state.trace.append(
                {"step": "Guardrail Applied", "content": f"High-risk action approved by user: \"{_pending}\""}
            )
            st.rerun()
    with col_no:
        if st.button("❌ Cancel"):
            st.session_state.trace.append(
                {"step": "Guardrail Applied", "content": f"High-risk action cancelled by user: \"{_pending}\""}
            )
            st.session_state.pending_input = None
            st.session_state.pending_confirmed = False
            st.rerun()


# ====================== ReAct AGENT LOOP ======================
# This is the core of how the agent works — the ReAct pattern:
#   1. The agent receives the user message and REASONS about what to do (Plan).
#   2. If it decides to use a tool, it calls one (Act).
#   3. The tool result is fed back to the agent, which then REFLECTS and replies (Reflect).
# This loop can repeat multiple times in one turn if the agent needs to chain tool calls.
if st.session_state.pending_input and st.session_state.pending_confirmed:
    _exec_input = st.session_state.pending_input
    st.session_state.pending_input = None
    st.session_state.pending_confirmed = False

    # Add the user's message to the conversation history.
    st.session_state.messages.append({"role": "user", "content": _exec_input})
    st.session_state.trace.append({"step": "User", "content": _exec_input})

    # st.status shows live, expandable progress so the user knows exactly
    # what the agent is doing at each phase (Plan → Act → Reflect).
    with st.status(
        f"{selected_agent['icon']} {selected_agent_name} is working on it...",
        expanded=True,
    ) as status:

        # --- Plan step: ask the model what to do ---
        st.write("📋 **Planning** — figuring out the best approach...")
        response = client.chat.completions.create(
            model="grok-beta",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3,
        )
        add_cost(response.usage)
        msg = response.choices[0].message
        st.session_state.messages.append(msg.model_dump())

        # --- Act step: if the model requested a tool, run it ---
        if msg.tool_calls:
            # Friendly per-tool labels so users see what's actually happening.
            _TOOL_LABELS = {
                "web_search": "🔍 **Searching the web** for current info...",
                "get_current_datetime": "🕒 **Checking the date and time**...",
                "save_to_memory": "💾 **Saving** something to remember for later...",
                "load_from_memory": "📂 **Looking up** something I remembered earlier...",
            }
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                st.write(_TOOL_LABELS.get(tool_name, f"🔧 **Using a tool** ({tool_name})..."))
                st.session_state.trace.append(
                    {"step": "Tool Call", "content": f"Calling {tool_name}({args})"}
                )
                try:
                    result = tool_map[tool_name](**args)
                    st.session_state.trace.append(
                        {"step": "Tool Result", "content": result}
                    )
                    # Feed the tool result back into the conversation.
                    st.session_state.messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": tool_name,
                            "content": result,
                        }
                    )
                except Exception as e:
                    st.session_state.trace.append(
                        {"step": "Tool Error", "content": str(e)}
                    )

            # --- Reflect step: ask the model to summarise what it found ---
            st.write("✍️ **Writing your answer** based on what I found...")
            final_response = client.chat.completions.create(
                model="grok-beta",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto",
            )
            add_cost(final_response.usage)
            final_msg = final_response.choices[0].message
            st.session_state.messages.append(final_msg.model_dump())
            st.session_state.trace.append(
                {"step": "Final Reflection", "content": final_msg.content}
            )
        else:
            # No tool needed — the agent answered directly from its own knowledge.
            st.write("✍️ **Writing your answer**...")
            st.session_state.trace.append(
                {"step": "Final Reflection", "content": msg.content}
            )

        status.update(label="✅ Done!", state="complete", expanded=False)
        st.session_state.tasks_completed += 1


# ====================== STARTER PROMPTS ======================
# Show 3 example prompts ABOVE the conversation so first-time users
# aren't staring at a blank chat box wondering what to ask.
# Clicking one fills the chat with that prompt and runs it through guardrails normally.
if not st.session_state.messages or len(st.session_state.messages) <= 1:
    st.markdown(
        '<div class="section-label">Try one of these to get started</div>',
        unsafe_allow_html=True,
    )
    _starter_prompts = selected_agent.get("starter_prompts", [])
    _sp_cols = st.columns(len(_starter_prompts) or 1)
    for _idx, _prompt in enumerate(_starter_prompts):
        with _sp_cols[_idx]:
            if st.button(
                f"💬 {_prompt}",
                key=f"starter_{selected_agent_name}_{_idx}",
                use_container_width=True,
            ):
                # Run the chosen prompt through the same guardrail flow as typed input.
                blocked, block_reason = check_guardrails(_prompt)
                if blocked:
                    st.session_state.trace.append(
                        {"step": "Guardrail Applied", "content": block_reason}
                    )
                elif needs_email_confirmation(_prompt) or needs_risky_confirmation(_prompt):
                    st.session_state.pending_input = _prompt
                    st.session_state.pending_confirmed = False
                else:
                    st.session_state.pending_input = _prompt
                    st.session_state.pending_confirmed = True
                st.rerun()


# ====================== WATCH YOUR AGENT THINK ======================
# Shows every step the agent took, in plain English so non-technical users
# can follow along. In Literacy Mode, each step also includes a short explanation.
st.subheader(f"{selected_agent['icon']} Watch your agent think")
if not st.session_state.trace:
    st.caption(
        "Send a message below and you'll see every step your agent takes here — "
        "planning, searching, and writing your answer in real time."
    )

# Plain-English labels for each step type (shown to all users).
_STEP_LABELS = {
    "User":             ("👤", "You asked"),
    "Tool Call":        ("🔍", "Used a tool"),
    "Tool Result":      ("📥", "Information found"),
    "Tool Error":       ("⚠️", "Tool problem"),
    "Final Reflection": ("🤖", "Agent's answer"),
}

# Literacy Mode explanations — shown next to each step when the toggle is ON.
_LITERACY_EXPLANATIONS = {
    "Final Reflection": (
        "💡 **This is the Reflect step** — after gathering information, the agent reviews everything "
        "and writes a final answer. Reviewing its own work is what makes this an agent, not just a chatbot."
    ),
    "Tool Call": (
        "🔧 **This is the Act step** — the agent decided it needed real-world information "
        "and used a tool to get it. You're watching live tool use, not a simulation."
    ),
    "Tool Result": (
        "📥 **The tool returned data** — the agent now has fresh information and will use it "
        "to write your answer."
    ),
}

for entry in st.session_state.trace:
    _step = entry["step"]
    _icon, _label = _STEP_LABELS.get(_step, ("•", _step))

    if _step == "User":
        st.info(f"{_icon} **{_label}:** {entry['content']}")
    elif _step == "Tool Call":
        st.warning(f"{_icon} **{_label}:** {entry['content']}")
        if literacy_mode:
            st.caption(_LITERACY_EXPLANATIONS["Tool Call"])
    elif _step == "Tool Result":
        st.success(f"{_icon} **{_label}:** {entry['content']}")
        if literacy_mode:
            st.caption(_LITERACY_EXPLANATIONS["Tool Result"])
    elif _step == "Guardrail Applied":
        st.markdown(
            f'<span class="guardrail-trace">🛡️ Safety rule kicked in</span><br>{entry["content"]}',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(f"{_icon} **{_label}:** {entry['content']}")
        if literacy_mode and _step in _LITERACY_EXPLANATIONS:
            st.caption(_LITERACY_EXPLANATIONS[_step])


# ====================== CONVERSATION HISTORY ======================
# A clean chat-style view of just the back-and-forth between you and the agent.
st.subheader("💬 Your conversation")
_has_chat = any(
    m["role"] == "user" or (m["role"] == "assistant" and m.get("content"))
    for m in st.session_state.messages
)
if not _has_chat:
    st.caption("Your conversation with the agent will appear here once you send your first message.")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant" and msg.get("content"):
        st.chat_message("assistant").write(msg["content"])
