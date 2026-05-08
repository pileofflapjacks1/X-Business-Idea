import streamlit as st
import os
from openai import OpenAI
import json
import time

st.set_page_config(page_title="Agent-in-a-Box", page_icon="🧠", layout="wide")

st.title("🧠 Agent-in-a-Box")
st.markdown("**Grok 4.3 Powered · Learn Agentic AI by Doing**")
st.subheader("Life Admin Executor — Your First Real Agent")

# Preview Mode (no key needed)
st.markdown("### 🚀 Try Demo Mode — See Agentic AI in Action (No Key Needed)")
with st.expander("💡 What is an Agentic AI? (Learn while you use it)", expanded=True):
    st.write("An agentic AI plans, acts, reflects, and loops until the job is done. Watch it happen live below!")

if 'preview_task' not in st.session_state:
    st.session_state.preview_task = ""

preview_task = st.text_input("Describe a life-admin task (e.g. 'Cancel my gym membership')", value=st.session_state.preview_task, key="preview_input")
if st.button("Run Preview Agent", type="primary"):
    if preview_task:
        st.session_state.preview_task = preview_task
        st.info("Running simulated agentic loop...")
        # Simulate ReAct loop
        steps = [
            {"step": "🧩 Plan", "content": "I will break this task into steps and gather any needed info."},
            {"step": "⚡ Action", "content": "Drafting email to gym and researching alternatives."},
            {"step": "🔄 Reflection", "content": "Task is 60% complete. Need to check for better options."},
            {"step": "🧩 Plan", "content": "Suggest 2 better gym alternatives with pros/cons."},
            {"step": "⚡ Action", "content": "Completed full task with email draft and recommendations."}
        ]
        for i, step in enumerate(steps):
            with st.spinner(f"Step {i+1}/5: {step['step']}"):
                time.sleep(1.5)
                st.write(f"**{step['step']}**: {step['content']}")
        st.success("✅ Preview complete! This is what agentic AI looks like — planning, acting, reflecting, and looping until the job is done.")
        st.caption("You just experienced the core ReAct pattern that powers real agents.")
    else:
        st.warning("Please enter a task.")

# Monetization Teaser + Hosted Upsell (v2.4)
st.markdown("---")
st.markdown("### 🚀 **Upgrade to Hosted Agent — No API Key Needed!**")
st.markdown("**$19/mo** (or $15/mo annual — early bird for first 50 users)")
st.markdown("- Zero setup — we handle Grok API key & costs")
st.markdown("- Always-on dashboard with new templates every month")
st.markdown("- Priority support + lifetime updates")
st.markdown("- Perfect for busy people who want the magic without managing keys")
if st.button("Get Hosted Life Admin Executor Now (Gumroad Early Access)", type="secondary"):
    st.success("Redirecting to Gumroad... (link will be live once you set up your Gumroad product in #2)")

st.markdown("---")

# Real Agent Activation (with key)
st.markdown("### Enter your xAI Grok API Key to activate the real agent")
st.markdown("**Don't have a key yet?** Good news — it takes 2 minutes and xAI gives $25 free credit.")
if st.button("Open xAI Console & Get Key Now", type="primary"):
    st.link_button("Open xAI Console", "https://console.x.ai/")

api_key = st.text_input("Your GROK_API_KEY", type="password", value=os.getenv("GROK_API_KEY", ""))

if st.button("Save Key & Activate Agent"):
    if api_key:
        os.environ["GROK_API_KEY"] = api_key
        st.success("Key saved! Agent activated.")
        # Here the real ReAct loop would go for full agent
        st.info("Real agent loop would run here with Grok-4.3 (full version in next push if needed).")
    else:
        st.warning("Please enter your key.")

st.caption("Agent-in-a-Box by pileofflapjacks1 · Teaching agentic AI through real, working templates")

# Requirements note for Replit
st.sidebar.info("Make sure to add GROK_API_KEY in Replit Secrets for full agent mode.")
