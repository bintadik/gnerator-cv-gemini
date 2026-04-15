"""
Streamlit Cloud Diagnostic Page
Shows system info and package versions for debugging deployment issues
"""

import streamlit as st
import sys
import platform
import pkg_resources

st.set_page_config(page_title="System Diagnostics", page_icon="🔧", layout="wide")

st.title("🔧 System Diagnostics")

st.info(
    "This page shows your system information and package versions. "
    "Share this info when reporting issues."
)

# Basic System Info
col1, col2 = st.columns(2)

with col1:
    st.subheader("System Information")
    st.write(f"**Python Version:** {platform.python_version()}")
    st.write(f"**Platform:** {platform.platform()}")
    st.write(f"**Python Executable:** {sys.executable}")

with col2:
    st.subheader("Streamlit Version")
    import streamlit

    st.write(f"**Streamlit:** {streamlit.__version__}")

# Package Versions
st.subheader("📦 Installed Packages")

packages = [
    "streamlit",
    "google-generativeai",
    "openai",
    "python-dotenv",
    "pypdf2",
    "python-docx",
]

package_info = []
missing_packages = []

for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        package_info.append({"Package": package, "Version": version, "Status": "✓"})
    except pkg_resources.DistributionNotFound:
        missing_packages.append(package)

import pandas as pd

if package_info:
    df = pd.DataFrame(package_info)
    st.dataframe(df, use_container_width=True)

if missing_packages:
    st.error(f"⚠️ Missing packages: {', '.join(missing_packages)}")
else:
    st.success("✓ All packages installed")

# API Configuration Check
st.subheader("🔐 API Configuration Status")

api_status = []

try:
    import os

    gemini_key = bool(os.getenv("GEMINI_API_KEY"))
    api_status.append(
        ("GEMINI_API_KEY", "✓ Configured" if gemini_key else "✗ Not found")
    )
except Exception as e:
    api_status.append(("GEMINI_API_KEY", f"✗ Error: {str(e)}"))

try:
    openrouter_key = bool(os.getenv("OPENROUTER_API_KEY"))
    api_status.append(
        ("OPENROUTER_API_KEY", "✓ Configured" if openrouter_key else "✗ Not found")
    )
except Exception as e:
    api_status.append(("OPENROUTER_API_KEY", f"✗ Error: {str(e)}"))

for key_name, status in api_status:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write(key_name)
    with col2:
        st.write(status)

# LaTeX Check
st.subheader("📄 LaTeX Installation")

import subprocess

try:
    result = subprocess.run(["pdflatex", "--version"], capture_output=True, timeout=5)
    if result.returncode == 0:
        st.success("✓ pdflatex is installed")
    else:
        st.warning("⚠️ pdflatex found but may not be working properly")
except FileNotFoundError:
    st.error("✗ pdflatex not found. LaTeX compilation will fail.")
except Exception as e:
    st.error(f"✗ Could not check LaTeX: {str(e)}")

# Import Test
st.subheader("🧪 Module Import Test")

import_tests = [
    ("streamlit", "import streamlit"),
    ("google.generativeai", "import google.generativeai"),
    ("openai", "from openai import OpenAI"),
    ("PyPDF2", "import pypdf2"),
    ("python-docx", "import docx"),
    ("python-dotenv", "from dotenv import load_dotenv"),
]

for package_name, import_stmt in import_tests:
    try:
        exec(import_stmt)
        st.write(f"✓ {package_name}")
    except Exception as e:
        st.error(f"✗ {package_name}: {str(e)}")
