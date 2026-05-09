import streamlit as st
from openai import OpenAI
import json
import datetime
from duckduckgo_search import DDGS
from replit import db

# ====================== CONFIG ======================
st.set_page_config(page_title="Life Admin Executor", page_icon="🤖", layout="wide")
st.title("🧬 Agent-in-a-Box: Life Admin Executor")
st.markdown("**Real agentic AI powered by Grok** — watch it plan, call tools, act, and reflect.")

# API setup
if "grok_key" not in st.session_state:
    st.session_state.grok_key = ""

grok_key = st.text_input("Paste your Grok API key (xAI)", type="password", value=st.session_state.grok_key)
if grok_key:
    st.session_state.grok_key = grok_key

client = OpenAI(
    api_key=grok_key or "dummy",
    base_url="https://api.x.ai/v1"
)

# ====================== TOOLS ======================
def web_search(query: str) -> str:
    """Search the web for up-to-date information."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        return "\n".join([f"{r['title']}: {r['body']}" for r in results])
    except:
        return "Web search failed — using cached knowledge."

def get_current_datetime() -> str:
    """Return current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_memory(key: str, value: str) -> str:
    """Persist data in Replit DB (long-term memory)."""
    db[key] = value
    return f"Saved {key} to memory."

def load_from_memory(key: str) -> str:
    """Retrieve from Replit DB."""
    return db.get(key, "No data found for that key.")

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_memory",
            "description": "Save information to long-term memory",
            "parameters": {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "load_from_memory",
            "description": "Load information from long-term memory",
            "parameters": {"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}
        }
    }
]

# Tool executor map
tool_map = {
    "web_search": web_search,
    "get_current_datetime": get_current_datetime,
    "save_to_memory": save_to_memory,
    "load_from_memory": load_from_memory
}

# ====================== SESSION STATE ======================
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful Life Admin Executor. Always plan first, use tools when needed, reflect on results, and be concise."}]

if "trace" not in st.session_state:
    st.session_state.trace = []

# ====================== UI ======================
st.sidebar.header("Agent Controls")
if st.sidebar.button("Clear Memory & Trace"):
    st.session_state.trace = []
    st.session_state.messages = st.session_state.messages[:1]
    st.rerun()

user_input = st.chat_input("What do you need help with today?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.trace.append({"step": "User", "content": user_input})

    # Main agent loop
    with st.spinner("Agent thinking..."):
        response = client.chat.completions.create(
            model="grok-beta",
            messages=st.session_state.messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.3
        )

        msg = response.choices[0].message
        st.session_state.messages.append(msg.model_dump() if hasattr(msg, 'model_dump') else msg.dict())

        # Handle tool calls
        if msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                st.session_state.trace.append({"step": "Tool Call", "content": f"Calling {tool_name} with {args}"}) 

                try:
                    result = tool_map[tool_name](**args)
                    st.session_state.trace.append({"step": "Tool Result", "content": result})
                    st.session_state.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": str(result)
                    })
                except Exception as e:
                    st.session_state.trace.append({"step": "Tool Error", "content": str(e)})

            # Final completion after tools
            final_response = client.chat.completions.create(
                model="grok-beta",
                messages=st.session_state.messages,
                tools=tools,
                tool_choice="auto"
            )
            final_msg = final_response.choices[0].message
            st.session_state.messages.append(final_msg.model_dump() if hasattr(final_msg, 'model_dump') else final_msg.dict())
            st.session_state.trace.append({"step": "Final Reflection", "content": final_msg.content})
        else:
            st.session_state.trace.append({"step": "Final Reflection", "content": msg.content})

# ====================== DISPLAY ======================
st.subheader("Agent Trace (watch the magic)")
for entry in st.session_state.trace:
    if entry["step"] == "User":
        st.info(f"👤 **User**: {entry['content']}")
    elif entry["step"] == "Tool Call":
        st.warning(f"🔧 **Tool Called**: {entry['content']}")
    elif entry["step"] == "Tool Result":
        st.success(f"✅ **Tool Result**: {entry['content']}")
    else:
        st.markdown(f"🤖 **{entry['step']}**: {entry['content']}")

st.subheader("Live Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg.get("content", ""))