import streamlit as st
from agent import run_agent
from tools import load_tasks

st.set_page_config(page_title="🧠 Productivity Task Agent", layout="centered")

st.title("🧠 Productivity Task Agent")

# Add a reset button
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
user_input = st.chat_input("Enter your task command")

if user_input:
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response
    with st.spinner("Thinking..."):
        try:
            response = run_agent(user_input)
            assistant_reply = response['output']
            
            # Display assistant response
            st.chat_message("assistant").markdown(assistant_reply)
            st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

# Divider
st.markdown("---")
st.subheader("📋 Current Tasks")

try:
    df = load_tasks()
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load tasks: {e}")
