import io
from typing import List, Dict, Any
from pypdf import PdfReader

class PDFLoader:
    @staticmethod
    def load_pdf(file_src: Any, filename: str) -> Dict[str, Any]:
        """
        Extracts text from a PDF file (given as file path or file-like object).
        Returns a dictionary with text content, page contents, page count, and character count.
        """
        pages_data = []
        full_text = ""
        total_chars = 0
        
        try:
            # Check if file_src is bytes/UploadFile or a file path
            if isinstance(file_src, bytes):
                reader = PdfReader(io.BytesIO(file_src))
            elif hasattr(file_src, "read"):
                # Handle Streamlit uploaded file which has a read() method
                reader = PdfReader(file_src)
            else:
                # Assume it is a file path/string
                reader = PdfReader(str(file_src))
                
            page_count = len(reader.pages)
            
            for idx, page in enumerate(reader.pages):
                page_num = idx + 1
                text = page.extract_text() or ""
                # Strip leading/trailing whitespaces and normalize spacing
                text = " ".join(text.split())
                
                if text.strip():
                    pages_data.append({
                        "text": text,
                        "page_num": page_num,
                        "filename": filename
                    })
                    full_text += text + " "
                    total_chars += len(text)
                    
            return {
                "success": True,
                "pages": pages_data,
                "page_count": page_count,
                "char_count": total_chars,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "pages": [],
                "page_count": 0,
                "char_count": 0,
                "error": str(e)
            }
