
import streamlit as st
from groq import Groq

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Groq AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Groq AI Chatbot")
st.caption("Chat with your AI assistant")

# -----------------------------
# API Configuration
# -----------------------------
MODEL = "llama-3.3-70b-versatile"

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error(
        "Groq API key not found. "
        "Please add GROQ_API_KEY in Streamlit Cloud Secrets."
    )
    st.stop()

# -----------------------------
# Initialize Groq Client
# -----------------------------
if "client" not in st.session_state:
    st.session_state.client = Groq(api_key=API_KEY)

# -----------------------------
# Initialize Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display Previous Messages
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.messages
                )

                reply = response.choices[0].message.content

                if not reply:
                    reply = "No response received from Groq."

                st.markdown(reply)

                st.session_state.messages.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                # Remove failed user message from history
                st.session_state.messages.pop()

                st.error(f"Groq API Error: {e}")

# -----------------------------
# Clear Chat
# -----------------------------
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()
