import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Clean and simple modern UI styles */
        .stChatInputContainer {
            padding-bottom: 20px;
        }
        .about-section {
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(128,128,128,0.2);
            margin-top: 20px;
        }
        .about-section img {
            border-radius: 50%;
            width: 100px;
            height: 100px;
            object-fit: cover;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
