import streamlit as st
import importlib
import textwrap

import utils.helpers
from utils.helpers import format_date, clean_html
import utils.styles
from utils.styles import apply_global_styles
import components.sidebar
from components.sidebar import render_sidebar

# Page configuration
try:
    st.set_page_config(
        page_title="Gyani Baba - Welcome",
        page_icon="🤖",
        layout="wide"
    )
except Exception:
    pass

# Apply global styling
apply_global_styles()

# Render Sidebar
importlib.reload(components.sidebar)
render_sidebar("Dashboard")

# Page-Specific Styling: Remove Streamlit padding for a true full-width web landing page
st.markdown(
    """
    <style>
    div.block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Entire landing page HTML matching the uploaded design mockup pixel-for-pixel using custom CSS layout rules
landing_html = """
<!DOCTYPE html>
<html class="dark" lang="en">
<head>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1.0" name="viewport">
    <title>Gyani Baba | Your AI-Powered Knowledge Assistant</title>
    <!-- Material Symbols -->
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Manrope:wght@700;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
    
    <style>
        /* Custom CSS Layout variables & styles matching mockup */
        body {
            background-color: #0F172A !important;
            font-family: 'Inter', sans-serif !important;
            color: #F8FAFC !important;
            margin: 0;
            padding: 0;
        }

        /* Glassmorphism Styles */
        .glass {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.02) !important;
            backdrop-filter: blur(24px) !important;
            -webkit-backdrop-filter: blur(24px) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-left: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05), 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        .glass-card:hover {
            border-top-color: rgba(255, 255, 255, 0.25) !important;
            border-left-color: rgba(255, 255, 255, 0.18) !important;
            box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.08), 0 12px 40px 0 rgba(173, 198, 255, 0.15) !important;
        }
        .neon-glow {
            box-shadow: 0 0 20px rgba(173, 198, 255, 0.2) !important;
        }

        /* Nav Bar Layout */
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 48px;
            height: 64px;
            background: #0F172A;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .nav-logo {
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 1.3rem;
            color: #6366F1;
            text-decoration: none;
            letter-spacing: -0.01em;
        }
        .nav-links {
            display: flex;
            gap: 32px;
            align-items: center;
        }
        .nav-links a {
            color: #94A3B8;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.2s;
        }
        .nav-links a:hover {
            color: #6366F1;
        }
        .nav-btn {
            background-color: #6366F1;
            color: #ffffff;
            padding: 8px 24px;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.8rem;
            text-decoration: none;
            box-shadow: 0 0 15px rgba(173, 198, 255, 0.15);
            transition: all 0.2s;
        }
        .nav-btn:hover {
            box-shadow: 0 0 25px rgba(173, 198, 255, 0.3);
            transform: translateY(-1px);
        }

        /* Hero Section Layout */
        .hero-section {
            padding: 80px 24px;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 24px;
        }
        .badge-container {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 6px 16px;
            border-radius: 9999px;
            color: #6366F1;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 8px;
            text-decoration: none;
        }
        .badge-dot {
            background-color: #6366F1;
            border-radius: 50%;
            height: 8px;
            width: 8px;
            box-shadow: 0 0 8px #6366F1;
        }
        .hero-title {
            font-family: 'Manrope', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            line-height: 1.15;
            color: #ffffff;
            margin: 0;
        }
        .hero-gradient {
            background: linear-gradient(90deg, #6366F1, #a5b4fc, #ffb786);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            color: #94A3B8;
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 640px;
            margin: 8px auto 0 auto;
        }
        .hero-actions {
            display: flex;
            gap: 16px;
            justify-content: center;
            margin-top: 16px;
        }
        .action-primary {
            background-color: #6366F1;
            color: #ffffff;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(173, 198, 255, 0.2);
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .action-primary:hover {
            box-shadow: 0 6px 20px rgba(173, 198, 255, 0.4);
            transform: translateY(-1px);
        }
        .action-secondary {
            background-color: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
        }
        .action-secondary:hover {
            background-color: rgba(255, 255, 255, 0.08);
        }

        /* Hero Floating Animation Canvas */
        .hero-visual {
            position: relative;
            width: 100%;
            max-width: 800px;
            height: 320px;
            margin: 48px auto 0 auto;
        }
        .visual-blur {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            width: 240px;
            height: 240px;
            background: rgba(208, 188, 255, 0.05);
            filter: blur(100px);
            border-radius: 50%;
            z-index: 1;
        }
        .visual-core {
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            z-index: 10;
        }
        .core-box {
            width: 140px;
            height: 140px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(24px);
            border: 1px solid rgba(173, 198, 255, 0.25);
            border-radius: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 25px rgba(173, 198, 255, 0.15);
        }
        .visual-doc-1 {
            position: absolute;
            left: 10%;
            top: 10%;
            z-index: 20;
        }
        .visual-doc-2 {
            position: absolute;
            right: 10%;
            top: 35%;
            z-index: 20;
        }
        .visual-doc-3 {
            position: absolute;
            left: 20%;
            bottom: 8%;
            z-index: 20;
        }
        .floating-card-body {
            display: flex;
            align-items: center;
            gap: 12px;
            width: 220px;
            border-radius: 12px;
            padding: 12px 16px;
            text-align: left;
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-16px); }
            100% { transform: translateY(0px); }
        }
        .animate-float {
            animation: float 6s ease-in-out infinite;
        }

        /* Features Section */
        .features-section {
            max-width: 1100px;
            margin: 100px auto 0 auto;
            padding: 0 24px 80px 24px;
        }
        .section-header {
            text-align: center;
            margin-bottom: 64px;
        }
        .section-title {
            font-family: 'Manrope', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
        }
        .section-subtitle {
            color: #94A3B8;
            font-size: 1rem;
            max-width: 580px;
            margin: 16px auto 0 auto;
            line-height: 1.5;
        }

        /* Bento Grid */
        .features-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 24px;
        }
        .grid-8 {
            grid-column: span 8;
        }
        .grid-4 {
            grid-column: span 4;
        }
        .bento-card {
            border-radius: 24px;
            padding: 32px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            text-decoration: none;
            min-height: 280px;
            position: relative;
            overflow: hidden;
        }
        .icon-box {
            width: 56px;
            height: 56px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 16px;
            margin-bottom: 24px;
        }
        .bento-title {
            font-family: 'Manrope', sans-serif;
            font-size: 1.3rem;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
        }
        .bento-desc {
            color: #94A3B8;
            font-size: 0.9rem;
            line-height: 1.5;
            margin: 8px 0 0 0;
        }

        /* Prompts inside chat bento */
        .prompt-pills {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 24px;
        }
        .prompt-pill {
            padding: 12px;
            border-radius: 12px;
            width: fit-content;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.75rem;
        }

        /* Terminal Emulator Box */
        .terminal-box {
            font-family: 'JetBrains Mono', monospace;
            color: #a5b4fc;
            background-color: rgba(0,0,0,0.3);
            border-radius: 16px;
            padding: 24px;
            flex: 1;
            min-width: 240px;
            text-align: left;
            font-size: 0.75rem;
            line-height: 1.5;
        }
        .terminal-dots {
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
        }
        .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }

        /* CTA Section */
        .cta-section {
            padding: 80px 24px;
        }
        .cta-card {
            max-width: 900px;
            margin: 0 auto;
            border-radius: 32px;
            padding: 64px 32px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .cta-title {
            font-family: 'Manrope', sans-serif;
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0 0 16px 0;
        }
        .cta-desc {
            color: #94A3B8;
            font-size: 1.1rem;
            max-width: 580px;
            margin: 0 auto 32px auto;
            line-height: 1.6;
        }
        .cta-actions {
            display: flex;
            justify-content: center;
            gap: 16px;
        }

        /* Footer */
        .footer-container {
            background-color: #0F172A;
            border-top: 1px solid rgba(255,255,255,0.05);
            padding: 48px 48px;
        }
        .footer-main {
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 32px;
        }
        .footer-logo {
            font-family: 'Manrope', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
            color: #6366F1;
            margin-bottom: 8px;
            display: block;
        }
        .footer-desc {
            color: #94A3B8;
            font-size: 0.8rem;
            margin: 0;
        }
        .footer-cols {
            display: flex;
            gap: 48px;
        }
        .footer-col {
            display: flex;
            flex-direction: column;
            gap: 8px;
            text-align: left;
            font-size: 0.8rem;
        }
        .footer-col-title {
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .footer-col a {
            color: #94A3B8;
            text-decoration: none;
        }
        .footer-col a:hover {
            color: #6366F1;
        }
        .footer-bottom {
            max-width: 1100px;
            margin: 48px auto 0 auto;
            padding-top: 32px;
            border-top: 1px solid rgba(255,255,255,0.05);
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: #94A3B8;
        }

        /* Media Queries for responsive collapsing */
        @media (max-width: 768px) {
            .nav-container {
                flex-direction: column;
                height: auto;
                padding: 16px;
                gap: 16px;
            }
            .hero-title {
                font-size: 2.2rem;
            }
            .hero-actions {
                flex-direction: column;
                width: 100%;
                gap: 12px;
            }
            .action-primary, .action-secondary {
                width: 100%;
                justify-content: center;
            }
            .hero-visual {
                height: 400px;
            }
            .visual-doc-1 {
                left: 5%;
                top: 5%;
            }
            .visual-doc-2 {
                right: 5%;
                top: 75%;
            }
            .visual-doc-3 {
                left: 5%;
                bottom: 35%;
            }
            .features-grid {
                display: flex;
                flex-direction: column;
                gap: 24px;
            }
            .footer-main {
                flex-direction: column;
                align-items: flex-start;
            }
            .footer-bottom {
                flex-direction: column;
                gap: 12px;
            }
        }
    </style>
</head>
<body class="bg-surface text-on-surface">
    
    <!-- Navigation Shell -->
    <nav class="nav-container">
        <div style="display:flex; align-items:center; gap:32px;">
            <a class="nav-logo" href="/Dashboard" target="_self">Gyani Baba</a>
            <div class="nav-links" style="display:flex; align-items:center; gap:24px;">
                <a href="/Upload" target="_self">Upload PDF</a>
                <a href="/Chat" target="_self">AI Chat</a>
                <a href="/Documents" target="_self">Library</a>
            </div>
        </div>
        <div>
            <a class="nav-btn" href="/Upload" target="_self">Get Started</a>
        </div>
    </nav>

    <!-- Main Content Canvas -->
    <main>
        <!-- Hero Section -->
        <section class="hero-section">

            
            <!-- Main Heading -->
            <h1 class="hero-title">
                Your AI-Powered <br>
                <span class="hero-gradient">Personal Knowledge</span> <br>
                Assistant
            </h1>
            
            <!-- Subtitle -->
            <p class="hero-subtitle">
                Centralize your documents, research, and ideas in a single ethereal space. Let Gyani Baba connect the dots and provide instant, accurate insights.
            </p>
            
            <!-- Actions -->
            <div class="hero-actions">
                <a class="action-primary" href="/Upload" target="_self">
                    Start Building Your Mind <span class="material-symbols-outlined text-sm" style="font-size: 1rem;">arrow_forward</span>
                </a>
                <a class="action-secondary" href="/Chat" target="_self">
                    Open Chat
                </a>
            </div>

            <!-- Hero Visual: Floating Documents & AI Core -->
            <div class="hero-visual">
                <div class="visual-blur"></div>
                
                <!-- Centered AI Core -->
                <div class="visual-core">
                    <div class="core-box">
                        <span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1; font-size: 4.5rem;">smart_toy</span>
                    </div>
                </div>
                
                <!-- Floating Documents -->
                <!-- Left Top: Q3 Report PDF -->
                <div class="visual-doc-1 animate-float" style="animation-delay: 0.5s;">
                    <div class="glass-card floating-card-body">
                        <div style="width: 40px; height: 40px; border-radius: 8px; background-color: rgba(255, 180, 171, 0.15); display: flex; align-items: center; justify-content: center; color: #ffb4ab;">
                            <span class="material-symbols-outlined">picture_as_pdf</span>
                        </div>
                        <div>
                            <p style="font-size: 0.8rem; font-weight: 700; color: #ffffff; margin: 0;">Q3 Report.pdf</p>
                            <p style="color: #94A3B8; font-size: 0.7rem; margin: 2px 0 0 0;">Processed by AI</p>
                        </div>
                    </div>
                </div>
                
                <!-- Right Middle: Project Analysis Excel -->
                <div class="visual-doc-2 animate-float" style="animation-delay: 1.2s;">
                    <div class="glass-card floating-card-body" style="width: 230px;">
                        <div style="width: 40px; height: 40px; border-radius: 8px; background-color: rgba(255, 183, 134, 0.15); display: flex; align-items: center; justify-content: center; color: #ffb786;">
                            <span class="material-symbols-outlined">table_chart</span>
                        </div>
                        <div>
                            <p style="font-size: 0.8rem; font-weight: 700; color: #ffffff; margin: 0;">Project_Analysis.xlsx</p>
                            <p style="color: #94A3B8; font-size: 0.7rem; margin: 2px 0 0 0;">Data extracted</p>
                        </div>
                    </div>
                </div>
                
                <!-- Left Bottom: Research Notes Text -->
                <div class="visual-doc-3 animate-float" style="animation-delay: 0.8s;">
                    <div class="glass-card floating-card-body" style="width: 210px;">
                        <div style="width: 40px; height: 40px; border-radius: 8px; background-color: rgba(173, 198, 255, 0.15); display: flex; align-items: center; justify-content: center; color: #6366F1;">
                            <span class="material-symbols-outlined">description</span>
                        </div>
                        <div>
                            <p style="font-size: 0.8rem; font-weight: 700; color: #ffffff; margin: 0;">Research_Notes.txt</p>
                            <p style="color: #94A3B8; font-size: 0.7rem; margin: 2px 0 0 0;">Summarized</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>


        <!-- CTA Section -->
        <section class="cta-section">
            <div class="glass-card cta-card">
                <h2 class="cta-title">Ready to augment your mind?</h2>
                <p class="cta-desc">
                    Join capstone researchers, developers, and B.Tech students who are using Gyani Baba to master their document corpora.
                </p>
                <div class="cta-actions">
                    <a class="action-primary" href="/Upload" target="_self">
                        Get Started Free
                    </a>
                    <a class="action-secondary" href="/Chat" target="_self">
                        Talk to Gyani
                    </a>
                </div>
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 24px 0 0 0;">Completely local vector index. No credit card required.</p>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer-container">
            <div class="footer-main">
                <div>
                    <span class="footer-logo">Gyani Baba</span>
                    <p class="footer-desc">The future of personal knowledge management.</p>
                </div>
                <div class="footer-cols">
                    <div class="footer-col">
                        <span class="footer-col-title">Product</span>
                        <a href="/Upload" target="_self">Upload</a>
                        <a href="/Chat" target="_self">Chat</a>
                    </div>
                    <div class="footer-col">
                        <span class="footer-col-title">Config</span>
                        <a href="/Documents" target="_self">Library</a>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 Gyani Baba AI. All rights reserved.</p>
                <div style="display: flex; gap: 24px;">
                    <a href="#" style="color: #94A3B8; text-decoration: none;">Privacy Policy</a>
                    <a href="#" style="color: #94A3B8; text-decoration: none;">Terms of Service</a>
                </div>
            </div>
        </footer>
    </main>
</body>
</html>
"""

st.markdown(clean_html(landing_html), unsafe_allow_html=True)
