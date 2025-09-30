import streamlit as st

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None

def render_sidebar():
    st.sidebar.title("API Key Input")
    api_key = st.sidebar.text_input(
        "Enter your API key:", 
        key="api_key_input",
        type="password"
    )
    update_button = st.sidebar.button("Update API Key", key="update_button")
    return api_key, update_button