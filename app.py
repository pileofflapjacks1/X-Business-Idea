import streamlit as st
from openai import OpenAI
import os
import json
import time

st.set_page_config(page_title="Life Admin Executor", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* Global font & background */
    html, body, [class*="css"] {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    .main > div { padding-top: 0rem; }
    .block-container { padding: 2rem 3rem 3rem; max-width: 960px; margin: auto; }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 60%, #0e4a6e 100%);
        border-radius: 16px;
        padding: 3rem 3rem 2.5rem;
        margin-bottom: 2.5rem;
        text-align: center;
        color: white;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(99,179,237,0.2);
        color: #90cdf4;
        border: 1px solid rgba(99,179,237,0.4);
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 0.3rem 0.9rem;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0 0 0.75rem;
        line-height: 1.15;
    }
    .hero p {
        font-size: 1.1rem;
        color: #94a3b8;
        max-width: 620px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* Cards */
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .card h3 {
        font-size: 1rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 0.4rem;
    }
    .card p { color: #64748b; font-size: 0.92rem; margin: 0; line-height: 1.6; }

    /* Step pills in the ReAct loop */
    .step-pill {
        display: inline-block;
        border-radius: 8px;
        padding: 0.25rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .step-plan   { background:#eff6ff; color:#1d4ed8; border:1px solid #bfdbfe; }
    .step-action { background:#f0fdf4; color:#15803d; border:1px solid #bbf7d0; }
    .step-reflect{ background:#fdf4ff; color:#7e22ce; border:1px solid #e9d5ff; }

    /* Divider label */
    .section-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #94a3b8;
        margin: 2rem 0 0.8rem;
    }

    /* Key input panel */
    .key-panel {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.5rem;
    }
    .key-panel p { font-size: 0.9rem; color: #475569; margin: 0 0 0.8rem; }

    /* Pricing strip */
    .pricing-strip {
        background: linear-gradient(135deg, #0f172a, #1e3a5f);
        border-radius: 12px;
        padding: 1.8rem 2rem;
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2rem;
    }
    .pricing-strip h3 { margin: 0; font-size: 1.1rem; font-weight: 700; }
    .pricing-strip p  { margin: 0.3rem 0 0; font-size: 0.88rem; color: #94a3b8; }
    .price-tag {
        font-size: 1.8rem;
        font-weight: 800;
        color: #7dd3fc;
        white-space: nowrap;
    }
    .price-tag span { font-size: 0.9rem; font-weight: 500; color: #94a3b8; }

    /* Footer */
    .footer { text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2.5rem; }
    .footer a { color: #63b3ed; text-decoration: none; }

    /* Override Streamlit button styles */
    div.stButton > button[kind="primary"] {
        background: #1d4ed8;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        font-size: 0.95rem;
    }
    div.stButton > button[kind="primary"]:hover { background: #1e40af; }
    div.stButton > button[kind="secondary"] {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="badge">⚡ Powered by Grok &nbsp;·&nbsp; ReAct Agent Framework</div>
    <h1>Your AI Life Admin<br>Assistant</h1>
    <p>Describe any tedious life task and watch a real autonomous agent plan, act,
    and follow through — step by step, in real time.</p>
</div>
""", unsafe_allow_html=True)


# ── How it works ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""<div class="card">
        <h3>🧩 Plan</h3>
        <p>The agent breaks your goal into clear, logical steps before touching anything.</p>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown("""<div class="card">
        <h3>⚡ Act</h3>
        <p>It executes each step, drafting emails, doing research, and generating outputs.</p>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown("""<div class="card">
        <h3>🔄 Reflect</h3>
        <p>After each action it checks progress and loops until the job is genuinely done.</p>
    </div>""", unsafe_allow_html=True)


# ── API key handling ──────────────────────────────────────────────────────────
_env_key = os.environ.get("GROK_API_KEY", "")
if _env_key and "grok_key" not in st.session_state:
    st.session_state.grok_key = _env_key

if "grok_key" not in st.session_state:
    st.markdown('<div class="section-label">Connect your AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="key-panel"><p>Paste your xAI Grok API key to activate the agent. Your key is never stored outside this session.</p>', unsafe_allow_html=True)
    col_a, col_b = st.columns([4, 1])
    with col_a:
        api_key = st.text_input(
            "Grok API Key",
            type="password",
            placeholder="xai-...",
            label_visibility="collapsed",
        )
    with col_b:
        activate = st.button("Activate →", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
        "No key yet? [Get one free at console.x.ai](https://console.x.ai/) — new users receive $25 in free credit.",
        unsafe_allow_html=False,
    )
    if activate:
        if len(api_key) > 20:
            st.session_state.grok_key = api_key
            st.rerun()
        else:
            st.error("Please enter a valid API key (should start with xai-).")
else:
    st.success("Agent connected and ready.", icon="✅")


# ── Main agent UI ─────────────────────────────────────────────────────────────
if "grok_key" in st.session_state:
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=st.session_state.grok_key)

    st.markdown('<div class="section-label">Your task</div>', unsafe_allow_html=True)
    task = st.text_area(
        "Task",
        height=110,
        placeholder="e.g. Cancel my gym membership, negotiate a lower rate, and suggest two better alternatives near me...",
        label_visibility="collapsed",
    )

    col_run, col_clear = st.columns([5, 1])
    with col_run:
        run = st.button("⚡  Run Agent", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear key", use_container_width=True):
            del st.session_state.grok_key
            st.rerun()

    if run:
        if not task.strip():
            st.warning("Please describe a task first.")
        else:
            st.markdown('<div class="section-label">Agent working</div>', unsafe_allow_html=True)
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an autonomous Life Admin Executor Agent powered by Grok. "
                        "Follow the ReAct pattern strictly. "
                        "Respond only in this exact JSON format every turn:\n"
                        '{"plan":"…","action":"…","reflection":"…","complete":true|false}'
                    ),
                },
                {"role": "user", "content": f"Task: {task}"},
            ]

            max_iterations = 5
            full_result = []

            for i in range(1, max_iterations + 1):
                with st.spinner(f"Iteration {i} of {max_iterations}…"):
                    response = client.chat.completions.create(
                        model="grok-3",
                        messages=messages,
                        temperature=0.7,
                    )
                    content = response.choices[0].message.content

                try:
                    r = json.loads(content)
                except json.JSONDecodeError:
                    r = {"plan": "", "action": content, "reflection": "", "complete": True}

                st.markdown(f"""
<div class="card" style="margin-bottom:0.7rem;">
    <div style="margin-bottom:0.6rem;font-size:0.78rem;font-weight:700;color:#64748b;letter-spacing:0.06em;">ITERATION {i}</div>
    <div style="margin-bottom:0.5rem;">
        <span class="step-pill step-plan">Plan</span>
        <div style="color:#1e293b;font-size:0.93rem;margin-top:0.3rem;">{r.get('plan','')}</div>
    </div>
    <div style="margin-bottom:0.5rem;">
        <span class="step-pill step-action">Action</span>
        <div style="color:#1e293b;font-size:0.93rem;margin-top:0.3rem;">{r.get('action','')}</div>
    </div>
    <div>
        <span class="step-pill step-reflect">Reflect</span>
        <div style="color:#1e293b;font-size:0.93rem;margin-top:0.3rem;">{r.get('reflection','')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

                full_result.append(r)
                messages.append({"role": "assistant", "content": content})

                if r.get("complete", False):
                    break

                time.sleep(0.5)

            st.success("Task complete.", icon="✅")
            st.info(
                "You just watched a real ReAct agent — it plans, acts, and reflects in a loop until your goal is done. "
                "That's the foundation of all serious agentic AI systems.",
                icon="💡",
            )


# ── Learn more expander ────────────────────────────────────────────────────────
with st.expander("What makes this an 'agent' and not just a chatbot?"):
    st.markdown("""
A standard chatbot responds once and stops. An **agent** operates in a loop:

1. **Plan** — break the goal into concrete steps
2. **Act** — do something real toward that goal  
3. **Reflect** — check whether the goal is met; if not, plan again

This is the **ReAct pattern** (Reasoning + Acting), the same architecture behind
AutoGPT, Claude computer use, and most production AI agents. This template makes
it visible so you can learn it while using it.
""")


# ── Hosted upsell ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="pricing-strip">
    <div>
        <h3>Want this without managing API keys?</h3>
        <p>Fully hosted · Always-on dashboard · New templates monthly · We handle costs &amp; updates</p>
    </div>
    <div class="price-tag">$19<span>/mo</span></div>
</div>
""", unsafe_allow_html=True)

col_p1, col_p2 = st.columns([3, 1])
with col_p2:
    st.button("Get hosted access →", type="secondary", use_container_width=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer" style="margin-top:2rem;">
    Agent-in-a-Box · by <a href="#">pileofflapjacks1</a> · Teaching agentic AI through real, working templates
</div>
""", unsafe_allow_html=True)
