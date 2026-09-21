import streamlit as st
import uuid
from backend.rag import ingest_pdf

def render_sidebar():
    st.sidebar.title("NexusRAG")
    
    # Session Control
    st.sidebar.header("Session Control")
    if st.sidebar.button("Create New Chat", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
        
    st.sidebar.markdown(f"**Current Thread:** `{st.session_state.get('thread_id', 'None')[:8]}...`")
    
    st.sidebar.divider()
    
    # Data Ingestion
    st.sidebar.header("External Data Ingestion")
    uploaded_file = st.sidebar.file_uploader("Upload a PDF for RAG", type=["pdf"])
    if uploaded_file is not None:
        if st.sidebar.button("Process PDF"):
            with st.spinner("Ingesting PDF..."):
                result = ingest_pdf(uploaded_file)
                st.sidebar.success(result)
                
    st.sidebar.divider()
    
    st.sidebar.markdown('### About Developer')
    
    # Check if user provided an image in the workspace
    import os
    if os.path.exists("developer.png"):
        st.sidebar.image("developer.png", width=150)
    elif os.path.exists("developer.jpg"):
        st.sidebar.image("developer.jpg", width=150)
    else:
        st.sidebar.image("https://via.placeholder.com/150", width=150)
        
    st.sidebar.markdown("""
        <div class="about-section">
            <p><strong>Project:</strong> NexusRAG</p>
            <p><strong>Built by:</strong> Deepak Mishra</p>
            <p><strong>Email:</strong> deep.mishra45321@gmail.com</p>
            <p><strong>Mobile:</strong> 7876776987</p>
        </div>
    """, unsafe_allow_html=True)
