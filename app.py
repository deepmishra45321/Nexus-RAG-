import streamlit as st
import uuid
from backend.memory import init_long_term_memory
from ui.styles import apply_custom_styles
from ui.sidebar import render_sidebar
from ui.chat import render_chat_interface

# Set page config
st.set_page_config(
    page_title="NexusRAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Long-Term Memory DB
init_long_term_memory()

# Apply custom styles
apply_custom_styles()

# Render UI components
render_sidebar()
render_chat_interface()
