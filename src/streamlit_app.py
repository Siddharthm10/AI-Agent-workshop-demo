import streamlit as st
from agent import run_agent
import pandas as pd
from tools import load_tasks

st.set_page_config(page_title="Productivity Agent", layout="centered")
st.title("🧠 Productivity Task Agent")

# Input
user_input = st.text_input("Enter your command", placeholder="e.g., Add task to submit report by Friday")

if st.button("Submit") and user_input.strip():
    with st.spinner("Thinking..."):
        response = run_agent(user_input)
        st.success(response['output'])

st.markdown("---")
st.subheader("📋 Current Tasks")

try:
    df = load_tasks()
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load tasks: {e}")
