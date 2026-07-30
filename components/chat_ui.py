import streamlit as st
import base64
from typing import List, Dict, Any

def render_message(sender: str, message: str, sources: List[Dict[str, Any]] = None):
    """
    Renders a chat bubble for either user or AI, formatting markdown, 
    code segments, and listing sources using Streamlit's native chat layout.
    """
    avatar = "👤" if sender == "user" else "🤖"
    
    # Map 'ai' to 'assistant' for native streamlit chat message component support
    role = "user" if sender == "user" else "assistant"
    
    with st.chat_message(role, avatar=avatar):
        # Render markdown directly (handles code, tables, formatting natively)
        st.markdown(message)
        
        # Render cited sources if present
        if sources:
            with st.expander("📚 Sources & Citations", expanded=False):
                sources_html = '<div style="font-family:\'Inter\',sans-serif; padding-top: 4px;">'
                for idx, src in enumerate(sources):
                    filename = src.get("filename", "Doc")
                    page_num = src.get("page_num", "N/A")
                    score = src.get("score", 0.0)
                    sources_html += f'<span class="source-tag" title="Relevance: {score:.4f}">{filename} (pg. {page_num})</span>'
                sources_html += '</div>'
                st.markdown(sources_html, unsafe_allow_html=True)

def get_chat_download_link(history: List[Dict[str, Any]]) -> str:
    """Generates a base64 encoded link to download the chat log as a txt file."""
    chat_text = ""
    for msg in history:
        sender = "User" if msg["sender"] == "user" else "Gyani Baba"
        time_str = msg.get("timestamp", "")
        chat_text += f"[{time_str}] {sender}:\n{msg['message']}\n"
        if msg.get("sources"):
            chat_text += "Sources:\n"
            for src in msg["sources"]:
                chat_text += f"  - {src.get('filename')} (Page {src.get('page_num')})\n"
        chat_text += "\n" + "="*50 + "\n\n"
        
    b64 = base64.b64encode(chat_text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="chat_history.txt" style="text-decoration: none; color: #6366F1; font-weight: 600; font-family:\'Inter\',sans-serif;">Download History</a>'

def render_typing_animation():
    """Renders a typing indicator using a native chat message placeholder."""
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("🤖 *Gyani Baba is searching and thinking...*")
