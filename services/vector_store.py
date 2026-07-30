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
