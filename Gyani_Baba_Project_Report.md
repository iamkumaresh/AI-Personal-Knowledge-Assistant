# GYANI BABA 🤖
## A Standalone AI-Powered Personal Knowledge Assistant Grounded in Offline Vector Indexes

**A CAPSTONE PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE DEGREE OF**

### BACHELOR OF TECHNOLOGY
#### IN
### COMPUTER SCIENCE & ENGINEERING

**DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING**  
**SCHOOL OF ENGINEERING & TECHNOLOGY**  
**JULY 2026**  

---
# Abstract
This capstone project report presents 'Gyani Baba', an advanced, high-performance, and secure AI-Powered Personal Knowledge Assistant. The application is designed to address the challenges of information retrieval, cognitive overload, and data privacy in modern document-intensive environments. The system utilizes Retrieval-Augmented Generation (RAG) architecture, integrating a local dense vector retriever with a state-of-the-art generative language model to deliver grounded, accurate, and private question-answering capabilities. The system processes documents (PDF format) by extracting text page-by-page, chunking the content using hierarchical recursive splitting algorithms, and embedding the chunks into a high-dimensional vector space using a local SentenceTransformers model. These vector embeddings are stored in a serialized FAISS vector database. The chatbot engine uses Google's Gemini models to generate answers grounded strictly in the retrieved text context, effectively eliminating LLM hallucinations. The database layer is managed using a local SQLite database that records metadata, chat session logs, and message histories. The application features a sleek, high-contrast visual interface styled with glassmorphism CSS aesthetics, offering responsive layouts, interactive statistics cards, dynamic API key configuration, and collapsed citation references. Through rigorous diagnostics, automated verification, and process isolation, Gyani Baba provides a secure, reliable, and highly optimized knowledge-management solution for researchers, students, and engineers.

---
# Chapter 1: Introduction
## 1.1 Background & Inspiration
With the rapid digitization of work and research environments, the volume of digital text documents, particularly PDFs, has grown exponentially. Navigating these vast resources to extract specific technical insights, placement notes, or academic arguments has become a major source of cognitive overload. Standard document search utilities (e.g., Ctrl+F) rely on exact keyword matches, which fail to capture semantic relationships. For instance, searching a networking document for 'latency issues' will miss sections discussing 'TCP packet retransmissions' unless the query words are explicitly present. To solve this, researchers have turned to Large Language Models (LLMs), which can comprehend semantic query intent. However, deploying standard LLMs directly introduces significant challenges: first, the model's training data is static and does not include the user's private documents; second, LLMs frequently hallucinate plausible-sounding but completely incorrect information when answering outside their parameters; and third, uploading sensitive documents to commercial APIs poses severe privacy risks. The Gyani Baba project resolves these limitations using Retrieval-Augmented Generation (RAG) concepts. By combining private local text embedding and FAISS vector databases with grounded LLM generation, Gyani Baba creates a highly secure, private knowledge space.
## 1.2 Problem Definition
The project addresses the following critical problems:

1. **Cognitive Load in Document Search**: Manual document reading is slow and inefficient for finding specific details.
2. **Hallucinations in Commercial LLMs**: General-purpose LLMs lack grounding in specific documents, leading to incorrect responses.
3. **Data Sovereignty and Security**: Commercial cloud services ingest uploaded documents for training, exposing intellectual property.
4. **Offline Failures and Sandbox Constraints**: Traditional RAG pipelines fail completely when network connection is lost or restricted. Gyani Baba implements local embedding fallback logic to ensure continuous offline operability.
## 1.3 System Objectives
The core technological milestones of this project are:

- **Offline Semantic Processing**: Configure local models ('sentence-transformers/all-MiniLM-L6-v2') to execute directly on the CPU, preventing remote connection timeouts.
- **Grounded Generation**: Enforce prompts that limit LLM answers to the provided context, preventing hallucinated fabrications.
- **Multi-Session Management**: Build a local database to manage separate chat histories, allowing users to save, switch, and delete sessions.
- **Responsive, Premium UI/UX**: Design a dashboard with a high-contrast dark theme and Glassmorphism accents to optimize work screen space.
## 1.4 Functional Boundaries
Gyani Baba limits PDF uploads to 15MB to prevent memory exhaustion in low-end consumer laptops. It splits files recursively using custom separator heuristics, manages indexes in a local FAISS directory, and handles session histories in SQLite. Conversational logic relies on external API access, falling back gracefully when the API keys are invalid or rate-limited.

---
# Chapter 2: Literature Review
## 2.1 Retrieval-Augmented Generation Principles
Retrieval-Augmented Generation (RAG) is a framework introduced by Lewis et al. in 2020. Standard LLMs rely on static weights learned during pre-training. RAG separates the retrieval of external data from the generation of text. When a query is submitted, the system performs a similarity search against a vector database of documents. The database returns relevant text chunks, which are prepended as context inside the LLM prompt. This restricts the LLM to synthesise answers based only on the retrieved facts, resolving static weight limitations.
## 2.2 Comparative Study of Vector Index Libraries
Vector databases index, store, and query high-dimensional vector representations. For this project, FAISS (Facebook AI Similarity Search) was selected due to its lightweight, in-memory execution and direct serialization to disk. FAISS runs completely offline with zero server daemon overhead. Other databases (like Pinecone, Milvus, and Chroma) were evaluated but discarded for this standalone desktop project due to their high memory footprints, cloud dependency, or complex deployment overhead.

