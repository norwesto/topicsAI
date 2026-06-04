import streamlit as st
from agent import chat, SYSTEM_PROMPT
from tools import get_all_upcoming_assignments, add_study_session, get_events_for_week, clear_calendar, delete_event, save_calendar, load_calendar, get_assignments, get_courses

st.set_page_config(page_title = "Canvas Planning Assistant", page_icon = "📚")
st.title("Canvas Planning Assistant")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# display chat history
for msg in st.session_state.messages:
    if isinstance(msg, dict) and msg.get("role") == "user":
        st.chat_message("user").write(msg["content"])
    elif isinstance(msg, dict) and msg.get("role") == "assistant" and msg.get("content"):
        st.chat_message("assistant").write(msg["content"])

# chat input
if user_input := st.chat_input("Ask me about your assignments..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Thinking..."):
        reply = chat(st.session_state.messages)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)