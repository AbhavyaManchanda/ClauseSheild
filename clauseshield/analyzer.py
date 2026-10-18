"""
analyzer.py - PDF text extraction and Ollama LLM execution for ClauseShield.
Zero cloud network calls: 100% local PDF extraction and local model inference.
"""

import io
import re
from typing import Generator, Any
import pdfplumber
import ollama
from prompts import SYSTEM_PROMPT, build_analysis_prompt

DEFAULT_OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1"


def extract_text_from_pdf(pdf_file: Any) -> dict[str, Any]:
    """
    Extracts text cleanly from a PDF file using pdfplumber.
    
    Args:
        pdf_file: Either a file path (str), a BytesIO object, or a Streamlit UploadedFile.
        
    Returns:
        dict containing:
            - 'text': Extracted full text with page headers.
            - 'pages': Total number of pages processed.
            - 'word_count': Approximate total words.
            - 'char_count': Character count.
            - 'page_details': List of dicts with per-page text and word counts.
            
    Raises:
        ValueError: If PDF is empty or text cannot be extracted (e.g., image-only scan).
    """
    extracted_pages = []
    total_text_blocks = []

    # Open PDF from stream or file path
    try:
        if isinstance(pdf_file, (str, bytes)):
            pdf_ctx = pdfplumber.open(pdf_file)
        else:
            # Handles Streamlit UploadedFile or BytesIO
            pdf_ctx = pdfplumber.open(pdf_file)

        with pdf_ctx as pdf:
            total_pages = len(pdf.pages)
            if total_pages == 0:
                raise ValueError("The provided PDF contains 0 pages.")

            for idx, page in enumerate(pdf.pages, start=1):
                raw_page_text = page.extract_text() or ""
                # Normalize line breaks and multiple spaces
                clean_page_text = re.sub(r"[ \t]+", " ", raw_page_text).strip()
                
                extracted_pages.append({
                    "page_number": idx,
                    "text": clean_page_text,
                    "words": len(clean_page_text.split()) if clean_page_text else 0
                })

                if clean_page_text:
                    total_text_blocks.append(f"--- [Page {idx}] ---\n{clean_page_text}")

    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Failed to read PDF file: {str(e)}") from e

    full_text = "\n\n".join(total_text_blocks).strip()

    if not full_text or len(full_text.split()) < 20:
        raise ValueError(
            "Extracted text is empty or too short (< 20 words). "
            "This PDF might be an image-only scan or OCR-protected. "
            "Please upload a text-searchable PDF."
        )

    words = len(full_text.split())
    chars = len(full_text)

    return {
        "text": full_text,
        "pages": len(extracted_pages),
        "word_count": words,
        "char_count": chars,
        "page_details": extracted_pages
    }


def check_ollama_status(host: str = DEFAULT_OLLAMA_HOST) -> tuple[bool, list[str], str | None]:
    """
    Checks if Ollama service is reachable locally and lists available models.
    
    Args:
        host: Ollama server URL (defaults to http://localhost:11434).
        
    Returns:
        tuple (is_online, model_names, error_message)
    """
    try:
        client = ollama.Client(host=host)
        response = client.list()
        
        # ollama SDK returns ListResponse object with .models attribute
        model_names = []
        if hasattr(response, "models") and response.models:
            for m in response.models:
                # m could be Model object with 'model' attribute or dict
                if hasattr(m, "model"):
                    model_names.append(m.model)
                elif isinstance(m, dict) and "name" in m:
                    model_names.append(m["name"])
                elif isinstance(m, dict) and "model" in m:
                    model_names.append(m["model"])
                else:
                    model_names.append(str(m))
        elif isinstance(response, dict) and "models" in response:
            for m in response["models"]:
                if isinstance(m, dict):
                    model_names.append(m.get("name", m.get("model", "")))
                else:
                    model_names.append(str(m))
                    
        model_names = [m for m in model_names if m]
        return True, model_names, None
    except Exception as e:
        err_msg = str(e)
        return False, [], err_msg


def analyze_contract_text(
    contract_text: str,
    model: str = DEFAULT_MODEL,
    host: str = DEFAULT_OLLAMA_HOST,
    custom_focus: list[str] | None = None,
    stream: bool = True
) -> Generator[str, None, None] | str:
    """
    Executes local contract analysis via Ollama.
    
    Args:
        contract_text: Extracted plain text of the contract.
        model: Name of the local Ollama model (e.g. 'llama3.1', 'llama3.1:8b').
        host: Ollama server URL.
        custom_focus: Optional list of areas to scrutinize.
        stream: If True, yields streaming text chunks. If False, returns full string.
        
    Returns:
        Generator yielding text tokens if stream=True, or complete string if stream=False.
    """
    client = ollama.Client(host=host)
    user_prompt = build_analysis_prompt(contract_text, custom_focus=custom_focus)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]

    # Model inference options: temperature=0.1 for high fidelity legal reasoning
    options = {
        "temperature": 0.1,
        "top_p": 0.9,
    }

    if stream:
        def stream_generator() -> Generator[str, None, None]:
            response = client.chat(
                model=model,
                messages=messages,
                options=options,
                stream=True
            )
            for chunk in response:
                if "message" in chunk and "content" in chunk["message"]:
                    yield chunk["message"]["content"]
                elif hasattr(chunk, "message") and hasattr(chunk.message, "content"):
                    yield chunk.message.content

        return stream_generator()
    else:
        response = client.chat(
            model=model,
            messages=messages,
            options=options,
            stream=False
        )
        if "message" in response and "content" in response["message"]:
            return response["message"]["content"]
        elif hasattr(response, "message") and hasattr(response.message, "content"):
            return response.message.content
        return str(response)

