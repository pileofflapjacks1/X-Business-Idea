import streamlit as st
from openai import OpenAI
import os
import json
import time

st.set_page_config(page_title="Agent-in-a-Box", page_icon="📦", layout="wide")
st.title("🧠 Agent-in-a-Box")
st.subheader("Grok 4.3 Powered · Learn Agentic AI by Doing")

st.markdown("### Life Admin Executor — Your First Real Agent")

# === TEACHING SECTION ===
with st.expander("💡 What is an Agentic AI? (Learn while you use it)"):
    st.markdown("""
    **Agentic AI** = An AI that doesn't just answer questions. 
    It **plans**, **acts**, **reflects**, and **loops** until the goal is achieved.
    
    This template shows you the classic **ReAct pattern** (Reason + Act) in action.
    Watch the steps below to learn how real agents work!
    """)

# API Key handling — prefer env var (Replit Secret), fall back to manual entry
_env_key = os.environ.get("GROK_API_KEY", "")
if _env_key and 'grok_key' not in st.session_state:
    st.session_state.grok_key = _env_key

if 'grok_key' not in st.session_state:
    col1, col2 = st.columns([3,1])
    with col1:
        api_key = st.text_input("Enter your xAI Grok API Key to activate the agent", type="password", help="Get your key at https://console.x.ai")
    with col2:
        if st.button("Save Key & Activate Agent", type="primary"):
            if len(api_key) > 20:
                st.session_state.grok_key = api_key
                st.success("✅ Agent activated! Grok is ready.")
                st.rerun()
            else:
                st.error("Please enter a valid Grok API key")
else:
    st.success("✅ Grok Agent is Ready")

if 'grok_key' in st.session_state:
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=st.session_state.grok_key)
    
    task = st.text_area("What life admin task do you want the agent to handle?", 
                       height=120, 
                       placeholder="Cancel my gym membership, negotiate a lower rate, and recommend better alternatives near me...")

    if st.button("🚀 Run Autonomous Agent", type="primary", use_container_width=True):
        if not task:
            st.warning("Please describe a task")
        else:
            with st.spinner("Agent is working autonomously..."):
                # Initialize chat history for the agent
                messages = [
                    {"role": "system", "content": """You are an autonomous Life Admin Executor Agent powered by Grok.
You are proactive, thorough, and helpful. 
Follow the ReAct pattern strictly:
1. Think step-by-step (Plan)
2. Take action or give clear next steps
3. Reflect on whether the goal is complete

Respond in this exact JSON format every turn:
{
  "plan": "Your detailed plan for this step",
  "action": "What you are doing or the output for the user",
  "reflection": "Is the task complete? What next?",
  "complete": true or false
}"""}
                ]
                
                messages.append({"role": "user", "content": f"Task: {task}" })
                
                max_iterations = 5
                full_response = ""
                
                for iteration in range(1, max_iterations + 1):
                    st.markdown(f"**Iteration {iteration}/{max_iterations}**")
                    
                    response = client.chat.completions.create(
                        model="grok-4.3",
                        messages=messages,
                        temperature=0.7,
                    )
                    
                    try:
                        content = response.choices[0].message.content
                        result = json.loads(content)
                        
                        # Display the agent's thinking visibly
                        st.markdown(f"**🧩 Plan:** {result.get('plan', '')}")
                        st.markdown(f"**⚡ Action:** {result.get('action', '')}")
                        st.markdown(f"**🔄 Reflection:** {result.get('reflection', '')}")
                        
                        full_response += f"**Iteration {iteration}**\nPlan: {result.get('plan')}\nAction: {result.get('action')}\n\n"
                        
                        messages.append({"role": "assistant", "content": content})
                        
                        if result.get("complete", False):
                            st.success("✅ Task completed by the agent!")
                            break
                            
                    except json.JSONDecodeError:
                        st.write("Raw output:", content)
                        break
                    
                    time.sleep(0.8)  # Small pause so user can read each step
                
                st.divider()
                st.subheader("Final Result")
                st.write(full_response)
                
                st.info("This is what agentic AI looks like — planning, acting, reflecting, and looping until the job is done.")

st.divider()
st.caption("Agent-in-a-Box by pileofflapjacks1 · Teaching agentic AI through real, working templates")