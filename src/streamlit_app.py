import streamlit as st
from agent import run_agent
from tools import load_tasks
import os

os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
st.set_page_config(page_title="🧠 Productivity Task Agent", layout="centered")

st.title("🧠 Productivity Task Agent")
st.markdown("Easily manage and track your tasks with AI assistance.")

# Initialize query history
if "user_queries" not in st.session_state:
    st.session_state.user_queries = []

# Input box for task commands
user_input = st.text_input("Enter your task command")

if st.button("Submit") and user_input.strip() != "":
    # Store the query
    st.session_state.user_queries.insert(0, user_input.strip())
    st.session_state.user_queries = st.session_state.user_queries[:5]  # Keep only last 5
    
    # Call the agent
    with st.spinner("Processing your request..."):
        response = run_agent(user_input.strip())
        st.success("Processed successfully!")

# Display last 5 queries
if st.session_state.user_queries:
    st.markdown("### 🕓 Last 5 Queries")
    for idx, q in enumerate(st.session_state.user_queries, start=1):
        st.markdown(f"**{idx}.** {q}")

# Divider and task table
st.markdown("---")
st.subheader("📋 Current Tasks")

try:
    df = load_tasks()
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load tasks: {e}")
