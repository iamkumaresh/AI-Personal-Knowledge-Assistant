import streamlit as st
from utils.helpers import get_greeting, clean_html

def render_header(title: str, subtitle: str):
    """
    Renders a unified premium glassmorphic header at the top of the page.
    """
    greeting = get_greeting()
    
    header_html = f"""
    <div class="glass-card" style="padding: 14px 20px; margin-bottom: 16px; border-left: 4px solid #6366F1;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
            <div>
                <h2 style="margin: 0; color: #f8fafc; font-size: 1.5rem; font-weight: 700; font-family: 'Manrope', sans-serif;">
                    {title}
                </h2>
                <p style="margin: 2px 0 0 0; color: #94a3b8; font-size: 0.85rem; font-family: 'Inter', sans-serif;">
                    {subtitle}
                </p>
            </div>
            <div style="text-align: right; background: rgba(99, 102, 241, 0.06); padding: 6px 12px; border-radius: 8px; border: 1px solid rgba(99, 102, 241, 0.12);">
                <span style="font-size: 0.7rem; color: #6366F1; font-weight: 600; text-transform: uppercase; font-family: 'Inter', sans-serif;">System Status</span>
                <div style="font-weight: 700; color: #f8fafc; font-size: 0.85rem; font-family: 'Inter', sans-serif;">{greeting}!</div>
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(header_html), unsafe_allow_html=True)
