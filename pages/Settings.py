import streamlit as st
import os
import sqlite3
import shutil
import textwrap
import importlib

import utils.helpers
from utils.helpers import clean_html
import utils.styles
from utils.styles import apply_global_styles
import components.sidebar
from components.sidebar import render_sidebar
import components.header
from components.header import render_header

from utils.config import (
    DATABASE_PATH, UPLOADS_DIR, FAISS_DIR, 
    is_gemini_api_key_valid, get_gemini_api_key, GEMINI_MODEL_NAME,
    BASE_DIR
)
from services.database import get_stats, get_connection
from services.vector_store import VectorStoreManager
from services.embedding_service import EmbeddingService

# Page Config
try:
    st.set_page_config(
        page_title="Gyani Baba - Settings",
        layout="wide"
    )
except Exception:
    pass

# Apply global styles
apply_global_styles()

# Render sidebar
importlib.reload(components.sidebar)
render_sidebar("Settings")

# Render Header
render_header(
    title="System Settings & Diagnostics",
    subtitle="Monitor system health, check APIs, and perform database maintenance"
)

# Diagnostic Stats
stats = get_stats()
db_size = os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0
db_size_kb = db_size / 1024

# Let's count messages and sessions
total_messages = 0
total_sessions = 0
try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chat_sessions")
    total_sessions = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM chat_messages")
    total_messages = cursor.fetchone()[0]
    conn.close()
except Exception:
    pass

# FAISS Files count
faiss_size_kb = 0
if os.path.exists(FAISS_DIR):
    for f in os.listdir(FAISS_DIR):
        fp = os.path.join(FAISS_DIR, f)
        if os.path.isfile(fp):
            faiss_size_kb += os.path.getsize(fp) / 1024

