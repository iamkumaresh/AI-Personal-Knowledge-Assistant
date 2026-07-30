import streamlit as st
from services.database import init_db

# 1. Set Page Configuration (Must be the very first Streamlit command)
try:
    st.set_page_config(
        page_title="Gyani Baba",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

# 2. Initialize Database on startup
try:
    init_db()
except Exception as e:
    st.error(f"Fatal error initializing SQLite database: {e}")

# 3. Initialize default session state values if not present
if "current_session_id" not in st.session_state:
    st.session_state["current_session_id"] = None
if "chat_placeholder_text" not in st.session_state:
    st.session_state["chat_placeholder_text"] = ""

# 4. Redirect immediately to the Dashboard page
st.switch_page("pages/Dashboard.py")
