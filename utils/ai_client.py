"""
AI Client for generating CV content and cover letters.
Supports multiple providers: Google Gemini and OpenRouter.
"""

import os
from typing import Optional

# Import handling for cloud deployment
try:
    import streamlit as st

    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


class AIClient:
    """Client for interacting with various AI providers."""

    # Available providers
    PROVIDERS = {"google": "Google Gemini", "openrouter": "OpenRouter"}

    # Free models for each provider
    FREE_MODELS = {
        "google": [
            "gemini-1.5-flash",
            "gemini-2.5-flash",
        ],
        "openrouter": [
            "meta-llama/llama-3.2-3b-instruct:free",
            "google/gemma-4-26b-a4b-it:free",
            "minimax/minimax-m2.5:free",
        ],
    }

    def __init__(
        self, provider: str = "google", model: str = None, api_key: Optional[str] = None
    ):
        """
        Initialize AI client.

        Args:
            provider: AI provider ('google' or 'openrouter')
            model: Model name to use
            api_key: API key. If None, reads from environment.
        """
        self.provider = provider.lower()
        if self.provider not in self.PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider}. Supported: {list(self.PROVIDERS.keys())}"
            )

        # Set default model if not provided
        if model is None:
            model = self.FREE_MODELS[self.provider][0]
        self.model = model

        # Set API key with Streamlit Cloud secrets support
        if self.provider == "google":
            # Try Streamlit secrets first (for Cloud deployment)
            if HAS_STREAMLIT:
                try:
                    self.api_key = (
                        api_key
                        or st.secrets.get("gemini_api_key")
                        or os.getenv("GEMINI_API_KEY")
                    )
                except Exception:
                    self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            else:
                self.api_key = api_key or os.getenv("GEMINI_API_KEY")

            if not self.api_key:
                raise ValueError(
                    "Gemini API key not found. Set GEMINI_API_KEY environment variable or Streamlit secrets."
                )
            if genai is None:
                raise ImportError("google-generativeai package not installed")
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        elif self.provider == "openrouter":
            # Try Streamlit secrets first (for Cloud deployment)
            if HAS_STREAMLIT:
                try:
                    self.api_key = (
                        api_key
                        or st.secrets.get("openrouter_api_key")
                        or os.getenv("OPENROUTER_API_KEY")
                    )
                except Exception:
                    self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            else:
                self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")

            if not self.api_key:
                raise ValueError(
                    "OpenRouter API key not found. Set OPENROUTER_API_KEY environment variable or Streamlit secrets."
                )
            if OpenAI is None:
                raise ImportError("openai package not installed")
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )

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
        language: str = "English",
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
            template_instruction = (
                f"\n\nUse this LaTeX template structure:\n{latex_template}"
            )
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

        if self.provider == "google":
            response = self.client.generate_content(prompt)
            return self._clean_output(response.text)
        elif self.provider == "openrouter":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return self._clean_output(response.choices[0].message.content)

    def generate_cover_letter(
        self,
        original_cv: str,
        job_description: str,
        company_name: str,
        language: str = "English",
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

        if self.provider == "google":
            response = self.client.generate_content(prompt)
            return self._clean_output(response.text)
        elif self.provider == "openrouter":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return self._clean_output(response.choices[0].message.content)


# Backward compatibility
class GeminiClient(AIClient):
    """Backward compatibility class for existing code."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(provider="google", api_key=api_key)
