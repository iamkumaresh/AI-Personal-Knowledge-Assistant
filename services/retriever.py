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