st.markdown(
    clean_html(
        """
        <div class="glass-card">
            <h3 style="margin-top:0; color:#f8fafc; font-family:'Manrope',sans-serif;">System Status & Metrics</h3>
            <p style="color:#8c909f; font-size:0.9rem; font-family:'Inter',sans-serif;">
                Diagnostics for evaluating system components, local directories, and API connectivity.
            </p>
        </div>
        """
    ),
    unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs(["Connections", "Storage & DB", "Maintenance"])

with tab1:
    st.markdown("#### Google Gemini Integration")
    api_valid = is_gemini_api_key_valid()
    
    if api_valid:
        status_html = f"""
        <div style="background-color: #064E3B; border: 1px solid #059669; padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; font-family: 'Inter', sans-serif; display: flex; align-items: center; gap: 8px; color: #F8FAFC; font-size: 0.9rem;">
            <span class="material-symbols-outlined" style="color: #34D399; font-size: 1.2rem;">check_circle</span>
            <span><strong>Gemini API Status:</strong> Connected (Model: <code>{GEMINI_MODEL_NAME}</code>)</span>
        </div>
        """
        st.markdown(clean_html(status_html), unsafe_allow_html=True)
    else:
        status_html = """
        <div style="background-color: #7F1D1D; border: 1px solid #EF4444; padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; font-family: 'Inter', sans-serif; display: flex; align-items: center; gap: 8px; color: #F8FAFC; font-size: 0.9rem;">
            <span class="material-symbols-outlined" style="color: #FCA5A5; font-size: 1.2rem;">cancel</span>
            <span><strong>Gemini API Status:</strong> Disconnected / Quota Exceeded</span>
        </div>
        """
        st.markdown(clean_html(status_html), unsafe_allow_html=True)
        st.warning("To enable conversational answers, please enter a valid Gemini API Key from Google AI Studio below.")
        
    # User API Key input field
    user_key = st.text_input(
        "Gemini API Key (stored in session)",
        value=st.session_state.get("user_api_key", ""),
        type="password",
        help="Paste your custom Gemini API key here. It overrides the default key for the current session.",
        placeholder="AIzaSy..."
    )
    if user_key != st.session_state.get("user_api_key", ""):
        st.session_state["user_api_key"] = user_key
        st.rerun()
        
    st.markdown("---")
    st.markdown("#### Embedding Pipeline")
    embeddings_status_html = """
    <div style="background-color: #064E3B; border: 1px solid #059669; padding: 12px 16px; border-radius: 8px; margin-bottom: 12px; font-family: 'Inter', sans-serif; display: flex; align-items: center; gap: 8px; color: #F8FAFC; font-size: 0.9rem;">
        <span class="material-symbols-outlined" style="color: #34D399; font-size: 1.2rem;">check_circle</span>
        <span><strong>Embeddings Engine:</strong> Active</span>
    </div>
    """
    st.markdown(clean_html(embeddings_status_html), unsafe_allow_html=True)
    st.info("Utilizing local SentenceTransformers model: `all-MiniLM-L6-v2`. Embeddings are computed locally and are completely free and private.")

with tab2:
    st.markdown("#### Database Details")
    st.markdown(
        f"""
        - **Database Type:** SQLite
        - **Database Location:** `{DATABASE_PATH}`
        - **Database File Size:** `{db_size_kb:.2f} KB`
        - **Uploaded Documents in SQL:** `{stats['total_documents']}`
        - **Total Pages Logged:** `{stats['total_pages']}`
        - **Total Sessions:** `{total_sessions}`
        - **Total Messages Logged:** `{total_messages}`
        """
    )
    
    st.markdown("---")
    st.markdown("#### FAISS Index Details")
    st.markdown(
        f"""
        - **Vector Database Type:** FAISS (Facebook AI Similarity Search)
        - **Index Location:** `{FAISS_DIR}`
        - **Local Index File Size:** `{faiss_size_kb:.2f} KB`
        - **Indexed State:** `{'Active Index' if VectorStoreManager.has_index() else 'Empty (No Index File)'}`
        """
    )

with tab3:
    st.markdown("#### Maintenance Actions")
    st.warning("**Caution:** The actions below modify databases and system configurations. Use with care.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Reset Buttons
    reset_col1, reset_col2 = st.columns(2)
    
    with reset_col1:
        st.markdown(
            clean_html(
                """
                <div style="background: rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:16px; border-radius:10px;">
                    <h5 style="margin-top:0; color:#f8fafc; font-family:'Manrope',sans-serif;">Clear Chat Conversations</h5>
                    <p style="color:#8c909f; font-size:0.8rem; height:45px; font-family:'Inter',sans-serif;">
                        Deletes all conversational records, past messages, and session IDs from the SQLite database.
                    </p>
                </div>
                """
            ),
            unsafe_allow_html=True
        )
        st.markdown('<span class="danger-btn-marker"></span>', unsafe_allow_html=True)
        if st.button("Delete All Chat Sessions", key="btn_clear_chats", use_container_width=True):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM chat_messages")
                cursor.execute("DELETE FROM chat_sessions")
                conn.commit()
                conn.close()
                st.success("All conversation sessions and messages deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error resetting chat history: {e}")
        
    with reset_col2:
        st.markdown(
            clean_html(
                """
                <div style="background: rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:16px; border-radius:10px;">
                    <h5 style="margin-top:0; color:#f8fafc; font-family:'Manrope',sans-serif;">Full System Reset</h5>
                    <p style="color:#8c909f; font-size:0.8rem; height:45px; font-family:'Inter',sans-serif;">
                        Purges all uploads, clears SQLite documents, clears all chat logs, and deletes the FAISS vector index.
                    </p>
                </div>
                """
            ),
            unsafe_allow_html=True
        )
        st.markdown('<span class="danger-btn-marker"></span>', unsafe_allow_html=True)
        if st.button("Reset Entire Application", key="btn_reset_all", use_container_width=True):
            try:
                # 1. Clear database tables
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM chat_messages")
                cursor.execute("DELETE FROM chat_sessions")
                cursor.execute("DELETE FROM documents")
                conn.commit()
                conn.close()
                
                # 2. Clear FAISS index
                VectorStoreManager.clear_vector_store()
                
                # 3. Clear physical PDFs in uploads
                if os.path.exists(UPLOADS_DIR):
                    for file_name in os.listdir(UPLOADS_DIR):
                        file_p = os.path.join(UPLOADS_DIR, file_name)
                        if file_name != ".gitkeep" and os.path.isfile(file_p):
                            os.remove(file_p)
                            
                st.success("Application has been completely reset. Ready for fresh uploads!")
                st.rerun()
            except Exception as e:
                st.error(f"Error executing complete reset: {e}")

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# About developer / B.Tech Capstone project footer
st.markdown(
    clean_html(
        """
        <div class="glass-card" style="text-align: center; border: 1px solid rgba(99, 102, 241, 0.2);">
            <h4 style="margin-top:0; color: #6366F1; font-family:'Manrope',sans-serif;">About Gyani Baba</h4>
            <p style="color: #F8FAFC; font-size: 0.9rem; line-height: 1.6; max-width: 800px; margin: 0 auto 16px auto; font-family:'Inter',sans-serif;">
                Gyani Baba is developed as a production-quality B.Tech Generative AI Capstone project. It exhibits semantic text chunking, local vector mapping, and contextual large language model synthesis.
            </p>
            <div style="font-size: 0.8rem; color:#94A3B8; font-family:'Inter',sans-serif; margin-bottom: 8px;">
                Built with Streamlit • SQLite • FAISS • SentenceTransformers • LangChain • Google Gemini API
            </div>
            <div style="font-size: 0.8rem; color:#6366F1; font-weight:600; font-family:'Inter',sans-serif; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 12px; margin-top: 12px;">
                Gyani Baba © 2026 · Made for B.Tech Capstone Project
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True
)
