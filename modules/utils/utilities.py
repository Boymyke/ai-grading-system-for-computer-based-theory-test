import fitz  
from typing import Union
from pathlib import Path

def extract_text_from_pdf(pdf_input: Union[str, Path, bytes]) -> str:
    """
    Extract text from PDF. Accepts either:
    - File path as string or Path object
    - File-like object (from Streamlit uploader)
    - Bytes object
    
    Returns: Extracted text as string
    """
    try:
        if isinstance(pdf_input, (str, Path)):
            # Handle file path input
            doc = fitz.open(pdf_input)
        elif hasattr(pdf_input, 'read'):
            # Handle uploaded file object
            doc = fitz.open(stream=pdf_input.read(), filetype="pdf")
        elif isinstance(pdf_input, bytes):
            # Handle bytes input
            doc = fitz.open(stream=pdf_input, filetype="pdf")
        else:
            raise ValueError("Unsupported input type for PDF")
        
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
        
    except Exception as e:
        raise Exception(f"Error processing PDF: {str(e)}")


