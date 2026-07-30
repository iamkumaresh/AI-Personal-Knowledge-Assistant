import streamlit as st
import uuid
import datetime
import sqlite3
import importlib

import utils.helpers
from utils.helpers import clean_html
import utils.styles
from utils.styles import apply_global_styles
import components.sidebar
from components.sidebar import render_sidebar
import components.header
from components.header import render_header
from components.chat_ui import render_message, render_typing_animation, get_chat_download_link
from services.database import (
    get_chat_sessions, create_chat_session, get_chat_history, 
    add_chat_message, clear_chat_history, delete_chat_session, get_stats
)
from services.retriever import ContextRetriever
from services.gemini_service import GeminiService
from utils.config import DATABASE_PATH

# Page Setup
try:
    st.set_page_config(
        page_title="Gyani Baba - Chat",
        layout="wide"
    )
except Exception:
    pass

# Apply global CSS
apply_global_styles()

# Render standard sidebar
importlib.reload(components.sidebar)
render_sidebar("Chat")

# Render Header
render_header(
    title="AI Chat Assistant",
    subtitle="Chat with Gyani Baba grounded in your uploaded documents"
)

# Check if we have documents uploaded
stats = get_stats()
has_docs = stats["total_documents"] > 0

# --- CHAT SESSION MANAGEMENT ---
sessions = get_chat_sessions()

# If no sessions exist, create a default one
if not sessions:
    default_id = str(uuid.uuid4())
    create_chat_session(default_id, "General Conversation")
    sessions = get_chat_sessions()
    st.session_state["current_session_id"] = default_id

# Set active session
if st.session_state.get("current_session_id") is None or st.session_state["current_session_id"] not in [s["id"] for s in sessions]:
    st.session_state["current_session_id"] = sessions[0]["id"]

active_session_id = st.session_state["current_session_id"]
active_session_title = next(s["title"] for s in sessions if s["id"] == active_session_id)

# --- SPLIT SCREEN LAYOUT ---
chat_sidebar_col, chat_main_col = st.columns([1, 3])

