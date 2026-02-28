"""
PDF Text Extraction Module
Extracts text from blood test PDFs using PyMuPDF with pdfplumber fallback.
"""

import io
from typing import Optional, Tuple


def extract_text_from_pdf(pdf_bytes: bytes) -> Tuple[Optional[str], str]:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Tuple of (extracted_text, method_used)
        - extracted_text: The extracted text or None if failed
        - method_used: 'pymupdf', 'pdfplumber', or 'failed'
    """
    # Try PyMuPDF first (primary method)
    text, success = _extract_with_pymupdf(pdf_bytes)
    if success and text.strip():
        return text, 'pymupdf'
    
    # Fallback to pdfplumber
    text, success = _extract_with_pdfplumber(pdf_bytes)
    if success and text.strip():
        return text, 'pdfplumber'
    
    return None, 'failed'


def _extract_with_pymupdf(pdf_bytes: bytes) -> Tuple[Optional[str], bool]:
    """Extract text using PyMuPDF (fitz)."""
    try:
        import fitz  # PyMuPDF
        
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text_parts = []
        
        for page in doc:
            text_parts.append(page.get_text())
        
        doc.close()
        
        full_text = "\n".join(text_parts)
        return full_text, True
        
    except Exception as e:
        print(f"PyMuPDF extraction failed: {e}")
        return None, False


def _extract_with_pdfplumber(pdf_bytes: bytes) -> Tuple[Optional[str], bool]:
    """Extract text using pdfplumber (fallback)."""
    try:
        import pdfplumber
        
        text_parts = []
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        full_text = "\n".join(text_parts)
        return full_text, True
        
    except Exception as e:
        print(f"pdfplumber extraction failed: {e}")
        return None, False


def validate_pdf(pdf_bytes: bytes) -> Tuple[bool, str]:
    """
    Validate that the uploaded file is a valid PDF.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check file size (max 10MB per PRD)
    max_size = 10 * 1024 * 1024  # 10MB
    if len(pdf_bytes) > max_size:
        return False, f"File too large. Maximum size is 10MB. Your file is {len(pdf_bytes) / (1024*1024):.1f}MB"
    
    # Check PDF magic bytes
    if not pdf_bytes.startswith(b'%PDF'):
        return False, "Invalid PDF file. Please upload a valid PDF."
    
    return True, ""