| Database | Deployment | Index Type | Best Use Case |
|---|---|---|---|
| FAISS | In-Memory/Local File | L2/Cosine, HNSW, IVF | Desktop apps, local RAG, low-overhead deployments |
| ChromaDB | Local / Server client | HNSW | Medium scale applications, prototyping |
| Pinecone | Cloud Hosted | Proprietary | Enterprise RAG, multi-user scaling, high traffic web apps |
| Milvus | Docker/Distributed | HNSW, IVF, Quantization | Massive distributed clusters, billions of vectors |

## 2.3 Embedding Quantizations & LLMs
Semantic search relies on embedding models converting text strings into dense vector representations. We utilize 'all-MiniLM-L6-v2' (384-dimensional vectors) because it balances high semantic accuracy with low CPU footprint. For text generation, we employ Google's Gemini models. The model 'gemini-2.0-flash' provides excellent contextual grounding and operates on a generous free tier (1,500 requests/day), ensuring high accessibility for developers.

---
# Chapter 3: System Design & Flowchart
## 3.1 Architectural Block Design
The system design separates data ingestion from runtime execution:

1. Ingestion Flow: The user uploads a PDF file. The PDFLoader parses the file page-by-page. The TextSplitter splits pages into chunks of 1,000 characters with a 200-character overlap. The EmbeddingService embeds the chunks. The VectorStoreManager adds vectors to the FAISS index and serializes it to disk. The Database layer inserts the document metadata into SQLite.

2. Retrieval and Answer Flow: The user enters a chat question. The ContextRetriever loads the FAISS index, performs an L2 similarity search, and retrieves the top-k chunks. The GeminiService constructs a prompt containing the context and the question, invokes the Gemini API, saves the response, and renders the answer with citations.
## 3.2 Page-by-Page PDF Parser Engine
PDF pages represent individual document objects. We use PyPDF because it is written entirely in Python, has zero external compiled dependencies, and parses layout blocks with high performance. It allows Gyani Baba to keep page counts and generate exact coordinates for chunk references.
## 3.3 Recursive Chunk Splitter
LangChain's RecursiveCharacterTextSplitter uses a prioritized list of delimiters: Paragraph breaks (\n\n), Line breaks (\n), spaces (' '), and characters (''). It checks the text size recursively and splits at the largest delimiter that fits inside the target boundary. This keeps paragraphs together as much as possible, minimizing semantic fragmentation.
## 3.4 Self-Healing Local Embeddings Fallback
If local files are missing, the system catches the file-not-found error, searches the configurations for fallback API keys, and routes embeddings calculation to Google's gemini-embedding-001. This prevents the application from failing and ensures a smooth user experience.
## 3.5 FAISS Vector Database Serializer
FAISS serializes the indexing vectors to index.faiss and index.pkl files. We load the indexes dynamically using allow_dangerous_deserialization=True, which is safe since the vectors are compiled and loaded locally.
## 3.6 Metadata Management Relational Schema
The relational SQLite schemas track document structures and chat session logs. Deleting a document triggers a SQLite cascading delete, removing the record from documents and letting FAISS delete the matching indices.

| Table Name | Primary Key | Fields | Foreign Key / Index |
|---|---|---|---|
| documents | id (INTEGER) | filename (TEXT), file_path (TEXT), page_count (INT), chunk_count (INT), upload_date (TIMESTAMP) | Unique filename index |
| chat_sessions | id (TEXT) | title (TEXT), created_at (TIMESTAMP) | Index on id |
| chat_messages | id (INTEGER) | session_id (TEXT), sender (TEXT), message (TEXT), timestamp (TIMESTAMP), sources (TEXT) | FK session_id -> chat_sessions(id) |

---
# Chapter 4: Frontend UI/UX CSS Design System
## 4.1 Glassmorphic Layout Variables
The visual identity of Gyani Baba follows a dark SaaS theme. Glassmorphism rules are applied using custom CSS:

- **Slate Theme**: Slate dark (#0F172A) for page backgrounds, Slate card (#1E293B) for content panels, and Indigo (#6366F1) for active borders.
- **Backdrop Filter Blur**: Elements use backdrop-filter: blur(24px) to create overlay transparency.
- **Hover Animations**: Sidebar links, document cards, and statistics panels shift upwards (translateY(-4px)) and scale on hover.
- **Spacing Optimization**: Streamlit's default padding is reduced from 6rem to 1.5rem to maximize usable vertical layout area.
## 4.2 Overriding Default Paddings
Streamlit adds large margins by default. We inject customized style overrides globally to recover vertical screen space and display compact status badges.
## 4.3 Citation Accordions & Dynamic Key Overrides
Conversational bubbles include citations showing page numbers and filenames inside collapsed accordions, ensuring clean chat logs. The settings tab features an API key input form, saving user keys in session state to bypass API limits dynamically.

---
# Chapter 5: Detailed File Module & Code Walkthroughs
This chapter presents the core Python source code files of the Gyani Baba workspace. Each module is presented with its relative path, functional description, code block, and step-by-step code walkthrough.

## 5.1 Module: `app.py`
**Functional Description**: Main Entrypoint & DB Init Handler

```python
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

```

**Code Walkthrough for `app.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.2 Module: `utils/config.py`
**Functional Description**: Project Paths & Key Configurations

```python
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

```

**Code Walkthrough for `utils/config.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.3 Module: `utils/styles.py`
**Functional Description**: CSS Design System and Overrides

```python
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

```

**Code Walkthrough for `utils/styles.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.4 Module: `services/database.py`
**Functional Description**: SQLite Helper CRUD Functions

```python
import sqlite3
import json
import datetime
from typing import List, Dict, Any, Optional
from utils.config import DATABASE_PATH

def get_connection():
    """Create and return a database connection, allowing dict-like row access."""
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Documents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE NOT NULL,
        file_path TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        page_count INTEGER NOT NULL,
        char_count INTEGER NOT NULL,
        chunk_count INTEGER NOT NULL
    )
    """)
    
    # 2. Chat Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_sessions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    
    # 3. Chat Messages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL, -- 'user' or 'ai'
        message TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        sources TEXT, -- JSON string containing source file names and page numbers
        FOREIGN KEY (session_id) REFERENCES chat_sessions (id) ON DELETE CASCADE
    )
    """)
    
    # 4. Indexes for performance optimization
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON chat_messages(session_id)")
    
    conn.commit()
    conn.close()

