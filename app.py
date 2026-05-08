import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="Agent-in-a-Box", page_icon="📦")
st.title("🚀 Agent-in-a-Box Marketplace")
st.subheader("Grok 4.3 Powered Templates")

st.markdown("### Life Admin Executor - First Template")

# API Key handling
if 'grok_key' not in st.session_state:
    api_key = st.text_input("Enter your xAI Grok API Key", type="password")
    if st.button("Save Key & Start"):
        st.session_state.grok_key = api_key
        st.success("Key saved! You can now use the agent.")
else:
    st.success("✅ Grok API Key is set")

if 'grok_key' in st.session_state:
    client = OpenAI(base_url="https://api.x.ai/v1", api_key=st.session_state.grok_key)
    
    task = st.text_area("Describe your life admin task or request:", height=120, placeholder="Cancel my old gym membership and find better alternatives...")
    
    if st.button("Run Agent", type="primary"):
        with st.spinner("Grok Agent is thinking and acting..."):
            try:
                response = client.chat.completions.create(
                    model="grok-4.3",
                    messages=[
                        {"role": "system", "content": "You are an autonomous Life Admin Executor Agent. You help users with bureaucratic and life admin tasks efficiently. Research when needed, give clear action steps, and be proactive."},
                        {"role": "user", "content": task}
                    ],
                    temperature=0.7,
                    reasoning_effort="medium"
                )
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.divider()
st.info("This is your first Agent-in-a-Box template. More templates coming soon!")