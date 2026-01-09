"""
CV/Cover Letter Generator - Streamlit Application

An AI-powered application that generates tailored CVs/resumes and cover letters
using Google's Gemini API.
"""

import os
import streamlit as st
from pathlib import Path

# Import utility modules
from utils.cv_parser import parse_cv
from utils.gemini_client import GeminiClient
from utils.latex_handler import read_latex_template, compile_latex_to_pdf, save_latex_file
from utils.analytics import inject_ga4


# Page configuration
st.set_page_config(
    page_title="CV/Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'cv_text' not in st.session_state:
        st.session_state.cv_text = None
    if 'generated_latex' not in st.session_state:
        st.session_state.generated_latex = None
    if 'generated_cover_letter' not in st.session_state:
        st.session_state.generated_cover_letter = None
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = None


def setup_sidebar():
    """Setup sidebar with API key configuration."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=os.getenv('GEMINI_API_KEY', ''),
            help="Enter your Google Gemini API key."
        )
        
        st.markdown("[🔗 Get your free Gemini API Key here](https://aistudio.google.com/app/apikey)")
        
        if api_key:
            try:
                # Re-initialize to ensure we have the latest class definition
                st.session_state.gemini_client = GeminiClient(api_key)
                st.success("✅ API Key configured")
            except Exception as e:
                st.error(f"❌ API Key error: {str(e)}")
        else:
            st.warning("⚠️ Please enter your Gemini API key")
        
        st.divider()
        
        # Template selection
        st.subheader("📝 LaTeX Template")
        
        # Get available templates from templates folder
        templates_dir = Path(__file__).parent / "templates"
        template_files = list(templates_dir.glob("*.tex"))
        template_names = ["Default (moderncv)"] + [f.stem for f in template_files]
        
        selected_template = st.selectbox(
            "Choose a template",
            options=template_names,
            help="Select a LaTeX template for CV generation"
        )
        
        # Option to upload custom template
        upload_custom = st.checkbox("Upload custom template", value=False)
        
        if upload_custom:
            template_file = st.file_uploader(
                "Upload custom CV template (.tex)",
                type=['tex'],
                help="Upload your own LaTeX template"
            )
            
            if template_file:
                st.session_state.custom_template = template_file.read().decode('utf-8')
                st.session_state.selected_template_name = "Custom Upload"
                st.success("✅ Custom template loaded")
            else:
                st.session_state.custom_template = None
        else:
            # Load selected template from dropdown
            if selected_template == "Default (moderncv)":
                st.session_state.custom_template = None
                st.session_state.selected_template_name = "Default (moderncv)"
            else:
                # Load the selected template file
                template_path = templates_dir / f"{selected_template}.tex"
                if template_path.exists():
                    st.session_state.custom_template = read_latex_template(str(template_path))
                    st.session_state.selected_template_name = selected_template
                    st.success(f"✅ Template '{selected_template}' loaded")
                else:
                    st.session_state.custom_template = None
                    st.session_state.selected_template_name = "Default (moderncv)"
        
        st.divider()
        
        # Information
        st.subheader("ℹ️ About")
        st.info("""
        This app uses Google's Gemini AI to generate tailored CVs and cover letters.
        
        **Features:**
        - Upload your existing CV
        - Generate tailored LaTeX CV
        - Compile to PDF
        - Generate cover letters
        """)


def main_content():
    """Main content with combined CV and Cover Letter generation."""
    st.header("📄 Generate Tailored CV & Cover Letter")
    
    # Check if API key is configured
    if st.session_state.gemini_client is None:
        st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")
        return
    
    # Shared inputs section
    st.subheader("1. Upload Your CV & Enter Job Details")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose your CV/Resume file",
            type=['pdf', 'docx', 'txt'],
            help="Upload your current CV in PDF, DOCX, or TXT format",
            key="cv_uploader"
        )
        
        if uploaded_file:
            # Check if we already have this file parsed
            file_identifier = f"{uploaded_file.name}_{uploaded_file.size}"
            if st.session_state.get('last_parsed_file') != file_identifier:
                with st.spinner("Parsing CV..."):
                    try:
                        cv_text = parse_cv(uploaded_file)
                        if cv_text and len(cv_text.strip()) > 0:
                            st.session_state.cv_text = cv_text
                            st.session_state.last_parsed_file = file_identifier
                            st.success(f"✅ CV parsed successfully ({len(cv_text)} characters)")
                        else:
                            st.error("❌ Failed to extract text from CV. The file might be empty, encrypted, or contain only images.")
                            st.session_state.cv_text = None
                    except Exception as e:
                        st.error(f"❌ Error during CV parsing: {str(e)}")
                        st.session_state.cv_text = None
            
            if st.session_state.cv_text:
                with st.expander("View extracted text"):
                    st.text_area("CV Content", st.session_state.cv_text, height=150, disabled=True, key="cv_preview")
        else:
            # Clear state if file is removed
            st.session_state.cv_text = None
            st.session_state.last_parsed_file = None
    
    with col2:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Google, Microsoft, etc.",
            help="Enter the name of the company you're applying to"
        )
        
        job_title = st.text_input(
            "Job Title (Optional)",
            placeholder="e.g., Software Engineer, Data Scientist",
            help="Optional: Specific job title you're applying for"
        )
    
    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        height=150,
        help="Paste the full job description or key requirements"
    )
    
    # Enhancement mode and Language selector
    col_enh, col_lang = st.columns([2, 1])
    
    with col_enh:
        st.subheader("2. Enhancement Mode")
        enhancement_mode = st.radio(
            "Choose how to enhance your CV:",
            options=[
                "🎨 Conservative (Styling Only)",
                "⚖️ Balanced (Add Relevant Details)", 
                "🚀 Aggressive (Maximum Impact)"
            ],
            index=1,
            help="Select how aggressively to tailor your CV for this job",
            horizontal=True
        )
    
    with col_lang:
        st.subheader("3. Output Language")
        output_language = st.selectbox(
            "Select language:",
            options=["English", "Bahasa Indonesia"],
            index=0,
            help="Select the language for the generated content"
        )
    
    # Show description based on selected mode
    if "Conservative" in enhancement_mode:
        st.info("✨ **Conservative Mode**: Only improves formatting and styling. Keeps all content exactly as-is, just makes it look more professional.")
    elif "Balanced" in enhancement_mode:
        st.info("📝 **Balanced Mode**: Adds relevant keywords and expands on existing experiences honestly. Highlights transferable skills without exaggeration.")
    else:
        st.info("🔥 **Aggressive Mode**: Maximum optimization for the job. Uses powerful action verbs, quantifies achievements, and presents your experience in the most compelling way while staying truthful.")
    
    # Generation buttons
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_cv_btn = st.button("🚀 Generate Tailored CV", type="primary", use_container_width=True)
    
    with col2:
        generate_cl_btn = st.button("✉️ Generate Cover Letter", type="primary", use_container_width=True)
    
    # Generate CV
    if generate_cv_btn:
        if not st.session_state.cv_text:
            st.error("❌ Please upload your CV first.")
        elif not job_description:
            st.error("❌ Please enter the job description.")
        elif not company_name:
            st.error("❌ Please enter the company name.")
        else:
            # Clear previous results to force regeneration
            st.session_state.generated_latex = None
            if 'pdf_bytes' in st.session_state:
                st.session_state.pdf_bytes = None
            
            with st.spinner("🤖 Generating tailored CV with AI... This may take a moment."):
                try:
                    # Get custom template if uploaded
                    template = st.session_state.custom_template
                    if not template:
                        # Use default template
                        template_path = Path(__file__).parent / "templates" / "cv_template.tex"
                        template = read_latex_template(str(template_path))
                    
                    # Generate CV
                    latex_code = st.session_state.gemini_client.generate_cv_latex(
                        st.session_state.cv_text,
                        job_description,
                        company_name,
                        latex_template=template,
                        enhancement_mode=enhancement_mode,
                        language=output_language
                    )
                    
                    st.session_state.generated_latex = latex_code
                    st.success("✅ CV generated successfully!")
                    
                    # Show raw Gemini output
                    with st.expander("🔍 View Raw Gemini Output"):
                        st.code(latex_code, language="latex")
                    
                except Exception as e:
                    st.error(f"❌ Error generating CV: {str(e)}")
    
    # Generate Cover Letter
    if generate_cl_btn:
        if not st.session_state.cv_text:
            st.error("❌ Please upload your CV first.")
        elif not job_description:
            st.error("❌ Please enter the job description.")
        elif not company_name:
            st.error("❌ Please enter the company name.")
        else:
            # Clear previous results to force regeneration
            st.session_state.generated_cover_letter = None
            
            with st.spinner("🤖 Generating cover letter with AI... This may take a moment."):
                try:
                    # Add job title to description if provided
                    full_job_desc = job_description
                    if job_title:
                        full_job_desc = f"Job Title: {job_title}\n\n{job_description}"
                    
                    # Generate cover letter
                    cover_letter = st.session_state.gemini_client.generate_cover_letter(
                        st.session_state.cv_text,
                        full_job_desc,
                        company_name,
                        language=output_language
                    )
                    
                    st.session_state.generated_cover_letter = cover_letter
                    st.success("✅ Cover letter generated successfully!")
                    
                    # Show raw Gemini output
                    with st.expander("🔍 View Raw Gemini Output"):
                        st.text_area("Raw Output", cover_letter, height=200, disabled=True, key="raw_cl_output")
                    
                except Exception as e:
                    st.error(f"❌ Error generating cover letter: {str(e)}")
    
    # Display CV results
    if st.session_state.generated_latex:
        st.divider()
        st.subheader("2. Generated CV (LaTeX)")
        
        # Use hash of content as key to force update when content changes
        content_hash = hash(st.session_state.generated_latex)
        
        edited_latex = st.text_area(
            "Edit LaTeX code if needed",
            value=st.session_state.generated_latex,
            height=300,
            help="You can edit the LaTeX code before compiling to PDF",
            key=f"latex_editor_{content_hash}"
        )
        
        # Update session state if edited
        if edited_latex != st.session_state.generated_latex:
            st.session_state.generated_latex = edited_latex
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download .tex",
                data=st.session_state.generated_latex,
                file_name="cv.tex",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            if st.button("📄 Compile to PDF", use_container_width=True):
                with st.spinner("Compiling LaTeX to PDF..."):
                    success, pdf_bytes, error_msg = compile_latex_to_pdf(st.session_state.generated_latex)
                    
                    if success:
                        st.success("✅ PDF compiled successfully!")
                        st.session_state.pdf_bytes = pdf_bytes
                    else:
                        st.error(f"❌ Compilation failed: {error_msg}")
        
        with col3:
            if 'pdf_bytes' in st.session_state and st.session_state.pdf_bytes:
                st.download_button(
                    label="📥 Download PDF",
                    data=st.session_state.pdf_bytes,
                    file_name="cv.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    
    # Display Cover Letter results
    if st.session_state.generated_cover_letter:
        st.divider()
        st.subheader("3. Generated Cover Letter")
        
        # Use hash of content as key to force update when content changes
        cl_content_hash = hash(st.session_state.generated_cover_letter)
        
        edited_cover_letter = st.text_area(
            "Edit cover letter if needed",
            value=st.session_state.generated_cover_letter,
            height=300,
            help="You can edit the cover letter before copying or downloading",
            key=f"cover_letter_editor_{cl_content_hash}"
        )
        
        # Update session state if edited
        if edited_cover_letter != st.session_state.generated_cover_letter:
            st.session_state.generated_cover_letter = edited_cover_letter
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📋 Download as .txt",
                data=st.session_state.generated_cover_letter,
                file_name="cover_letter.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                label="📥 Download as .docx",
                data=st.session_state.generated_cover_letter,
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Note: This is plain text. Open in Word and format as needed."
            )
        
        st.info("💡 Tip: Select all text above and copy (Ctrl+C / Cmd+C) to paste into your application.")


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Inject GA4 tracking
    inject_ga4()
    
    # Header
    st.markdown('<div class="main-header">📄 CV/Cover Letter Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Resume and Cover Letter Tailoring with Gemini</div>', unsafe_allow_html=True)
    
    # Setup sidebar
    setup_sidebar()
    
    # Main content (single page)
    main_content()
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        Made with ❤️ using Streamlit and Google Gemini AI<br>
        <small>Ensure you have LaTeX installed (MiKTeX/TeX Live/MacTeX) for PDF compilation</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
