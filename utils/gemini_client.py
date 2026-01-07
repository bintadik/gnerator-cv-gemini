"""
Gemini API client for generating CV content and cover letters.
"""

import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key. If None, reads from environment.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def _clean_output(self, text: str) -> str:
        """
        Remove markdown code blocks (triple backticks) from the AI output.
        
        Args:
            text: Raw AI output
            
        Returns:
            Cleaned text
        """
        text = text.strip()
        # Remove opening triple backticks (with or without language identifier)
        if text.startswith("```"):
            # Find the end of the first line
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline:].strip()
            else:
                text = text.replace("```", "").strip()
        
        # Remove closing triple backticks
        if text.endswith("```"):
            text = text[:-3].strip()
            
        return text

    def generate_cv_latex(
        self, 
        original_cv: str, 
        job_description: str, 
        company_name: str,
        latex_template: Optional[str] = None,
        enhancement_mode: str = "balanced",
        language: str = "English"
    ) -> str:
        """
        Generate tailored CV content in LaTeX format.
        
        Args:
            original_cv: Original CV text content
            job_description: Target job description
            company_name: Target company name
            latex_template: Optional LaTeX template to use
            enhancement_mode: How aggressively to tailor (conservative/balanced/aggressive)
            language: Output language (English/Bahasa Indonesia)
            
        Returns:
            Generated LaTeX code as string
        """
        if latex_template:
            template_instruction = f"\n\nUse this LaTeX template structure:\n{latex_template}"
        else:
            template_instruction = ""
        
        # Customize instructions based on enhancement mode
        if "conservative" in enhancement_mode.lower():
            mode_instructions = """
ENHANCEMENT MODE: CONSERVATIVE (Styling Only)
- Keep ALL content from the original CV exactly as written
- ONLY improve the LaTeX formatting, layout, and visual styling
- Do NOT add, remove, or modify any text content
- Do NOT add new skills, experiences, or achievements
- Focus on making the existing content look more professional and well-organized
- Use better typography, spacing, and visual hierarchy
"""
        elif "aggressive" in enhancement_mode.lower():
            mode_instructions = """
ENHANCEMENT MODE: AGGRESSIVE (Maximum Impact)
- Optimize every aspect of the CV for maximum impact
- Use powerful action verbs and compelling language
- Quantify achievements wherever possible (add realistic metrics if implied)
- Highlight transferable skills that match the job requirements
- Expand bullet points to showcase impact and results
- Add relevant keywords from the job description naturally
- Present experiences in the most impressive way while staying truthful
- Make the candidate appear as the perfect fit for this role
"""
        else:  # balanced
            mode_instructions = """
ENHANCEMENT MODE: BALANCED (Add Relevant Details)
- Enhance the CV by adding relevant keywords from the job description
- Expand on existing experiences to highlight relevant skills
- Add context and details that are implied but not explicitly stated
- Emphasize transferable skills and relevant achievements
- Keep all content honest and based on the original CV
- Improve clarity and impact of existing bullet points
- Do NOT fabricate experiences or skills not present in the original
"""
        
        prompt = f"""You are an expert CV/resume writer and LaTeX specialist. 

Given the following information:

ORIGINAL CV:
{original_cv}

JOB DESCRIPTION:
{job_description}

COMPANY NAME:
{company_name}

OUTPUT LANGUAGE:
{language}

{mode_instructions}

Your task:
1. Analyze the job description and identify key requirements, skills, and qualifications
2. Tailor the original CV according to the enhancement mode specified above
3. Generate a complete, professional LaTeX document for the CV in the specified OUTPUT LANGUAGE ({language})
4. Use a modern, clean CV template (like moderncv or a custom professional design)
5. Emphasize achievements and experiences most relevant to the job
6. Ensure the LaTeX code is complete and compilable{template_instruction}

CRITICAL: To avoid font errors, ALWAYS include these two lines in the preamble:
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}

CRITICAL: Output ONLY the raw text. Do NOT wrap the output in markdown code blocks (no triple backticks).
Start directly with \\documentclass and end with \\end{{document}}.
"""
        
        response = self.model.generate_content(prompt)
        return self._clean_output(response.text)
    
    def generate_cover_letter(
        self,
        original_cv: str,
        job_description: str,
        company_name: str,
        language: str = "English"
    ) -> str:
        """
        Generate a tailored cover letter.
        
        Args:
            original_cv: Original CV text content
            job_description: Target job description
            company_name: Target company name
            language: Output language (English/Bahasa Indonesia)
            
        Returns:
            Generated cover letter text
        """
        prompt = f"""You are an expert cover letter writer.

Given the following information:

ORIGINAL CV:
{original_cv}

JOB DESCRIPTION:
{job_description}

COMPANY NAME:
{company_name}

OUTPUT LANGUAGE:
{language}

Your task:
1. Write a compelling, professional cover letter for this job application in the specified OUTPUT LANGUAGE ({language})
2. Highlight the most relevant qualifications and experiences from the CV
3. Show enthusiasm for the role and company
4. Demonstrate understanding of the company's needs based on the job description
5. Keep it concise (3-4 paragraphs)
6. Use a professional but engaging tone
7. Include appropriate placeholders for [Your Name], [Your Address], [Date], etc.

CRITICAL: Output ONLY the raw text. Do NOT wrap the output in markdown code blocks (no triple backticks).
Output the cover letter text in a standard business letter format.
"""
        
        response = self.model.generate_content(prompt)
        return self._clean_output(response.text)
