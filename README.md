# Gyani Baba 🤖
### AI Personal Knowledge Assistant

Gyani Baba is a production-quality, modern, and modular Generative AI application built to act as a **Personal Knowledge Assistant**. It allows users to upload PDF documents, processes and indexes them into a local vector search index, and answers natural language questions grounded strictly in the content of the uploaded files.

The system features a beautiful dark-mode interface styled with modern Glassmorphic design principles.

---

## 🚀 Key Features

* **Home Dashboard**: Modern welcome screen containing project insights, recent document summaries, and quick statistics (Total Documents, Total Pages, AI Conversations Logged).
* **Document Ingestion**: Multi-file drag-and-drop uploader supporting size validation, page-by-page text extraction (PyPDF), and semantic text chunking (LangChain RecursiveTextSplitter).
* **Self-Healing Embeddings**: Utilizes local `sentence-transformers/all-MiniLM-L6-v2` embeddings for offline computation, automatically falling back to Google Cloud Gemini Embeddings (`models/text-embedding-004`) if local HuggingFace Hub downloads are blocked.
* **FAISS Vector Database**: Fast local vector storage with in-memory loading, serialization, and clean sub-index deletions by document filename.
* **Persistent Chat Sessions**: Persistent, ChatGPT-style conversational history saved in a local SQLite database, allowing multiple concurrent chat logs that persist across page reloads.
* **Document Library Grid**: Searchable library of all uploaded PDFs displaying page count, chunk counts, and an integrated lifecycle deletion utility that cleans up files, databases, and vector stores.
* **Diagnostics Panel**: Health monitoring dashboard evaluating database sizes, index metadata, and API key connectivity, alongside full-system reset utilities.

---

## 🏛️ System Architecture

The following diagram illustrates the application flow and component structure:

```
                     +----------------------------+
                     |    User Interface (Web)    |
                     |         (Streamlit)        |
                     +--------------+-------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
  +---------+---------+                           +---------+---------+
  |  Upload Controller|                           |   Chat Controller |
  +---------+---------+                           +---------+---------+
            |                                               |
            v                                               v
  +---------+---------+                           +---------+---------+
  |    PDF Reader     |                           | Vector Searcher   |
  |     (PyPDF)       |                           |  (FAISS DB)       |
  +---------+---------+                           +---------+---------+
            |                                               |
            v                                               v
  +---------+---------+                           +---------+---------+
  |  Text Splitter    |                           | Gemini Generator  |
  |  (LangChain)      |                           | (langchain-google)|
  +---------+---------+                           +---------+---------+
            |                                               |
            v                                               v
  +---------+---------+                           +---------+---------+
  | Embeddings Engine |                           | SQLite Database   |
  | (Local / Cloud)   |                           | (app.db Metadata) |
  +-------------------+                           +-------------------+
```

---

## 📂 Project Structure

```
project/
│
├── app.py                      # Main entrypoint & initialization config
│
├── pages/                      # Multi-page application views
│   ├── Dashboard.py            # Welcome page, stats, and recent logs
│   ├── Upload.py               # PDF dropzone and ingestion progress
│   ├── Chat.py                 # Multi-session conversation view & source citations
│   ├── Documents.py            # Library grid, filters, and item deletions
│   └── Settings.py             # Diagnostis checkups and systems resets
│
├── components/                 # Reusable UI layouts and blocks
│   ├── sidebar.py              # Branding and system status dots
│   ├── cards.py                # Statistics and document visual cards
│   ├── chat_ui.py              # User/AI bubble renders & download logs
│   └── header.py               # Time-aware greeting headers
│
├── services/                   # Deep logic layers and API managers
│   ├── database.py             # SQLite helper and query CRUD operations
│   ├── pdf_loader.py           # Text extractor wrapper
│   ├── text_splitter.py        # Token-safe recursive text chunker
│   ├── embedding_service.py    # Local SentenceTransformers + Gemini Fallback
│   ├── vector_store.py         # FAISS read, save, and chunk deletion
│   ├── gemini_service.py       # Google Gemini LLM factual-only QA prompter
│   └── retriever.py            # Context collector & deduplicator
│
├── utils/                      # Configurations and shared values
│   ├── config.py               # Directory setups and path definitions
│   ├── styles.py               # Glassmorphic global CSS stylesheets
│   └── helpers.py              # Date converters, size logs, greetings
│
├── database/                   # Directory containing persistent SQLite app.db
├── uploads/                    # Directory containing saved source PDFs
├── faiss_index/                # Directory containing indexed vector databases
│
├── requirements.txt            # Python dependencies configuration
├── README.md                   # Documentation
├── .env.example                # Shell environment variable structure
└── .gitignore                  # Git tracking rules
```

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.9, 3.10, 3.11, or 3.12 (Python 3.13 is fully supported)
* Pip package manager

### 1. Clone or Copy the Repository
Navigate to the root directory `d:\Gyani Baba`.

### 2. Install Dependencies
Run the command below in your terminal to install the latest stable package bindings:
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
1. Duplicate `.env.example` and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and paste your Gemini API Key retrieved from [Google AI Studio](https://aistudio.google.com/):
   ```env
   GEMINI_API_KEY=AIzaSy...your_gemini_api_key...
   ```

---

## 💻 Running Locally

To launch the Streamlit server and boot up the UI:
```bash
streamlit run app.py
```
This will automatically initialize directories, SQLite database, and launch your default browser pointing to `http://localhost:8501`.

---

## 🌐 Deployment to Streamlit Cloud

To publish this knowledge assistant on the web:
1. Push your repository to GitHub. Ensure `.env` and `database/app.db` are excluded (covered in `.gitignore`).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and link your GitHub repository, selecting `app.py` as the entrypoint.
4. Expand **Advanced settings...** and add your `GEMINI_API_KEY` under the **Secrets** text area:
   ```toml
   GEMINI_API_KEY = "AIzaSy...your_gemini_api_key..."
   ```
5. Deploy! Streamlit will install the requirements from `requirements.txt` and serve the application online.

---

## 🔮 Future Scope
* **Additional File Formats**: Expand loaders to parse `.docx`, `.txt`, `.csv`, and `.xlsx` files.
* **OCR Support**: Ingest scanned PDFs using `pytesseract` OCR library.
* **Advanced Re-ranking**: Integrate Cohere or cross-encoder re-rankers for improved document search accuracy.
* **Vector Store Migrations**: Support cloud databases like Pinecone or ChromaDB for multi-user scaling.
