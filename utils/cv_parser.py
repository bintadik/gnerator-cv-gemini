"""
CV/Resume parser utility for extracting text from various file formats.
Supports PDF, DOCX, and TXT files.
"""

import io
from typing import Optional
import PyPDF2
from docx import Document


def parse_cv(uploaded_file) -> Optional[str]:
    """
    Parse uploaded CV/resume file and extract text content.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        Extracted text content as string, or None if parsing fails
    """
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return parse_pdf(uploaded_file)
        elif file_extension in ['docx', 'doc']:
            return parse_docx(uploaded_file)
        elif file_extension == 'txt':
            return parse_txt(uploaded_file)
        else:
            return None
            
    except Exception as e:
        # Re-raise to let the UI handle the error message
        raise Exception(f"Error parsing {file_extension} file: {str(e)}")


def parse_pdf(uploaded_file) -> str:
    """Extract text from PDF file."""
    uploaded_file.seek(0)
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    
    return text.strip()


def parse_docx(uploaded_file) -> str:
    """Extract text from DOCX file."""
    uploaded_file.seek(0)
    doc = Document(io.BytesIO(uploaded_file.read()))
    text = ""
    
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    return text.strip()


def parse_txt(uploaded_file) -> str:
    """Extract text from TXT file."""
    uploaded_file.seek(0)
    return uploaded_file.read().decode('utf-8').strip()
