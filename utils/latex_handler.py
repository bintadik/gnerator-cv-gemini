"""
LaTeX handler for reading templates and compiling to PDF.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple


def read_latex_template(template_path: str) -> Optional[str]:
    """
    Read LaTeX template file.
    
    Args:
        template_path: Path to LaTeX template file
        
    Returns:
        Template content as string, or None if file not found
    """
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return None


def compile_latex_to_pdf(latex_content: str) -> Tuple[bool, Optional[bytes], Optional[str]]:
    """
    Compile LaTeX content to PDF.
    
    Args:
        latex_content: LaTeX source code as string
        
    Returns:
        Tuple of (success: bool, pdf_bytes: Optional[bytes], error_message: Optional[str])
    """
    # Create temporary directory for compilation
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tex_file = temp_path / "document.tex"
        pdf_file = temp_path / "document.pdf"
        
        try:
            # Write LaTeX content to file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            # Run pdflatex (run twice for references)
            for _ in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(temp_path), str(tex_file)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            # Check if PDF was created
            if pdf_file.exists():
                with open(pdf_file, 'rb') as f:
                    pdf_bytes = f.read()
                return True, pdf_bytes, None
            else:
                # Extract error from log
                log_file = temp_path / "document.log"
                error_msg = "PDF compilation failed."
                if log_file.exists():
                    with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                        log_content = f.read()
                        # Try to find the error line
                        for line in log_content.split('\n'):
                            if line.startswith('!'):
                                error_msg = line
                                break
                return False, None, error_msg
                
        except subprocess.TimeoutExpired:
            return False, None, "LaTeX compilation timed out (30s limit)"
        except FileNotFoundError:
            return False, None, "pdflatex not found. Please install a LaTeX distribution (MiKTeX, TeX Live, or MacTeX)"
        except Exception as e:
            return False, None, f"Compilation error: {str(e)}"


def save_latex_file(latex_content: str, output_path: str) -> bool:
    """
    Save LaTeX content to file.
    
    Args:
        latex_content: LaTeX source code
        output_path: Path to save the .tex file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        return True
    except Exception as e:
        print(f"Error saving LaTeX file: {e}")
        return False
