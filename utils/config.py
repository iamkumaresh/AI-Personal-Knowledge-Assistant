import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
DATABASE_DIR = BASE_DIR / "database"
FAISS_DIR = BASE_DIR / "faiss_index"

# Database Configuration
DATABASE_PATH = DATABASE_DIR / "app.db"

# Model Configurations
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL_NAME = "gemini-2.0-flash"

# Create directories if they don't exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
FAISS_DIR.mkdir(parents=True, exist_ok=True)

# Create gitkeep files to maintain directory structures
for directory in [UPLOADS_DIR, FAISS_DIR]:
    gitkeep_file = directory / ".gitkeep"
    if not gitkeep_file.exists():
        gitkeep_file.touch()

def get_gemini_api_key() -> str:
    """Retrieve Gemini API key from session state, environment, or default fallback."""
    try:
        import streamlit as st
        if "user_api_key" in st.session_state and st.session_state["user_api_key"].strip():
            return st.session_state["user_api_key"].strip()
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")
    
def is_gemini_api_key_valid() -> bool:
    """Check if Gemini API key is present and valid."""
    api_key = get_gemini_api_key()
    return bool(api_key and api_key.strip() and api_key != "your_gemini_api_key_here")
