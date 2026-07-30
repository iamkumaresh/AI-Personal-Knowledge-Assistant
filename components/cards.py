import streamlit as st
from typing import Any
from utils.helpers import format_date, format_file_size, truncate_text, clean_html

def render_stat_card(label: str, value: Any, col=None) -> None:
    """
    Renders a premium glassmorphism statistics card.
    If 'col' is provided, renders inside that streamlit column.
    """
    card_html = f"""
    <div class="stat-card">
        <div class="stat-value" style="font-size: 2rem; font-weight: 800; background: linear-gradient(90deg, #6366F1, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-family:'Manrope',sans-serif;">{value}</div>
        <div class="stat-label" style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-top: 4px; font-family:'Inter',sans-serif;">{label}</div>
    </div>
    """
    if col:
        col.markdown(clean_html(card_html), unsafe_allow_html=True)
    else:
        st.markdown(clean_html(card_html), unsafe_allow_html=True)

def render_doc_card(doc: dict, on_delete_callback, card_index: int) -> None:
    """
    Renders a beautiful document metadata card in the Library.
    Includes a grid representation with delete button functionality.
    """
    filename = doc["filename"]
    upload_date = format_date(doc["upload_date"])
    page_count = doc["page_count"]
    chunk_count = doc["chunk_count"]
    char_count = doc["char_count"]
    
    # Grid details using glassmorphism styling
    st.markdown(
        clean_html(
            f"""
            <div class="doc-card" style="margin-bottom:0;">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                    <span class="material-symbols-outlined" style="font-size: 1.8rem; color: #6366F1;">description</span>
                    <div style="overflow: hidden; width: 100%;">
                        <h4 style="margin: 0; color: #f8fafc; font-size: 0.95rem; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; font-family:'Manrope',sans-serif;" title="{filename}">
                            {filename}
                        </h4>
                        <div style="display: flex; align-items: center; gap: 6px; margin-top: 4px;">
                            <span class="material-symbols-outlined" style="font-size: 0.85rem; color: #10B981;" title="Indexed & Searchable">search</span>
                            <span class="material-symbols-outlined" style="font-size: 0.85rem; color: #6366F1;" title="Ready to Preview">visibility</span>
                            <span style="font-size: 0.7rem; color: #94A3B8; font-family:'Inter',sans-serif; margin-left: 2px;">Uploaded: {upload_date}</span>
                        </div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin: 12px 0; font-size: 0.75rem; text-align: center; font-family:'Inter',sans-serif;">
                    <div style="background: rgba(255,255,255,0.02); padding: 6px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);">
                        <div style="color: #94A3B8; font-weight: 500; font-size: 0.65rem; text-transform: uppercase;">Pages</div>
                        <div style="color: #6366F1; font-weight: 700; font-size: 0.9rem; margin-top: 2px;">{page_count}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 6px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);">
                        <div style="color: #94A3B8; font-weight: 500; font-size: 0.65rem; text-transform: uppercase;">Chunks</div>
                        <div style="color: #a5b4fc; font-weight: 700; font-size: 0.9rem; margin-top: 2px;">{chunk_count}</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 6px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03);">
                        <div style="color: #94A3B8; font-weight: 500; font-size: 0.65rem; text-transform: uppercase;">Size</div>
                        <div style="color: #ffb786; font-weight: 700; font-size: 0.85rem; margin-top: 2px;">{format_file_size(char_count)}</div>
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
    
    # Action button underneath card
    st.markdown('<span class="danger-btn-marker"></span>', unsafe_allow_html=True)
    if st.button("Delete Document", key=f"del_{card_index}", help=f"Delete {filename} from knowledge base", use_container_width=True):
        on_delete_callback(filename)
