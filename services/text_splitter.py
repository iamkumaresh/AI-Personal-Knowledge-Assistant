from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class TextSplitterService:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_pages(self, pages_data: List[Dict[str, Any]]) -> List[Document]:
        """
        Takes raw page objects and returns a list of LangChain Document objects
        with appropriate text splitting and metadata tracking (filename, page_num).
        """
        documents = []
        for page in pages_data:
            text = page["text"]
            metadata = {
                "filename": page["filename"],
                "page_num": page["page_num"]
            }
            
            # Split the text of a single page
            chunks = self.splitter.split_text(text)
            
            for chunk in chunks:
                documents.append(Document(
                    page_content=chunk,
                    metadata=metadata.copy()
                ))
                
        return documents
