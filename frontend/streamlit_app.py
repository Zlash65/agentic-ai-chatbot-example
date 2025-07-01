import streamlit as st
import requests

st.set_page_config(page_title="👽 AI Chatbot", layout="centered")

# Title
st.title("👽 AI Chatbot")
st.caption("Chat with different LLMs and optional web search support.")

# Supported models by provider
MODEL_OPTIONS = {
  "Groq": ["llama-3.1-8b-instant", "llama3-70b-8192"],
  "Gemini": ["gemini-2.0-flash", "gemini-2.5-flash"]
}

# Sidebar Configuration
with st.sidebar:
  st.header("⚙️ Agent Configuration")

  # Model provider
  model_provider = st.selectbox(
    "🔌 Model Provider",
    list(MODEL_OPTIONS.keys()),
    index=0,
    key="model_provider",
    help="Select which LLM provider to use"
  )

  # Update model list based on provider
  model_choices = MODEL_OPTIONS[model_provider]

  # Reset model if incompatible with selected provider
  if "model_name" in st.session_state and st.session_state.model_name not in model_choices:
    st.session_state.model_name = model_choices[0]

  # Model name (auto-updated)
  model_name = st.selectbox(
    "🧠 Model Name",
    model_choices,
    index=model_choices.index(st.session_state.get("model_name", model_choices[0])),
    key="model_name",
    help="Select the specific model you want to chat with"
  )

  # System prompt
  system_prompt = st.text_area(
    "📝 System Prompt",
    value="Act as a helpful, friendly, and humorous assistant.",
    height=120,
    help="This sets the behavior/personality of the assistant",
    placeholder="e.g., Act like a sarcastic movie critic or a coding mentor..."
  )

  allow_search = st.checkbox("🌐 Enable Web Search", value=False)

  st.markdown("---")

  if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

  st.markdown("---")
  st.markdown("Built with [Streamlit](https://streamlit.io/) and [FastAPI](https://fastapi.tiangolo.com/)")

# Model info badge
st.markdown(f"""
  <div style='
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    padding: 8px 16px;
    display: inline-block;
    margin-bottom: 1rem;
    font-weight: 500;
    font-size: 0.95rem;
  '>
    🧠 Using: <strong>{model_name}</strong> via <strong>{model_provider}</strong>
  </div>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
  st.session_state.chat_history = []

# Show chat history
for role, message in st.session_state.chat_history:
  with st.chat_message(role):
    st.markdown(message)

# Chat input box
user_input = st.chat_input("💬 Type your message...")

# Handle new message
if user_input:
  # Show user message
  with st.chat_message("user"):
    st.markdown(user_input)
  st.session_state.chat_history.append(("user", user_input))

  # Show AI thinking message
  with st.chat_message("ai"):
    with st.spinner("Thinking..."):
      try:
        # Payload for FastAPI
        payload = {
          "model_provider": model_provider.lower(),
          "model_name": model_name,
          "system_prompt": system_prompt,
          "messages": [user_input],
          "allow_search": allow_search
        }

        response = requests.post("http://localhost:3000/chat", json=payload)
        if response.status_code == 200:
          try:
            data = response.json()
            ai_response = data.get("response", "⚠️ No response from AI.")
          except Exception:
            ai_response = "⚠️ Could not parse server response."
        else:
          ai_response = f"❌ Server error: {response.status_code}"

        st.markdown(ai_response)
        st.session_state.chat_history.append(("ai", ai_response))

      except Exception as e:
        st.error(f"⚠️ Something went wrong: {str(e)}")
