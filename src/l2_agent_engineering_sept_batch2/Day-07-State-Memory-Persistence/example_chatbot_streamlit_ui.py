"""Day 7 (flavor 4 UI): Streamlit chat window for the SQLite-backed graph.

This file supports both of these launch commands::

    uv run example_chatbot_streamlit_ui.py
    uv run streamlit run example_chatbot_streamlit_ui.py
"""

import sys
import uuid
from pathlib import Path

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


def ensure_streamlit_runtime() -> None:
    """Relaunch this file with Streamlit when executed as a plain Python script."""
    if get_script_run_ctx(suppress_warning=True) is None:
        from streamlit.web import cli as stcli

        script_path = str(Path(__file__).resolve())
        sys.argv = ["streamlit", "run", script_path, *sys.argv[1:]]
        raise SystemExit(stcli.main())


ensure_streamlit_runtime()

from example_chatbot_streamlit import graph

USER_AVATAR = "🧑"
ASSISTANT_AVATAR = "🤖"

st.set_page_config(page_title="Day 7 Chatbot", page_icon="💬", layout="centered")

st.markdown(
    """
    <style>
    .block-container { max-width: 780px; padding-top: 2rem; }
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    [data-testid="stChatMessageContent"] p { margin-bottom: 0; }
    .chat-header {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 14px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 1.2rem;
        color: white;
    }
    .chat-header h1 { font-size: 1.3rem; margin: 0; }
    .chat-header p { margin: 0.2rem 0 0; opacity: 0.9; font-size: 0.85rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def start_new_chat() -> None:
    st.session_state.thread_id = uuid.uuid4().hex[:8]
    st.session_state.stopped = False


if "thread_id" not in st.session_state:
    st.session_state.thread_id = "student-1"
if "stopped" not in st.session_state:
    st.session_state.stopped = False

with st.sidebar:
    st.subheader("💬 Day 7 Chatbot")
    st.caption("SQLite-backed memory · gpt-oss:120b-cloud")
    st.text_input("Thread ID", key="thread_id")
    st.button("🆕 New chat", on_click=start_new_chat, use_container_width=True)
    st.divider()
    st.caption("Two different Thread IDs never share history.")

thread_id = st.session_state.thread_id
settings = {"configurable": {"thread_id": thread_id}}

st.markdown(
    f"""
    <div class="chat-header">
        <h1>Day 7 Chatbot</h1>
        <p>Thread: {thread_id} · type "bye" or "quit" to end the conversation</p>
    </div>
    """,
    unsafe_allow_html=True,
)

saved_state = graph.get_state(settings)
chat_history = saved_state.values.get("chat_history", [])

if not chat_history and not st.session_state.stopped:
    st.chat_message("assistant", avatar=ASSISTANT_AVATAR).write(
        "Hi! Send a message to start this thread's conversation."
    )

for message in chat_history:
    avatar = USER_AVATAR if message["role"] == "user" else ASSISTANT_AVATAR
    st.chat_message(message["role"], avatar=avatar).write(message["content"])

if st.session_state.stopped:
    st.chat_message("assistant", avatar=ASSISTANT_AVATAR).write("Goodbye!")
    st.button("Start a new chat", on_click=start_new_chat)
else:
    user_message = st.chat_input("Type a message ('bye' or 'quit' to stop)")
    if user_message:
        if user_message.strip().lower() in ("bye", "quit"):
            st.session_state.stopped = True
            st.rerun()
        else:
            st.chat_message("user", avatar=USER_AVATAR).write(user_message)
            with st.chat_message("assistant", avatar=ASSISTANT_AVATAR):
                with st.spinner("Thinking..."):
                    graph.invoke({"user_message": user_message}, config=settings)
            st.rerun()
