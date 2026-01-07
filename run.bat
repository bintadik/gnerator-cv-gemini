@echo off
REM Quick start script for CV/Cover Letter Generator

echo ========================================
echo CV/Cover Letter Generator
echo ========================================
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env file from .env.example and add your Gemini API key.
    echo.
    pause
    exit /b 1
)

echo Starting Streamlit application...
echo.
echo The app will open in your browser at http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

uv run streamlit run app.py
