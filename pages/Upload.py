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
