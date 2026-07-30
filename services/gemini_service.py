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
