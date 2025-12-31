import streamlit as st
import json
import time
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# ======================================================
# Page Configuration
# ======================================================
st.set_page_config(
    page_title="Assistant Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ======================================================
# Custom CSS (Chat UI Polish)
# ======================================================
st.markdown(
    """
    <style>
    .stChatMessage {
        padding: 14px;
        border-radius: 14px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="user"] {
        background-color: #e6f2ff;
    }
    .stChatMessage[data-testid="assistant"] {
        background-color: #f6f6f6;
    }
    code {
        background-color: #f0f0f0;
        padding: 4px 6px;
        border-radius: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# Sidebar Controls
# ======================================================
st.sidebar.title("⚙️ Controls")

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1
)

if st.sidebar.button("🧹 Reset Chat"):
    st.session_state.message_history = []
    st.experimental_rerun()

if st.sidebar.button("💾 Export Chat"):
    chat_json = json.dumps(st.session_state.get("message_history", []), indent=2)
    st.sidebar.download_button(
        label="Download Chat History",
        data=chat_json,
        file_name="chat_history.json",
        mime="application/json"
    )

st.sidebar.markdown("---")
st.sidebar.caption("LangGraph • LangChain • Streamlit")

# ======================================================
# Title
# ======================================================
st.title("Sunil's Chatbot")
# st.caption("LangGraph-powered conversational agent")

# ======================================================
# LangGraph Config
# ======================================================
CONFIG = {
    "configurable": {
        "thread_id": "thread-1",
        "temperature": temperature
    }
}

# ======================================================
# Session State Initialization
# ======================================================
if "message_history" not in st.session_state:
    st.session_state.message_history = []

# ======================================================
# Display Conversation History
# ======================================================
for msg in st.session_state.message_history:
    with st.chat_message(
        msg["role"],
        avatar="👤" if msg["role"] == "user" else "🤖"
    ):
        st.markdown(msg["content"])

# ======================================================
# Chat Input
# ======================================================
user_input = st.chat_input("Ask me anything...")

if user_input:
    # -------------------------
    # Store User Message
    # -------------------------
    st.session_state.message_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # -------------------------
    # Call LangGraph Agent
    # -------------------------
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()

        with st.spinner("🤖 Thinking..."):
            response = chatbot.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG
            )

        ai_message = response["messages"][-1].content

        # -------------------------
        # Simulated Streaming Effect
        # -------------------------
        streamed_text = ""
        for token in ai_message.split():
            streamed_text += token + " "
            placeholder.markdown(streamed_text)
            time.sleep(0.02)

    # -------------------------
    # Store Assistant Message
    # -------------------------
    st.session_state.message_history.append(
        {"role": "assistant", "content": ai_message}
    )
