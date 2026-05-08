import streamlit as st
from openai import OpenAI
import os
import json
import time

st.set_page_config(page_title="Agent-in-a-Box", page_icon="📦", layout="wide")
st.title("🚀 Agent-in-a-Box")
st.subheader("Grok 4.3 Powered · Learn Agentic AI by Doing")

st.markdown("**First Template: Life Admin Executor**")
st.caption("Watch a real agent plan → act → reflect → complete your task")

# ====================== TEACHING SIDEBAR ======================
st.sidebar.title("🧠 How Agentic AI Works")
st.sidebar.markdown("""
### What you're about to see:

1. **Planning** - The agent thinks step-by-step
2. **Acting** - It generates useful output or next actions
3. **Reflecting** - It evaluates if the goal is achieved
4. **Looping** - It keeps going until the task is done

This is the core **agentic loop** that makes AI go from chatbot to autonomous agent.

**Your Grok-powered agent learns by doing** — just like you will.
""")

# API Key handling
if 'grok_key' not in st.session_state:
    st.info("🔑 First time? Enter your xAI Grok API key below.")
    api_key = st.text_input("Enter your xAI Grok API Key", type="password", placeholder="gsk_...")
    if st.button("Save Key & Continue", type="primary"):
        if api_key.startswith("gsk_") or len(api_key) > 20:
            st.session_state.grok_key = api_key
            st.success("✅ Key saved! Let's run your agent.")
            st.rerun()
        else:
            st.error("Please enter a valid xAI Grok API key")
else:
    st.success("✅ Grok API Key is connected")
    if st.sidebar.button("🔄 Reset API Key"):
        del st.session_state.grok_key
        st.rerun()

if 'grok_key' in st.session_state:
    client = OpenAI(
        base_url="https://api.x.ai/v1",
        api_key=st.session_state.grok_key
    )

    # Task input
    task = st.text_area(
        "What life admin task do you want the agent to handle?",
        height=110,
        placeholder="Cancel my gym membership, negotiate a better deal, and suggest good alternatives...",
        help="Be specific — good agents thrive on clear goals"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_button = st.button("🚀 Run Life Admin Executor", type="primary", use_container_width=True)
    with col2:
        st.caption("This may take 30–90 seconds as the agent loops")

    if run_button and task:
        with st.spinner("Agent is now thinking and working..."):
            st.divider()
            st.subheader("🔄 Agentic Execution Trace")

            # Initialize conversation history
            messages = [
                {"role": "system", "content": """You are an autonomous Life Admin Executor Agent powered by Grok.

CORE AGENTIC BEHAVIOR:
- You plan step-by-step
- You take clear actions (write emails, create plans, research, make decisions)
- You reflect on progress
- You continue looping until the user's goal is fully completed
- Show your thinking clearly using this format:
  THINK: [your reasoning]
  PLAN: [next step]
  ACTION: [what you are doing right now]
  RESULT: [what happened or output]

When the task is complete, end with FINAL ANSWER: [complete response to user]"""}
            ]

            messages.append({"role": "user", "content": f"Task: {task}\n\nExecute this task as an autonomous agent. Keep going until it's done."})

            max_loops = 8
            completed = False

            for loop in range(max_loops):
                st.markdown(f"**Loop {loop+1}/{max_loops}**")
                placeholder = st.empty()

                try:
                    response = client.chat.completions.create(
                        model="grok-4.3",
                        messages=messages,
                        temperature=0.6,
                        max_tokens=1200
                    )
                    
                    content = response.choices[0].message.content
                    messages.append({"role": "assistant", "content": content})

                    # Display the agent's output with nice formatting
                    placeholder.markdown(content)

                    # Check if task is complete
                    if "FINAL ANSWER" in content.upper() or "TASK COMPLETE" in content.upper():
                        completed = True
                        st.success("🎉 Agent completed the task!")
                        break

                    # Small pause so user can read each step
                    time.sleep(1.2)

                except Exception as e:
                    st.error(f"Error in loop {loop+1}: {str(e)}")
                    break

            if not completed:
                st.warning("Agent reached maximum loops. Here's the final output.")

            st.divider()
            st.subheader("📋 Final Result")
            st.info("The agent ran a full agentic loop: planning, acting, reflecting, and iterating until done.")

    st.divider()
    st.markdown("### 📚 What You Just Experienced")
    st.markdown("""
    - **Agentic AI** = AI that doesn't just answer once. It *plans, acts, reflects, and loops* until the goal is achieved.
    - This template teaches the fundamental pattern behind advanced agents.
    - Next templates will add memory, tools, and more complex behaviors.
    """)

    st.info("💡 Fork this repo and modify the system prompt or add new templates to create your own agents!") 

else:
    st.warning("Enter your Grok API key above to activate the agent.")

st.caption("Agent-in-a-Box by pileofflapjacks1 · Teaching the world agentic AI one fork at a time")