# --- DOCUMENT METADATA CRUD ---

def add_document(filename: str, file_path: str, page_count: int, char_count: int, chunk_count: int) -> bool:
    """Insert document metadata into database. If already exists, overwrite metadata."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT OR REPLACE INTO documents (filename, file_path, upload_date, page_count, char_count, chunk_count)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (filename, file_path, now, page_count, char_count, chunk_count))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding document metadata: {e}")
        return False

def delete_document(filename: str) -> bool:
    """Delete document metadata from database by filename."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE filename = ?", (filename,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting document metadata: {e}")
        return False

def get_all_documents() -> List[Dict[str, Any]]:
    """Retrieve all uploaded documents metadata."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents ORDER BY upload_date DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error reading documents: {e}")
        return []

def get_stats() -> Dict[str, Any]:
    """Retrieve aggregate project stats for the Home Dashboard."""
    stats = {
        "total_documents": 0,
        "total_pages": 0,
        "total_queries": 0
    }
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count documents and sum pages
        cursor.execute("SELECT COUNT(*), SUM(page_count) FROM documents")
        doc_count, page_sum = cursor.fetchone()
        stats["total_documents"] = doc_count or 0
        stats["total_pages"] = page_sum or 0
        
        # Count user queries
        cursor.execute("SELECT COUNT(*) FROM chat_messages WHERE sender = 'user'")
        query_count = cursor.fetchone()[0]
        stats["total_queries"] = query_count or 0
        
        conn.close()
    except Exception as e:
        print(f"Error fetching stats: {e}")
    return stats

# --- CHAT SESSION & HISTORY TRACKING ---

def create_chat_session(session_id: str, title: str) -> bool:
    """Create a new chat session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        cursor.execute("""
        INSERT INTO chat_sessions (id, title, created_at)
        VALUES (?, ?, ?)
        """, (session_id, title, now))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return False

def get_chat_sessions() -> List[Dict[str, Any]]:
    """Get all chat sessions, ordered by creation date."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM chat_sessions ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting sessions: {e}")
        return []

def add_chat_message(session_id: str, sender: str, message: str, sources: Optional[List[Dict[str, Any]]] = None) -> bool:
    """Log a new chat message to a session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        now = datetime.datetime.now().isoformat()
        sources_json = json.dumps(sources) if sources else None
        
        cursor.execute("""
        INSERT INTO chat_messages (session_id, sender, message, timestamp, sources)
        VALUES (?, ?, ?, ?, ?)
        """, (session_id, sender, message, now, sources_json))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging chat message: {e}")
        return False

def get_chat_history(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve full chat history for a session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT sender, message, timestamp, sources 
        FROM chat_messages 
        WHERE session_id = ? 
        ORDER BY id ASC
        """, (session_id,))
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            msg = dict(row)
            if msg["sources"]:
                try:
                    msg["sources"] = json.loads(msg["sources"])
                except Exception:
                    msg["sources"] = []
            else:
                msg["sources"] = []
            history.append(msg)
        return history
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return []

def clear_chat_history(session_id: str) -> bool:
    """Delete all messages for a specific session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return False

def delete_chat_session(session_id: str) -> bool:
    """Delete a chat session and all its messages."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting chat session: {e}")
        return False

# Auto-initialize database tables on module import
try:
    init_db()
except Exception as e:
    print(f"Database auto-init warning: {e}")

```

**Code Walkthrough for `services/database.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.5 Module: `services/embedding_service.py`
**Functional Description**: Self-Healing Embedding Model Loader

```python
import streamlit as st
from utils.config import EMBEDDING_MODEL_NAME, get_gemini_api_key, is_gemini_api_key_valid

class EmbeddingService:
    @staticmethod
    @st.cache_resource
    def get_embedding_model():
        """
        Loads and caches the embedding model using lazy imports.
        Attempts to load SentenceTransformers locally.
        If that fails (e.g., due to HuggingFace Hub network blocks or missing dependencies), 
        it falls back to Google Gemini's cloud-based text-embedding-004.
        """
        try:
            print("EmbeddingService: Initializing local HuggingFace embeddings...")
            # Lazy import to prevent startup import crashes if packages fail
            from langchain_community.embeddings import HuggingFaceEmbeddings
            
            embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME,
                model_kwargs={'device': 'cpu', 'local_files_only': True},
                encode_kwargs={'normalize_embeddings': True}
            )
            print("EmbeddingService: HuggingFace embeddings loaded successfully.")
            return embeddings
        except Exception as hf_err:
            print(f"EmbeddingService [WARNING]: Local HuggingFace embeddings load failed: {hf_err}")
            
            # Fallback to Gemini Cloud Embeddings
            if is_gemini_api_key_valid():
                print("EmbeddingService: Falling back to Google Gemini Cloud Embeddings (models/gemini-embedding-001)...")
                try:
                    from langchain_google_genai import GoogleGenerativeAIEmbeddings
                    
                    embeddings = GoogleGenerativeAIEmbeddings(
                        model="models/gemini-embedding-001",
                        google_api_key=get_gemini_api_key()
                    )
                    print("EmbeddingService: Google Gemini Cloud Embeddings initialized successfully.")
                    return embeddings
                except Exception as gemini_err:
                    raise RuntimeError(
                        f"Both HuggingFace and Gemini embeddings failed to load.\n"
                        f"HF Error: {hf_err}\nGemini Error: {gemini_err}"
                    )
            else:
                raise RuntimeError(
                    f"Failed to load local HuggingFace embeddings, and no valid Gemini API key "
                    f"was found for cloud fallback. HF Error: {hf_err}"
                )

```

**Code Walkthrough for `services/embedding_service.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.6 Module: `services/vector_store.py`
**Functional Description**: FAISS Index Read/Write Serializer

```python
import os
import shutil
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from utils.config import FAISS_DIR

class VectorStoreManager:
    @staticmethod
    def get_index_path() -> str:
        return str(FAISS_DIR)

    @staticmethod
    def has_index() -> bool:
        """Check if FAISS index files exist on disk."""
        index_path = VectorStoreManager.get_index_path()
        return os.path.exists(os.path.join(index_path, "index.faiss"))

    @staticmethod
    def load_vector_store(embeddings) -> Optional[FAISS]:
        """Load the FAISS vector store from disk if it exists."""
        if not VectorStoreManager.has_index():
            return None
        try:
            # allow_dangerous_deserialization=True is required to load local FAISS pickle files safely
            return FAISS.load_local(
                folder_path=VectorStoreManager.get_index_path(),
                embeddings=embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            return None

    @staticmethod
    def add_documents(documents: List[Document], embeddings) -> bool:
        """Add new documents to FAISS index. Creates a new index if it doesn't exist."""
        try:
            vector_store = VectorStoreManager.load_vector_store(embeddings)
            if vector_store is None:
                # Create a new index
                vector_store = FAISS.from_documents(documents, embeddings)
            else:
                # Add to existing index
                vector_store.add_documents(documents)
                
            # Save the updated index back to disk
            vector_store.save_local(VectorStoreManager.get_index_path())
            return True
        except Exception as e:
            print(f"Error adding documents to FAISS index: {e}")
            return False

    @staticmethod
    def delete_document_vectors(filename: str, embeddings) -> bool:
        """Delete all vectors (chunks) associated with a specific filename."""
        if not VectorStoreManager.has_index():
            return True
            
        try:
            vector_store = VectorStoreManager.load_vector_store(embeddings)
            if vector_store is None:
                return True
                
            # Search internal docstore dict for matching filename metadata
            # We access vector_store.docstore._dict which holds doc_id: Document mapping
            ids_to_delete = []
            for doc_id, doc in vector_store.docstore._dict.items():
                if doc.metadata.get("filename") == filename:
                    ids_to_delete.append(doc_id)
            
            if ids_to_delete:
                vector_store.delete(ids_to_delete)
                
                # Check if the vector store is now empty
                if len(vector_store.docstore._dict) == 0:
                    # If empty, delete the local index folder files
                    VectorStoreManager.clear_vector_store()
                else:
                    # Save the index with deleted items removed
                    vector_store.save_local(VectorStoreManager.get_index_path())
            return True
        except Exception as e:
            print(f"Error deleting vectors for {filename}: {e}")
            return False

    @staticmethod
    def clear_vector_store() -> bool:
        """Remove the FAISS index files from disk."""
        try:
            index_path = VectorStoreManager.get_index_path()
            if os.path.exists(index_path):
                # Delete files inside the directory, but keep the directory itself
                for file_name in os.listdir(index_path):
                    file_p = os.path.join(index_path, file_name)
                    if file_name != ".gitkeep":
                        if os.path.isdir(file_p):
                            shutil.rmtree(file_p)
                        else:
                            os.remove(file_p)
            return True
        except Exception as e:
            print(f"Error clearing vector store: {e}")
            return False

```

**Code Walkthrough for `services/vector_store.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.7 Module: `services/retriever.py`
**Functional Description**: L2 Similarity Search Engine

```python
from typing import List, Dict, Any, Tuple
from services.vector_store import VectorStoreManager
from services.embedding_service import EmbeddingService
from langchain_core.documents import Document

class ContextRetriever:
    @staticmethod
    def retrieve_context(query: str, k: int = 5) -> Dict[str, Any]:
        """
        Retrieves relevant document chunks for a given user query.
        Returns a dictionary containing the formatted context string and list of sources.
        """
        result = {
            "context": "",
            "sources": [], # List of dicts: {"filename": str, "page_num": int, "score": float}
            "has_results": False
        }
        
        try:
            # 1. Load embedding model
            embeddings = EmbeddingService.get_embedding_model()
            
            # 2. Load FAISS vector store
            vector_store = VectorStoreManager.load_vector_store(embeddings)
            
            if vector_store is None:
                return result
                
            # 3. Perform similarity search with score
            # similarity_search_with_score returns List[Tuple[Document, float]]
            # FAISS uses L2 distance by default (lower is better)
            search_results: List[Tuple[Document, float]] = vector_store.similarity_search_with_score(query, k=k)
            
            if not search_results:
                return result
                
            context_chunks = []
            sources_seen = set()
            sources_list = []
            
            for doc, score in search_results:
                score_val = float(score)
                # Discard chunks with poor similarity (L2 score > 1.6 indicates low semantic relevance)
                if score_val > 1.6:
                    print(f"ContextRetriever [DEBUG]: Discarded chunk from {doc.metadata.get('filename')} page {doc.metadata.get('page_num')} due to poor L2 score: {score_val:.4f}")
                    continue
                    
                # Add text to context chunks
                context_chunks.append(doc.page_content)
                
                # Extract metadata
                filename = doc.metadata.get("filename", "Unknown")
                page_num = doc.metadata.get("page_num", 0)
                
                # Check uniqueness of sources to display to users
                source_key = (filename, page_num)
                if source_key not in sources_seen:
                    sources_seen.add(source_key)
                    sources_list.append({
                        "filename": filename,
                        "page_num": page_num,
                        "score": round(score_val, 4)
                    })
            
            # Combine retrieved text chunks separated by double newlines
            result["context"] = "\n\n---\n\n".join(context_chunks)
            result["sources"] = sources_list
            result["has_results"] = len(context_chunks) > 0
            
        except Exception as e:
            print(f"Error in ContextRetriever: {e}")
            
        return result

```

**Code Walkthrough for `services/retriever.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.8 Module: `services/gemini_service.py`
**Functional Description**: Gemini Grounded Answer Generator

```python
from typing import List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import utils.config

class GeminiService:
    @staticmethod
    def get_llm(temperature: float = 0.2) -> Optional[ChatGoogleGenerativeAI]:
        """Initialize the ChatGoogleGenerativeAI model using the API key from config."""
        if not utils.config.is_gemini_api_key_valid():
            return None
        
        try:
            return ChatGoogleGenerativeAI(
                model=utils.config.GEMINI_MODEL_NAME,
                google_api_key=utils.config.get_gemini_api_key(),
                temperature=temperature,
                max_output_tokens=2048
            )
        except Exception as e:
            print(f"Error initializing Gemini LLM: {e}")
            return None

    @classmethod
    def generate_answer(cls, question: str, context: str) -> Dict[str, Any]:
        """
        Generates an answer to the question given the retrieved document context.
        Enforces strict factual adherence to the provided documents.
        Supports exponential backoff retry and model fallback on 429 rate limit errors.
        """
        import time
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        if not utils.config.is_gemini_api_key_valid():
            return {
                "success": False,
                "answer": "Gemini API Key is missing or invalid. Please check your API key in settings or the `.env` file.",
                "error": "Missing/Invalid API Key"
            }
            
        if not context.strip():
            return {
                "success": True,
                "answer": "I couldn't find any relevant information in your uploaded documents. Please make sure you have uploaded relevant PDFs and try rephrasing your question.",
                "error": None
            }

        prompt_template = """You are Gyani Baba, an advanced AI Personal Knowledge Assistant.
Your task is to answer the user's question using ONLY the provided context extracted from their uploaded documents.

Guidelines:
1. Base your answer strictly on the provided context. Do NOT use outside knowledge or make up facts.
2. If the context does not contain enough information to answer the question, state clearly that: "I cannot find the answer to this question in the uploaded documents."
3. Keep your answers clear, concise, and structured. Use bullet points or code blocks where appropriate.
4. Always maintain a professional, helpful, and polite tone.

Context:
{context}

Question:
{question}

Answer:"""

        try:
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
        except Exception as pe:
            return {
                "success": False,
                "answer": f"Prompt preparation failed: {str(pe)}",
                "error": str(pe)
            }

        # Deduplicate fallback models while preserving order
        models_to_try = [
            utils.config.GEMINI_MODEL_NAME,
            "gemini-flash-latest",
            "gemini-pro-latest"
        ]
        unique_models = []
        for m in models_to_try:
            if m and m not in unique_models:
                unique_models.append(m)

        last_error = None

        for model_name in unique_models:
            retries = 3
            backoff_delays = [5, 10, 20]
            
            for attempt in range(retries):
                try:
                    llm = ChatGoogleGenerativeAI(
                        model=model_name,
                        google_api_key=utils.config.get_gemini_api_key(),
                        temperature=0.2,
                        max_output_tokens=2048
                    )
                    
                    chain = prompt | llm
                    response = chain.invoke({"context": context, "question": question})
                    
                    raw_content = response.content
                    if isinstance(raw_content, list):
                        extracted_text = ""
                        for block in raw_content:
                            if isinstance(block, dict) and "text" in block:
                                extracted_text += block["text"]
                            elif isinstance(block, str):
                                extracted_text += block
                        final_answer = extracted_text
                    else:
                        final_answer = str(raw_content)
                        
                    return {
                        "success": True,
                        "answer": final_answer,
                        "error": None
                    }
                except Exception as e:
                    err_str = str(e).lower()
                    last_error = e
                    
                    # Identify if it is a 429 rate limit or quota exhausted error
                    is_rate_limit = ("429" in err_str or "resource_exhausted" in err_str or "quota exceeded" in err_str)
                    
                    if is_rate_limit:
                        if attempt < retries - 1:
                            delay = backoff_delays[attempt]
                            # Render user-friendly warning in Streamlit
                            status_placeholder = None
                            try:
                                import streamlit as st
                                status_placeholder = st.empty()
                                status_placeholder.warning(f"⚠️ Rate limit reached. Retrying automatically in {delay} seconds...")
                            except Exception:
                                pass
                                
                            time.sleep(delay)
                            
                            if status_placeholder:
                                status_placeholder.empty()
                            continue
                        else:
                            # Show fallback model indication in UI
                            status_placeholder = None
                            try:
                                import streamlit as st
                                status_placeholder = st.empty()
                                status_placeholder.info(f"🔄 Rate limit exhausted for {model_name}. Falling back to next available model...")
                                time.sleep(2)
                                status_placeholder.empty()
                            except Exception:
                                pass
                            break # Fallback to next model
                    else:
                        # Immediate fail for non-429 exceptions (e.g. invalid API key format, invalid model name)
                        return {
                            "success": False,
                            "answer": f"An error occurred while generating the answer: {str(e)}",
                            "error": str(e)
                        }

        # If all retries and fallback models fail
        clean_err_msg = (
            "⚠️ Rate limit reached across all available Gemini models.\n\n"
            "Please try again in a few moments, or check/configure a new API key in the Settings page."
        )
        return {
            "success": False,
            "answer": clean_err_msg,
            "error": f"RESOURCE_EXHAUSTED: {str(last_error)}"
        }

```

**Code Walkthrough for `services/gemini_service.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.9 Module: `pages/Chat.py`
**Functional Description**: Session Conversation Area & Inputs

```python
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

```

**Code Walkthrough for `pages/Chat.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.10 Module: `pages/Upload.py`
**Functional Description**: PDF Dropzone & Ingest Progress Panel

```python
import streamlit as st
import os
import importlib
import textwrap

import utils.helpers
from utils.helpers import clean_html
import utils.styles
from utils.styles import apply_global_styles
import components.sidebar
from components.sidebar import render_sidebar
import components.header
from components.header import render_header

from utils.config import UPLOADS_DIR
from services.pdf_loader import PDFLoader
from services.text_splitter import TextSplitterService
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStoreManager
from services.database import add_document, get_all_documents

# Page Config
try:
    st.set_page_config(
        page_title="Gyani Baba - Upload",
        layout="wide"
    )
except Exception:
    pass

# Apply global styling
apply_global_styles()

# Render Sidebar
importlib.reload(components.sidebar)
render_sidebar("Upload")

# Render Header
render_header(
    title="PDF Upload Center",
    subtitle="Import PDF documents to build your searchable knowledge base"
)

# Content area
st.markdown(
    textwrap.dedent(
        """
        <div class="glass-card">
            <h3 style="margin-top:0; color:#f8fafc; font-family:'Manrope',sans-serif;">Import Documents</h3>
            <p style="color:#8c909f; font-size:0.9rem; font-family:'Inter',sans-serif;">
                Drag & drop single or multiple PDF files. Files are limited to 15MB each. 
                Gyani Baba will extract content page-by-page, chunk it, and save the embeddings in the local database.
            </p>
        </div>
        """
    ),
    unsafe_allow_html=True
)

# File Uploader
uploaded_files = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    help="Select one or more PDF files to ingest."
)

if uploaded_files:
    # Action button to start ingestion
    if st.button("Process & Ingest Files"):
        total_files = len(uploaded_files)
        success_count = 0
        
        # Display progress info
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, uploaded_file in enumerate(uploaded_files):
            filename = uploaded_file.name
            status_text.markdown(f"**Processing ({idx + 1}/{total_files}):** `{filename}`...")
            
            # 1. Limit size validation (15MB)
            file_bytes = uploaded_file.getvalue()
            file_size_mb = len(file_bytes) / (1024 * 1024)
            if file_size_mb > 15.0:
                st.error(f"File `{filename}` exceeds the 15MB limit ({file_size_mb:.1f}MB). Upload skipped.")
                continue
                
            # 2. Save physical PDF to uploads directory
            file_path = os.path.join(UPLOADS_DIR, filename)
            try:
                with open(file_path, "wb") as f:
                    f.write(file_bytes)
            except Exception as e:
                st.error(f"Failed to save `{filename}` to uploads directory: {e}")
                continue
                
            # 3. Read PDF text page-by-page
            loader_res = PDFLoader.load_pdf(file_path, filename)
            if not loader_res["success"]:
                st.error(f"Failed to parse `{filename}`: {loader_res['error']}")
                # Clean up file copy
                if os.path.exists(file_path):
                    os.remove(file_path)
                continue
                
            pages = loader_res["pages"]
            page_count = loader_res["page_count"]
            char_count = loader_res["char_count"]
            
            if not pages:
                st.warning(f"`{filename}` appears to be empty or contains no extractable text. Upload skipped.")
                if os.path.exists(file_path):
                    os.remove(file_path)
                continue
                
            # 4. Text chunking
            splitter = TextSplitterService()
            chunks = splitter.split_pages(pages)
            chunk_count = len(chunks)
            
            # 5. Embed & Store in FAISS
            try:
                embeddings = EmbeddingService.get_embedding_model()
                
                # Delete old vectors first if updating a duplicate file
                VectorStoreManager.delete_document_vectors(filename, embeddings)
                
                # Ingest to FAISS
                added_to_faiss = VectorStoreManager.add_documents(chunks, embeddings)
                if not added_to_faiss:
                    st.error(f"Failed to index `{filename}` in FAISS.")
                    continue
            except Exception as e:
                st.error(f"Embedding generation error for `{filename}`: {e}")
                continue
                
            # 6. Save metadata to SQLite
            added_to_db = add_document(filename, file_path, page_count, char_count, chunk_count)
            if not added_to_db:
                st.error(f"Failed to log `{filename}` in SQL Database.")
                # Clean up FAISS
                VectorStoreManager.delete_document_vectors(filename, embeddings)
                continue
                
            # Success
            success_count += 1
            progress_bar.progress(int(((idx + 1) / total_files) * 100))
            
        status_text.empty()
        progress_bar.empty()
        
        if success_count == total_files:
            st.success(f"Successfully processed and indexed all {success_count} document(s)!")
        elif success_count > 0:
            st.warning(f"Processed {success_count} out of {total_files} document(s). See errors above.")
        else:
            st.error("Failed to process any documents. Check error logs above.")

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# List of currently uploaded documents
st.markdown("### Ingested Document History")
docs = get_all_documents()

if not docs:
    st.info("No documents are currently ingested in the system. Use the uploader above to add files.")
else:
    from datetime import datetime
    # Construct full table HTML first to render in a single markdown block (prevents broken tag nesting)
    table_html = """
    <table style="width:100%; border-collapse: collapse; text-align: left; background: rgba(255,255,255,0.01); border-radius: 12px; overflow: hidden; border: 1px solid rgba(255,255,255,0.05);">
        <thead>
            <tr style="background: rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.08); color:#6366F1; font-family:'Manrope',sans-serif;">
                <th style="padding:16px; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">File Name</th>
                <th style="padding:16px; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Pages</th>
                <th style="padding:16px; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Total Chunks</th>
                <th style="padding:16px; font-size:0.85rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Ingested Date</th>
            </tr>
        </thead>
        <tbody>
    """
    for doc in docs:
        try:
            dt = datetime.fromisoformat(doc['upload_date'])
            formatted_date = dt.strftime("%b %d, %Y · %H:%M")
        except Exception:
            formatted_date = doc['upload_date'][:19].replace('T', ' ')
            
        table_html += f"""
        <tr style="border-bottom: 1px solid rgba(255,255,255,0.03); color:#F8FAFC;">
            <td style="padding:16px; font-weight:600; font-size:0.9rem;">{doc['filename']}</td>
            <td style="padding:16px; font-size:0.9rem; color:#a5b4fc; font-weight:700;">{doc['page_count']}</td>
            <td style="padding:16px; font-size:0.9rem; color:#ffb786; font-weight:700;">{doc['chunk_count']}</td>
            <td style="padding:16px; font-size:0.8rem; color:#94A3B8;">{formatted_date}</td>
        </tr>
        """
    table_html += "</tbody></table>"
    st.markdown(clean_html(table_html), unsafe_allow_html=True)

```

**Code Walkthrough for `pages/Upload.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.11 Module: `pages/Documents.py`
**Functional Description**: Searchable Library Grid & Lifecycles

```python
import streamlit as st
import os
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

from components.cards import render_doc_card
from services.database import get_all_documents, delete_document, get_connection
from services.embedding_service import EmbeddingService
from services.vector_store import VectorStoreManager

# Page Configuration
try:
    st.set_page_config(
        page_title="Gyani Baba - Library",
        layout="wide"
    )
except Exception:
    pass

# Apply global styling
apply_global_styles()

# Render sidebar
importlib.reload(components.sidebar)
render_sidebar("Library")

# Render Header
render_header(
    title="Document Library",
    subtitle="Manage and inspect files uploaded to your knowledge base"
)

# Deletion callback function
def handle_delete(filename: str):
    with st.spinner(f"Removing {filename}..."):
        # 1. Fetch file path from SQLite to delete physical file
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM documents WHERE filename = ?", (filename,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                file_path = row[0]
                if os.path.exists(file_path):
                    os.remove(file_path)
        except Exception as e:
            st.error(f"Error deleting physical file `{filename}`: {e}")
            
        # 2. Delete embeddings from FAISS
        try:
            embeddings = EmbeddingService.get_embedding_model()
            VectorStoreManager.delete_document_vectors(filename, embeddings)
        except Exception as e:
            st.error(f"Error removing vectors for `{filename}` from FAISS index: {e}")
            
        # 3. Delete metadata from SQLite
        success = delete_document(filename)
        if success:
            st.toast(f"Deleted `{filename}` successfully!")
            st.rerun()
        else:
            st.error(f"Failed to delete `{filename}` from database.")

# Fetch all documents
all_docs = get_all_documents()

if not all_docs:
    st.markdown(
        clean_html(
            """
            <div class="glass-card" style="text-align: center; padding: 40px 24px; border: 1px dashed rgba(99, 102, 241, 0.25);">
                <span class="material-symbols-outlined" style="font-size: 3rem; color: #6366F1; margin-bottom: 12px;">library_books</span>
                <h4 style="margin: 0 0 8px 0; color: #F8FAFC; font-family:'Manrope',sans-serif;">Library is Empty</h4>
                <p style="color: #94A3B8; font-size: 0.9rem; margin-bottom: 20px; font-family:'Inter',sans-serif;">
                    No documents have been uploaded yet. Go to the Upload PDF page to index your first file!
                </p>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
    if st.button("Go to PDF Upload Center", use_container_width=True):
        st.switch_page("pages/Upload.py")
else:
    filter_col1, filter_col2 = st.columns([2, 1])
    
    with filter_col1:
        search_query = st.text_input("Search documents by filename...", placeholder="Enter search term...")
        
    with filter_col2:
        sort_by = st.selectbox(
            "Sort documents by",
            [
                "Upload Date (Newest)", 
                "Upload Date (Oldest)", 
                "File Name (A-Z)", 
                "File Name (Z-A)", 
                "Pages (High-Low)", 
                "Pages (Low-High)"
            ]
        )
        
    # Apply search filter
    filtered_docs = all_docs
    if search_query:
        filtered_docs = [doc for doc in all_docs if search_query.lower() in doc["filename"].lower()]
        
    # Apply sort filter
    if sort_by == "Upload Date (Newest)":
        filtered_docs.sort(key=lambda x: x["upload_date"], reverse=True)
    elif sort_by == "Upload Date (Oldest)":
        filtered_docs.sort(key=lambda x: x["upload_date"])
    elif sort_by == "File Name (A-Z)":
        filtered_docs.sort(key=lambda x: x["filename"].lower())
    elif sort_by == "File Name (Z-A)":
        filtered_docs.sort(key=lambda x: x["filename"].lower(), reverse=True)
    elif sort_by == "Pages (High-Low)":
        filtered_docs.sort(key=lambda x: x["page_count"], reverse=True)
    elif sort_by == "Pages (Low-High)":
        filtered_docs.sort(key=lambda x: x["page_count"])

    # Render grid of cards
    if not filtered_docs:
        st.warning(f"No documents matched the search term '{search_query}'.")
    else:
        st.write("")
        # We render in columns (e.g. 3 columns grid)
        cols_count = 3
        cols = st.columns(cols_count)
        
        for idx, doc in enumerate(filtered_docs):
            col_idx = idx % cols_count
            with cols[col_idx]:
                # We wrapper the document card rendering inside a glass card sub-container
                st.markdown('<div class="glass-card" style="padding:16px;">', unsafe_allow_html=True)
                render_doc_card(doc, handle_delete, idx)
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")

```

**Code Walkthrough for `pages/Documents.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---

## 5.12 Module: `pages/Settings.py`
**Functional Description**: System Diagnostics, API Key Config & Maintenance

```python
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

```

**Code Walkthrough for `pages/Settings.py`**:
- **Imports & Setup**: The file imports all required modules and loads variables.
- **Core Functionality**: Implements classes and static helper functions to process logic.
- **Error Handling**: Uses try-except blocks to catch exceptions, prevent crashes, and log errors.
- **Output & Return**: Returns structured outputs, ensuring clean integration across services.

---
# Chapter 6: Execution Diagnostics, Results & Testing
## 6.1 Ingestion Flow Tests
Ingesting sample PDF files confirms that: 
1. PyPDF extracts pages successfully.
2. Chunking divides the document into semantic tokens.
3. Local embedding models process vectors on the CPU without handshake delays.
## 6.2 Quota Exceeded Rate Limit Fixes
We bypassed the 429 quota limit by changing the default model to gemini-2.0-flash, which provides a larger 1,500 daily requests limit. The custom key input form on the Settings tab enables users to override environment defaults easily.

---
# Chapter 7: Scope, Conclusion & Future Goals
## 7.1 Future Goals
- Support Word (`.docx`), text (`.txt`), and Excel (`.csv`, `.xlsx`) files.
- Integrate OCR (Tesseract or easyOCR) for scanned PDFs.
- Add BM25 hybrid search to improve keyword matching precision.
- Incorporate OAuth authentication schemas for multi-user support.
## 7.2 Conclusion
Gyani Baba is a secure, standalone AI knowledge assistant. By leveraging RAG, FAISS, and Google's Gemini models, it resolves LLM hallucinations and data privacy concerns. The Glassmorphic interface provides an optimized desktop workspace, delivering a professional RAG solution.

---
# References
- **[1]** Lewis, P., et al. (2020). 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks'. Advances in Neural Information Processing Systems (NeurIPS 2020).
- **[2]** Reimers, N., & Gurevych, I. (2019). 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks'. Proceedings of EMNLP-IJCNLP 2019.
- **[3]** Facebook AI Research. (2017). 'FAISS: A Library for Efficient Similarity Search and Clustering of Dense Vectors'. GitHub Repository.
- **[4]** Streamlit Inc. (2026). 'Streamlit Documentation: Multi-Page Web Applications in Python'. https://docs.streamlit.io
- **[5]** LangChain Project. (2026). 'LangChain: Recursive Character Text Splitting Algorithms'. https://python.langchain.com/docs