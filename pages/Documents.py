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
