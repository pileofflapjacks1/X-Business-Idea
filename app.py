import streamlit as st
from openai import OpenAI
import os
import json
import time
import random

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

# === DEMO MODE SECTION (No key required) ===
st.markdown("### 🎮 Try Demo Mode First (No API Key Needed)")
st.caption("Experience the full agentic loop instantly — see exactly what you'll get with the real agent.")

if 'demo_active' not in st.session_state:
    st.session_state.demo_active = False

if st.button("🚀 Try Interactive Demo Now", type="secondary", use_container_width=True):
    st.session_state.demo_active = True
    st.rerun()

if st.session_state.demo_active:
    demo_task = st.text_area("What life admin task would you like the demo agent to handle?", 
                           height=100, 
                           placeholder="Cancel my gym membership and negotiate a better rate...")
    
    if st.button("Run Demo Agent", type="primary", use_container_width=True):
        if not demo_task:
            st.warning("Please describe a task")
        else:
            with st.spinner("Demo agent is working autonomously... (simulated)"):
                st.info("🔬 This is a **simulated preview** of the real Grok agent.")
                
                # Simulated ReAct loop
                max_iterations = 4
                full_response = ""
                
                for iteration in range(1, max_iterations + 1):
                    st.markdown(f"**Iteration {iteration}/{max_iterations}**")
                    
                    # Realistic simulated responses
                    plans = [
                        "Analyzing the task and breaking it down into clear steps",
                        "Gathering necessary information and preparing documents",
                        "Drafting communication and identifying negotiation points",
                        "Reviewing outcomes and suggesting next actions"
                    ]
                    actions = [
                        "Identifying key information needed from user and relevant templates",
                        "Drafting a professional cancellation email",
                        "Preparing negotiation script and alternatives research",
                        "Compiling final summary and recommendations"
                    ]
                    reflections = [
                        "Task is progressing well. Need more specific details to continue.",
                        "Draft is complete. Ready for user review and sending.",
                        "Negotiation points identified. Goal partially complete.",
                        "All steps completed successfully."
                    ]
                    
                    st.markdown(f"**🧩 Plan:** {plans[(iteration-1) % len(plans)]}")
                    st.markdown(f"**⚡ Action:** {actions[(iteration-1) % len(actions)]}")
                    st.markdown(f"**🔄 Reflection:** {reflections[(iteration-1) % len(reflections)]}")
                    
                    full_response += f"**Iteration {iteration}**\nPlan: {plans[(iteration-1) % len(plans)]}\nAction: {actions[(iteration-1) % len(actions)]}\n\n"
                    
                    time.sleep(1.2)
                    
                    if iteration >= 3:
                        st.success("✅ Demo task completed by the agent!")
                        break
                
                st.divider()
                st.subheader("Demo Final Result")
                st.write(full_response)
                st.info("This is what agentic AI looks like — planning, acting, reflecting, and looping until the job is done.\n\n**Ready for the real thing?** Activate the full Grok-powered agent below.")

st.divider()

# === REAL AGENT SECTION ===
st.markdown("### 🔑 Full Grok-Powered Agent")

# API Key handling
_env_key = os.environ.get("GROK_API_KEY", "")
if _env_key and 'grok_key' not in st.session_state:
    st.session_state.grok_key = _env_key

if 'grok_key' not in st.session_state:
    st.info("**Don't have a Grok API key yet?**")
    st.markdown("[Open xAI Console & Get Your Free Key →](https://console.x.ai) (takes ~2 minutes)")
    
    col1, col2 = st.columns([3,1])
    with col1:
        api_key = st.text_input("Enter your xAI Grok API Key to activate the full agent", type="password", help="Your key is stored only in this Replit session")
    with col2:
        if st.button("Save Key & Activate Full Agent", type="primary"):
            if len(api_key) > 20:
                st.session_state.grok_key = api_key
                st.success("✅ Full Grok Agent activated!")
                st.rerun()
            else:
                st.error("Please enter a valid Grok API key")
else:
    st.success("✅ Full Grok 4.3 Agent is Ready")

if 'grok_key' in st.session_state:
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=st.session_state.grok_key)
    
    task = st.text_area("What life admin task do you want the **real** agent to handle?", 
                       height=120, 
                       placeholder="Cancel my gym membership, negotiate a lower rate, and recommend better alternatives...")

    if st.button("🚀 Run Real Autonomous Agent", type="primary", use_container_width=True):
        if not task:
            st.warning("Please describe a task")
        else:
            with st.spinner("Real agent is working autonomously..."):
                # [Existing real agent code remains the same]
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
                        
                        st.markdown(f"**🧩 Plan:** {result.get('plan', '')}")
                        st.markdown(f"**⚡ Action:** {result.get('action', '')}")
                        st.markdown(f"**🔄 Reflection:** {result.get('reflection', '')}")
                        
                        full_response += f"**Iteration {iteration}**\\nPlan: {result.get('plan')}\\nAction: {result.get('action')}\\n\\n"
                        
                        messages.append({"role": "assistant", "content": content})
                        
                        if result.get("complete", False):
                            st.success("✅ Task completed by the real agent!")
                            break
                            
                    except json.JSONDecodeError:
                        st.write("Raw output:", content)
                        break
                    
                    time.sleep(0.8)
                
                st.divider()
                st.subheader("Final Result")
                st.write(full_response)
                
                st.info("This is what agentic AI looks like — planning, acting, reflecting, and looping until the job is done.")

st.divider()
st.caption("Agent-in-a-Box by pileofflapjacks1 · Teaching agentic AI through real, working templates")
