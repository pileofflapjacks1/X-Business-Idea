import streamlit as st
from openai import OpenAI
import json
import datetime
from duckduckgo_search import DDGS
from replit import db

# ====================== YOUR ORIGINAL AESTHETICS (preserved 100%) ======================
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
</style>
""",
    unsafe_allow_html=True,
)

# ====================== AGENT CONFIG ======================
AGENTS = {
    "Life Admin Executor": {
        "icon": "🏠",
        "system_prompt": "You are a helpful Life Admin Executor. Always plan first, use tools when needed, reflect on results, and be concise. Focus on daily life tasks, scheduling, reminders, info lookup.",
    },
    "Micro-CFO": {
        "icon": "💰",
        "system_prompt": "You are a Micro-CFO for personal finances. Be data-driven and truth-seeking. Analyze expenses, suggest budgets, track spending. Use tools for market data or calculations.",
    },
    "Habit Builder": {
        "icon": "🔥",
        "system_prompt": "You are a Habit Builder coach. Help users build, track, and reflect on habits. Use memory tools to persist progress. Be encouraging but realistic.",
    },
    "Career Resilience Coach": {
        "icon": "🚀",
        "system_prompt": "You are a Career Resilience Coach. Help with job search, skill gaps, networking advice. Use web search for real-time opportunities and market trends.",
    },
}

# ====================== UI SETUP ======================
st.set_page_config(page_title="Agent-in-a-Box Hub", page_icon="🧬", layout="wide")

# HERO (using your original styling)
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
  Every response you see below follows this pattern.
</p>""",
    },
    {
        "label": "Step 2 of 3 • Try your first agent",
        "title": "Send your first message",
        "body": (
            "Pick any agent from the sidebar, paste your API key, then try this starter prompt — "
            "or write your own. The agent will plan, search, and reply in seconds."
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

# Feature cards (using your .card class)
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
            <p>Ready-to-run personal agent that plans, uses real tools, remembers, and reflects.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ====================== GUARDRAILS SESSION STATE ======================
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
    "pending_input": None,
    "pending_confirmed": False,
}.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ====================== COST HELPERS ======================
GROK_COST_INPUT  = 5.0  / 1_000_000   # $ per input token
GROK_COST_OUTPUT = 15.0 / 1_000_000   # $ per output token

def add_cost(usage):
    if usage:
        st.session_state.session_cost += (
            getattr(usage, "prompt_tokens", 0)    * GROK_COST_INPUT +
            getattr(usage, "completion_tokens", 0) * GROK_COST_OUTPUT
        )

def cost_badge_class(cost, limit):
    if cost >= limit:
        return "cost-badge cost-badge-danger"
    if cost >= limit * 0.75:
        return "cost-badge cost-badge-warn"
    return "cost-badge"

# ====================== GUARDRAIL HELPERS ======================
SPEND_KEYWORDS  = ["buy", "purchase", "order", "pay", "charge", "subscribe", "checkout", "spend"]
EMAIL_KEYWORDS  = ["send email", "email to", "draft email", "compose email", "mail to", "send a message to"]
RISKY_KEYWORDS  = SPEND_KEYWORDS + ["delete", "remove", "post", "submit", "transfer", "share", "send"]

def input_contains(text, keywords):
    low = text.lower()
    return any(kw in low for kw in keywords)

def check_guardrails(user_text):
    """Returns (blocked: bool, reason: str | None)"""
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
    return st.session_state.guardrail_ask_email and input_contains(user_text, EMAIL_KEYWORDS)

def needs_risky_confirmation(user_text):
    return st.session_state.guardrail_approve_risky and input_contains(user_text, RISKY_KEYWORDS)

# Sidebar: API key + controls
with st.sidebar:
    st.header("🔑 Get Started")
    grok_key = st.text_input(
        "Paste your Grok API key (free at x.ai)",
        type="password",
        value=st.session_state.grok_key,
        help="Get your key at https://x.ai/api — it stays in your browser only.",
    )
    if grok_key:
        st.session_state.grok_key = grok_key
        st.success("✅ Key saved for this session")

    # ── Safety Guardrails ──
    st.markdown(
        """
<div class="guardrails-panel">
  <div class="guardrails-title">🛡️ Safety Guardrails</div>
  <div class="guardrails-sub">Rules that protect you every session</div>
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
    st.markdown(
        f'**Max spend this session** <span class="{_badge_cls}">${_cost:.4f} / ${_limit:.2f}</span>',
        unsafe_allow_html=True,
    )
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
    selected_agent_name = st.selectbox(
        "Choose your Agent",
        options=list(AGENTS.keys()),
        format_func=lambda x: f"{AGENTS[x]['icon']} {x}",
    )
    selected_agent = AGENTS[selected_agent_name]

    literacy_mode = st.toggle("🧠 Agent Literacy Mode (show explanations)", value=True)

    st.divider()
    st.header("Controls")
    if st.button("Clear Memory & Trace"):
        st.session_state.trace = []
        st.session_state.session_cost = 0.0
        st.session_state.pending_input = None
        st.session_state.pending_confirmed = False
        st.session_state.messages = [
            {"role": "system", "content": selected_agent["system_prompt"]}
        ]
        st.rerun()

# API client
client = OpenAI(
    api_key=st.session_state.grok_key or "dummy", base_url="https://api.x.ai/v1"
)


# ====================== TOOLS ======================
def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except:
        return "Web search failed — using cached knowledge."


def get_current_datetime() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_to_memory(key: str, value: str) -> str:
    db[key] = value
    return f"Saved '{key}' to long-term memory."


def load_from_memory(key: str) -> str:
    return db.get(key, "No data found for that key.")


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

tool_map = {
    "web_search": web_search,
    "get_current_datetime": get_current_datetime,
    "save_to_memory": save_to_memory,
    "load_from_memory": load_from_memory,
}

# ====================== SESSION STATE ======================
if (
    "messages" not in st.session_state
    or st.session_state.get("current_agent") != selected_agent_name
):
    st.session_state.messages = [
        {"role": "system", "content": selected_agent["system_prompt"]}
    ]
    st.session_state.current_agent = selected_agent_name
    st.session_state.trace = []

# ====================== CHAT ======================
user_input = st.chat_input("What do you need help with today?")

# ── Handle new user input: store as pending if confirmation needed ──
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
            st.session_state.pending_input = user_input
            st.session_state.pending_confirmed = False
        else:
            st.session_state.pending_input = user_input
            st.session_state.pending_confirmed = True

# ── Show confirmation prompt for pending high-risk / email actions ──
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

# ── Execute confirmed input ──
if st.session_state.pending_input and st.session_state.pending_confirmed:
    _exec_input = st.session_state.pending_input
    st.session_state.pending_input = None
    st.session_state.pending_confirmed = False

    st.session_state.messages.append({"role": "user", "content": _exec_input})
    st.session_state.trace.append({"step": "User", "content": _exec_input})

    with st.spinner(f"{selected_agent['icon']} {selected_agent_name} thinking..."):
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

        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                st.session_state.trace.append(
                    {"step": "Tool Call", "content": f"Calling {tool_name}({args})"}
                )
                try:
                    result = tool_map[tool_name](**args)
                    st.session_state.trace.append(
                        {"step": "Tool Result", "content": result}
                    )
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
            st.session_state.trace.append(
                {"step": "Final Reflection", "content": msg.content}
            )

# ====================== DISPLAY ======================
st.subheader(f"{selected_agent['icon']} Agent Trace — {selected_agent_name}")
for entry in st.session_state.trace:
    if entry["step"] == "User":
        st.info(f"👤 **User**: {entry['content']}")
    elif entry["step"] == "Tool Call":
        st.warning(f"🔧 **Tool Called**: {entry['content']}")
    elif entry["step"] == "Tool Result":
        st.success(f"✅ **Tool Result**: {entry['content']}")
    elif entry["step"] == "Guardrail Applied":
        st.markdown(
            f'<span class="guardrail-trace">🛡️ Guardrail Applied</span><br>{entry["content"]}',
            unsafe_allow_html=True,
        )
    else:
        content = entry["content"]
        if literacy_mode:
            explanation = {
                "Final Reflection": "🤖 **This is the Reflection step** — agents review what happened and decide next actions. This is what makes them truly agentic.",
                "Tool Call": "🔧 **This is real tool calling** — the agent decided to act in the world.",
            }.get(entry["step"], "")
            st.markdown(f"**{entry['step']}**: {content}\n\n{explanation}")
        else:
            st.markdown(f"**{entry['step']}**: {content}")

st.subheader("Live Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant" and msg.get("content"):
        st.chat_message("assistant").write(msg["content"])
