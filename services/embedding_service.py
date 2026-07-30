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