# Left column: Conversation Session List (ChatGPT style)
with chat_sidebar_col:
    st.markdown(
        clean_html(
            """
            <div class="glass-card" style="padding: 16px; margin-bottom: 12px; height: 100%;">
                <h4 style="margin-top:0; color:#f8fafc; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 8px; font-family:'Manrope',sans-serif;">
                    Conversations
                </h4>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
    
    # New Chat Button
    if st.button("New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        create_chat_session(new_id, f"Chat - {timestamp}")
        st.session_state["current_session_id"] = new_id
        st.rerun()
        
    st.write("")
    
    # Render scrollable list of conversations
    st.markdown('<div class="session-list-container">', unsafe_allow_html=True)
    for s in sessions:
        is_active = (s["id"] == active_session_id)
        title_label = s["title"]
        
        session_col, del_col = st.columns([4.2, 1])
        with session_col:
            if is_active:
                st.markdown('<div class="active-session-wrapper">', unsafe_allow_html=True)
                if st.button(title_label, key=f"sel_{s['id']}", use_container_width=True):
                    st.session_state["current_session_id"] = s["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if st.button(title_label, key=f"sel_{s['id']}", use_container_width=True):
                    st.session_state["current_session_id"] = s["id"]
                    st.rerun()
        with del_col:
            st.markdown('<span class="danger-btn-marker"></span>', unsafe_allow_html=True)
            if st.button("✕", key=f"del_session_{s['id']}", help="Delete session", use_container_width=True):
                delete_chat_session(s["id"])
                if st.session_state["current_session_id"] == s["id"]:
                    st.session_state["current_session_id"] = None
                st.rerun()
        st.markdown("<hr style='margin: 4px 0; border: none; border-bottom: 1px solid rgba(255,255,255,0.02);'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Right column: Active Chat Conversation
with chat_main_col:
    # Warning if no files exist
    if not has_docs:
        st.warning("No documents indexed yet. Head to the PDF Upload Center to add source files. Answers will not be grounded until you do.")
        
    st.markdown(
        clean_html(
            f"""
            <div style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 16px;">
                <span style="color:#8c909f; font-size:0.8rem; text-transform:uppercase; font-weight:600; letter-spacing:0.05em; font-family:'Inter',sans-serif;">Active Conversation Session</span>
                <h3 style="margin: 0; color:#f8fafc; font-size:1.4rem; font-family:'Manrope',sans-serif;">{active_session_title}</h3>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
    
    # Load history from SQLite
    history = get_chat_history(active_session_id)
    
    # Suggested Prompts (if chat is empty)
    if not history and has_docs:
        st.markdown("#### Suggested Questions:")
        sug_col1, sug_col2 = st.columns(2)
        with sug_col1:
            if st.button("Summarize the main topics of the documents", use_container_width=True):
                st.session_state["chat_placeholder_text"] = "Summarize the main topics of the documents"
        with sug_col2:
            if st.button("List the key findings or recommendations", use_container_width=True):
                st.session_state["chat_placeholder_text"] = "List the key findings or recommendations"
        st.markdown("<br>", unsafe_allow_html=True)
        
    # Render all past messages
    for msg in history:
        render_message(msg["sender"], msg["message"], msg.get("sources"))
        
    # User Input Field
    # If the user clicked a suggestion, pre-populate
    placeholder_val = st.session_state.get("chat_placeholder_text", "")
    st.session_state["chat_placeholder_text"] = "" # Clear placeholder for next rerun
    
    user_query = st.chat_input("Ask a question about your documents...", key="user_chat_input")
    
    # Handle user query submission
    query_to_process = user_query or placeholder_val
    
    if query_to_process:
        # 1. Display User Message & Save to SQLite
        render_message("user", query_to_process)
        add_chat_message(active_session_id, "user", query_to_process)
        
        # 2. Show AI Typing Animation
        with st.spinner(""):
            typing_placeholder = st.empty()
            with typing_placeholder.container():
                render_typing_animation()
                
            # 3. Retrieve Relevant Context
            retrieved = ContextRetriever.retrieve_context(query_to_process, k=5)
            context = retrieved["context"]
            sources = retrieved["sources"]
            
            # 4. Generate Gemini Answer
            if not has_docs:
                answer_res = GeminiService.generate_answer(
                    question=query_to_process, 
                    context="No document uploaded. Advise user to upload PDFs first."
                )
            else:
                answer_res = GeminiService.generate_answer(query_to_process, context)
                
            ai_answer = answer_res["answer"]
            
            # Clear typing animation
            typing_placeholder.empty()
            
            # 5. Display AI Message
            render_message("ai", ai_answer, sources)
            
            # 6. Save AI Response to SQLite
            add_chat_message(active_session_id, "ai", ai_answer, sources)
            
            # Update title of session if it was default name
            if active_session_title.startswith("Chat - ") or active_session_title == "General Conversation":
                short_title = query_to_process[:30] + "..." if len(query_to_process) > 30 else query_to_process
                try:
                    conn = sqlite3.connect(str(DATABASE_PATH))
                    cursor = conn.cursor()
                    cursor.execute("UPDATE chat_sessions SET title = ? WHERE id = ?", (short_title, active_session_id))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
            
            # Rerun to update sidebars and session state
            st.rerun()

    # --- FOOTER ACTIONS ---
    if history:
        st.markdown("<br><hr>", unsafe_allow_html=True)
        foot_col1, foot_col2, foot_col3 = st.columns([1, 1, 2])
        
        with foot_col1:
            st.markdown('<span class="danger-btn-marker"></span>', unsafe_allow_html=True)
            if st.button("Clear Chat History", use_container_width=True):
                clear_chat_history(active_session_id)
                st.success("Chat history cleared.")
                st.rerun()
            
        with foot_col2:
            download_link = get_chat_download_link(history)
            st.markdown(
                clean_html(
                    f"""
                    <div style="background:rgba(255,255,255,0.01); border:1px solid rgba(255,255,255,0.05); border-radius:8px; padding:9px; text-align:center;">
                        {download_link}
                    </div>
                    """
                ),
                unsafe_allow_html=True
            )
            
        with foot_col3:
            st.write("")
