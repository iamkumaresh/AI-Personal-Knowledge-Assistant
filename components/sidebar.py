import streamlit as st
import os
from utils.helpers import clean_html

def render_sidebar(active_page: str = ""):
    """Renders a clean, compact glassmorphic sidebar with Logo and Navigation links."""
    with st.sidebar:
        # Title and Branding
        st.markdown(
            clean_html(
                """
                <div style="text-align: center; padding: 20px 0 10px 0;">
                    <h1 style="font-size: 2.2rem; font-weight: 800; margin: 0; background: linear-gradient(90deg, #6366F1, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family: 'Manrope', sans-serif;">
                        Gyani Baba
                    </h1>
                    <p style="font-size: 0.8rem; color: #94a3b8; margin: 5px 0 0 0; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; font-family: 'Inter', sans-serif;">
                        AI Knowledge Assistant
                    </p>
                </div>
                """
            ), 
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        # Check active link state classes
        dash_active = 'active-sidemenu-link' if active_page == 'Dashboard' else ''
        upload_active = 'active-sidemenu-link' if active_page == 'Upload' else ''
        chat_active = 'active-sidemenu-link' if active_page == 'Chat' else ''
        library_active = 'active-sidemenu-link' if active_page == 'Library' else ''
        settings_active = 'active-sidemenu-link' if active_page == 'Settings' else ''
        
        # Navigation Menu (Material Icons and clean Inter font navigation list)
        nav_html = f"""
        <div style="display: flex; flex-direction: column; gap: 4px; margin-top: 10px; font-family: 'Inter', sans-serif;">
            <div style="color: #64748b; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding-left: 16px; margin-bottom: 8px;">Navigation</div>
            
            <a href="/Dashboard" target="_self" class="sidemenu-link {dash_active}">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">dashboard</span>
                Dashboard
            </a>
            <a href="/Upload" target="_self" class="sidemenu-link {upload_active}">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">cloud_upload</span>
                Upload PDF
            </a>
            <a href="/Chat" target="_self" class="sidemenu-link {chat_active}">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">chat</span>
                AI Chat
            </a>
            <a href="/Documents" target="_self" class="sidemenu-link {library_active}">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">library_books</span>
                Document Library
            </a>
            <a href="/Settings" target="_self" class="sidemenu-link {settings_active}">
                <span class="material-symbols-outlined" style="font-size: 1.25rem;">settings</span>
                Settings
            </a>
        </div>
        """
        st.markdown(clean_html(nav_html), unsafe_allow_html=True)
