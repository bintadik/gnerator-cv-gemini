# CV/Cover Letter Generator

An AI-powered web application that generates tailored CVs/resumes and cover letters using Google's Gemini API. Upload your existing CV, input job details, and get professionally formatted LaTeX documents and PDFs.

## Features

- 📄 **CV Upload**: Support for PDF, DOCX, and TXT formats
- 🤖 **AI-Powered Generation**: Uses Gemini API to tailor content to specific job postings
- 📝 **LaTeX Output**: Generates editable LaTeX code for full customization
- 📑 **PDF Compilation**: Compile LaTeX to PDF directly in the app
- ✉️ **Cover Letter Generation**: Create compelling cover letters with copyable text
- 🎨 **Custom Templates**: Upload your own LaTeX templates

## Prerequisites

1. **Python 3.10+**
2. **UV Package Manager**: Install from [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
3. **LaTeX Distribution** (for local PDF compilation):
   - **Windows**: [MiKTeX](https://miktex.org/download)
   - **macOS**: [MacTeX](https://www.tug.org/mactex/)
   - **Linux**: TeX Live (`sudo apt-get install texlive-full`)
4. **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Local Installation

1. **Clone or download this repository**

2. **Install dependencies using UV**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```

4. **Verify LaTeX installation** (optional, for PDF compilation):
   ```bash
   pdflatex --version
   ```

## Usage

1. **Start the application**:
   ```bash
   uv run streamlit run app.py
   ```
   Or double-click `run.bat` on Windows

2. **Open your browser** to the URL shown (typically `http://localhost:8501`)

3. **Generate a CV**:
   - Upload your existing CV/resume
   - Enter the job description
   - Enter the company name
   - Click "Generate CV"
   - Edit the LaTeX code if needed
   - Compile to PDF and download

4. **Generate a Cover Letter**:
   - Switch to the "Cover Letter" tab
   - Upload your CV (if not already done)
   - Enter job details
   - Click "Generate Cover Letter"
   - Copy the generated text

## Deployment to Streamlit Cloud

### Quick Deploy Steps

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/cv-coverletter-generator.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository and `app.py`
   - In **Advanced settings → Secrets**, add:
     ```toml
     GEMINI_API_KEY = "your_api_key_here"
     ```
   - Click "Deploy!"

3. **Access your app** at: `https://YOUR_USERNAME-cv-coverletter-generator.streamlit.app`

### Deployment Files

All required files are included:
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - LaTeX system packages
- ✅ `.streamlit/config.toml` - App configuration

**Note**: PDF compilation may have limitations on Streamlit Cloud due to resource constraints. Users can download the `.tex` file and compile locally or use [Overleaf](https://www.overleaf.com/).

## Project Structure

```
cv-coverletter-generator/
├── app.py                          # Main Streamlit application
├── utils/
│   ├── cv_parser.py               # CV/resume parsing utilities
│   ├── latex_handler.py           # LaTeX compilation and handling
│   └── gemini_client.py           # Gemini API integration
├── templates/
│   ├── cv_template.tex            # Default CV LaTeX template
│   └── cover_letter_template.txt  # Cover letter generation guide
├── requirements.txt               # Python dependencies (for Streamlit Cloud)
├── packages.txt                   # System packages (for Streamlit Cloud)
├── pyproject.toml                 # UV project configuration
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## Configuration

### Gemini API Settings

The application uses the Gemini 2.5 Flash model. You can modify the model in `utils/gemini_client.py`.

### LaTeX Templates

Custom templates should include placeholders that the AI can fill. The default template is located in `templates/cv_template.tex`.

## Troubleshooting

### LaTeX Compilation Errors

- Ensure `pdflatex` is in your system PATH
- Check that all required LaTeX packages are installed
- Review the error output in the Streamlit interface
- On Streamlit Cloud: Download `.tex` and compile locally

### API Errors

- Verify your Gemini API key is correct
- Check your API quota and rate limits
- Ensure you have internet connectivity
- On Streamlit Cloud: Check secrets are configured correctly

### File Upload Issues

- Supported formats: PDF, DOCX, TXT
- Maximum file size: 200MB (Streamlit default)
- Ensure files are not corrupted

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
