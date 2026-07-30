import streamlit as st
from utils.helpers import clean_html

def apply_global_styles():
    """Injects custom CSS matching the Indigo-Slate high-contrast premium SaaS dark theme."""
    css = """
    <style>
    /* Google Font Imports */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@700;800&family=JetBrains+Mono&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* Global Typography & Font Overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0F172A !important;
        scroll-behavior: smooth;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    /* Adjust Streamlit page block containers padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    /* Core Page Styling for Dark Theme */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
    }

    /* Hide Default Streamlit Elements for cleaner UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
    [data-testid="stSidebarNav"] {display: none !important;}

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        border-right: 1px solid #334155;
        transition: all 0.3s ease;
    }

    /* Custom Sidebar Navigation Links */
    .sidemenu-link {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 8px;
        color: #94A3B8 !important;
        text-decoration: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 4px;
    }
    
    .sidemenu-link:hover {
        background: rgba(99, 102, 241, 0.08);
        color: #6366F1 !important;
        transform: translateX(4px);
    }
    
    .sidemenu-link .material-symbols-outlined {
        color: #94A3B8;
        transition: color 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .sidemenu-link:hover .material-symbols-outlined {
        color: #6366F1;
    }
    
    .active-sidemenu-link {
        background: rgba(99, 102, 241, 0.12) !important;
        color: #6366F1 !important;
        font-weight: 600 !important;
        border-left: 3px solid #6366F1;
        border-radius: 0 8px 8px 0 !important;
        padding-left: 13px !important;
    }
    
    .active-sidemenu-link .material-symbols-outlined {
        color: #6366F1 !important;
    }

    /* Custom Glassmorphic Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.02) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.02) !important;
        border-radius: 16px !important;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.02), 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .glass-card:hover {
        background: rgba(30, 41, 59, 0.5) !important;
        border-top-color: rgba(255, 255, 255, 0.1) !important;
        border-left-color: rgba(255, 255, 255, 0.07) !important;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.04), 0 16px 48px 0 rgba(99, 102, 241, 0.12) !important;
        transform: translateY(-4px) scale(1.002);
    }

    /* Interactive Stat Cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.01) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stat-card:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        box-shadow: 0 12px 36px rgba(99, 102, 241, 0.1) !important;
        transform: translateY(-4px);
    }

    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6366F1, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }

    /* Gradient Headers & Titles */
    .gradient-text {
        background: linear-gradient(90deg, #6366F1 0%, #a5b4fc 50%, #ffb786 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Modern Document Card Grid styling */
    .doc-card {
        background: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .doc-card:hover {
        border-color: rgba(99, 102, 241, 0.3) !important;
        background: rgba(99, 102, 241, 0.02) !important;
        transform: scale(1.015);
    }

    /* Premium Custom Navigation / Buttons */
    div.stButton > button {
        background: #6366F1 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        max-width: 100% !important;
    }

    div.stButton > button:hover {
        background: #818cf8 !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    div.stButton > button:active {
        transform: scale(0.96) !important;
    }

    /* Secondary buttons or danger buttons */
    .danger-btn button,
    div.element-container:has(> span.danger-btn-marker) + div.element-container div.stButton > button,
    div:has(> span.danger-btn-marker) div.stButton > button,
    [data-testid="column"]:has(span.danger-btn-marker) div.stButton > button,
    [data-testid="stVerticalBlock"]:has(span.danger-btn-marker) div.stButton > button {
        background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .danger-btn button:hover,
    div.element-container:has(> span.danger-btn-marker) + div.element-container div.stButton > button:hover,
    div:has(> span.danger-btn-marker) div.stButton > button:hover,
    [data-testid="column"]:has(span.danger-btn-marker) div.stButton > button:hover,
    [data-testid="stVerticalBlock"]:has(span.danger-btn-marker) div.stButton > button:hover {
        background: #f87171 !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* Native Chat Message Styling Overrides */
    [data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatMessage"]:hover {
        background-color: rgba(30, 41, 59, 0.4) !important;
        border-color: rgba(99, 102, 241, 0.15) !important;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.06) !important;
    }

    /* Style the avatar containers for a premium look */
    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {
        background-color: rgba(99, 102, 241, 0.08) !important;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        border-radius: 8px !important;
    }

    .source-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.08) !important;
        color: #a5b4fc !important;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        margin-right: 6px;
        margin-top: 6px;
        border: 1px solid rgba(99, 102, 241, 0.15) !important;
        transition: all 0.2s ease;
        cursor: default;
    }
    
    .source-tag:hover {
        background: rgba(99, 102, 241, 0.15) !important;
        border-color: rgba(99, 102, 241, 0.25) !important;
    }

    /* Custom Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.01);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 4px;
        transition: background 0.3s ease;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.3);
    }

    /* Styled input fields */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
    }

    /* Sidebar session list buttons overrides */
    .session-list-container div.stButton > button {
        background-color: rgba(255, 255, 255, 0.01) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
        color: #94A3B8 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        width: 100% !important;
        display: block !important;
    }

    .session-list-container div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.03) !important;
        color: #6366F1 !important;
        border-color: rgba(99, 102, 241, 0.15) !important;
        transform: none !important;
    }

    .session-list-container .active-session-wrapper div.stButton > button {
        background-color: rgba(99, 102, 241, 0.08) !important;
        color: #6366F1 !important;
        font-weight: 600 !important;
        border-left: 3px solid #6366F1 !important;
        border-radius: 0 6px 6px 0 !important;
        padding-left: 9px !important;
    }

    /* Danger delete session button in sidebar */
    .session-list-container .danger-btn div.stButton > button,
    .session-list-container div:has(> span.danger-btn-marker) div.stButton > button {
        background-color: rgba(239, 68, 68, 0.05) !important;
        border: 1px solid rgba(239, 68, 68, 0.1) !important;
        color: #ef4444 !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        aspect-ratio: 1 !important;
    }

    .session-list-container .danger-btn div.stButton > button:hover,
    .session-list-container div:has(> span.danger-btn-marker) div.stButton > button:hover {
        background-color: rgba(239, 68, 68, 0.15) !important;
        color: #ef4444 !important;
        border-color: rgba(239, 68, 68, 0.3) !important;
        transform: scale(1.05) !important;
    }

    /* Tab active highlight styling overrides */
    div[data-baseweb="tab-highlight"] {
        background-color: #6366F1 !important;
    }
    div[data-baseweb="tab"] {
        color: #94A3B8 !important;
        font-family: 'Inter', sans-serif !important;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        color: #F8FAFC !important;
        font-weight: 600 !important;
    }

    /* Style Chat Input Focus */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.15) !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
    }
    </style>
    """
    st.markdown(clean_html(css), unsafe_allow_html=True)
