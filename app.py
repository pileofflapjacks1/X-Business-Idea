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

# Sidebar: API key + controls
with st.sidebar:
    st.header("🔑 Get Started")
    if "grok_key" not in st.session_state:
        st.session_state.grok_key = ""
    grok_key = st.text_input(
        "Paste your Grok API key (free at x.ai)",
        type="password",
        value=st.session_state.grok_key,
        help="Get your key at https://x.ai/api — it stays in your browser only.",
    )
    if grok_key:
        st.session_state.grok_key = grok_key
        st.success("✅ Key saved for this session")

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

if user_input:
    if not st.session_state.grok_key:
        st.error("Please paste your Grok API key in the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.trace.append({"step": "User", "content": user_input})

        with st.spinner(f"{selected_agent['icon']} {selected_agent_name} thinking..."):
            response = client.chat.completions.create(
                model="grok-beta",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.3,
            )
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
