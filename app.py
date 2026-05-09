import streamlit as st
from openai import OpenAI
import json
import datetime
from duckduckgo_search import DDGS
from replit import db

# ====================== AGENT CONFIG (the hub) ======================
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

# ====================== CONFIG & UI ======================
st.set_page_config(page_title="Agent-in-a-Box Hub", page_icon="🧬", layout="wide")
st.title("🧬 Agent-in-a-Box: Multi-Template Hub")
st.markdown(
    "**Real agentic AI powered by Grok** — fork once, switch between 4 agents instantly. Watch them plan, call tools, act, and reflect. Literacy Mode teaches you how agents really work."
)

# API key
if "grok_key" not in st.session_state:
    st.session_state.grok_key = ""
grok_key = st.text_input(
    "Paste your Grok API key (xAI)", type="password", value=st.session_state.grok_key
)
if grok_key:
    st.session_state.grok_key = grok_key

client = OpenAI(api_key=grok_key or "dummy", base_url="https://api.x.ai/v1")

# Agent selector
selected_agent_name = st.sidebar.selectbox(
    "Choose your Agent",
    options=list(AGENTS.keys()),
    format_func=lambda x: f"{AGENTS[x]['icon']} {x}",
)
selected_agent = AGENTS[selected_agent_name]

# Literacy Mode (education moat)
literacy_mode = st.sidebar.toggle(
    "🧠 Agent Literacy Mode (show explanations)", value=True
)


# ====================== TOOLS (shared) ======================
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

# ====================== UI CONTROLS ======================
st.sidebar.header("Controls")
if st.sidebar.button("Clear Memory & Trace"):
    st.session_state.trace = []
    st.session_state.messages = [
        {"role": "system", "content": selected_agent["system_prompt"]}
    ]
    st.rerun()

user_input = st.chat_input("What do you need help with today?")

if user_input:
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
                "Tool Call": "🔧 **This is real tool calling** — the agent decided to act in the world (search, save memory, etc.). No more fake steps.",
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
