# Deployment Guide - Streamlit Cloud

## Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Streamlit Cloud Account** - Sign up at https://streamlit.io
3. **API Keys** - Have your API keys ready (Gemini and/or OpenRouter)

## Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
# Make sure .env is NOT committed (already in .gitignore)
git status

# Push your code to GitHub
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

**⚠️ IMPORTANT: Rotate your API keys if they were exposed!**

### 2. Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Select your GitHub repository
4. Select **branch**: `main` (or your branch)
5. Set **main file path**: `app.py`
6. Click **Deploy**

### 3. Add Secrets to Streamlit Cloud

After deployment:

1. Go to your app's **Settings** (gear icon)
2. Click **Secrets**
3. Add your API keys in the format:

```toml
gemini_api_key = "your_gemini_api_key_here"
openrouter_api_key = "your_openrouter_api_key_here"
```

4. Click **Save**

The app will automatically restart with your secrets.

## Environment Files

### .env (Local Development)
Used locally when running `streamlit run app.py`
```
GEMINI_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

### Streamlit Cloud Secrets
Used when deployed to Streamlit Cloud (Settings → Secrets)
Same format as .env but configured in the cloud UI

## Troubleshooting

### "Error installing requirements"

**Solution:**
1. Check the **terminal logs** in Streamlit Cloud (Settings → Manage account → Logs)
2. This has been fixed by:
   - Using `requires-python = ">=3.9"` (supports more environments)
   - Removed Windows-specific packages from `pyproject.toml`
   - Using flexible version constraints in `requirements.txt`

**If error persists:**
1. Delete the app and redeploy
2. Check that `requirements.txt` only has these valid packages:
   ```
   streamlit>=1.31.0
   google-generativeai>=0.3.0
   python-dotenv>=1.0.0
   pypdf2>=3.0.0
   python-docx>=1.1.0
   openai>=1.0.0
   ```
3. Use the **Diagnostics** page (see below)

### "Module not found" Error
- Check `requirements.txt` has all dependencies
- Wait 2-3 minutes for Streamlit Cloud to install packages
- Click "Rerun" button in the app
- Visit `/pages/99_diagnostics` to check what's installed

### "API Key not found" Error
- Verify secrets are added in Streamlit Cloud Settings
- **Use lowercase key names:** `gemini_api_key`, not `GEMINI_API_KEY`
- Wait for app to restart after adding secrets

### LaTeX Compilation Error
- The `packages.txt` file automatically installs LaTeX on Streamlit Cloud
- If error persists:
  1. Wait 2-3 minutes for system packages to install
  2. Visit `/pages/99_diagnostics` to check LaTeX status

### OpenRouter Not Working
- Verify `openrouter_api_key` is set in Streamlit Cloud Secrets
- Check API key is valid at https://openrouter.ai/keys

## Built-in Diagnostics

Visit your app at `/pages/99_diagnostics` to check:
- ✓ Python version
- ✓ All installed packages
- ✓ API configuration status
- ✓ LaTeX installation status
- ✓ Module imports

## Files for Cloud Deployment

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `packages.txt` | System packages (includes LaTeX) |
| `.streamlit/config.toml` | Streamlit configuration |
| `app.py` | Main application |
| `utils/` | Utility modules |
| `.gitignore` | Excludes `.env` from git |

## Features

✅ Google Gemini (Free tier)
✅ OpenRouter (Free tier)
✅ Model selection
✅ LaTeX CV generation
✅ PDF compilation
✅ Cover letter generation

## API Key Links

- **Google Gemini**: https://aistudio.google.com/app/apikey
- **OpenRouter**: https://openrouter.ai/keys

## Notes

- The app uses the latest compatible versions of all libraries
- Streamlit Cloud automatically handles Python 3.9+
- System packages (LaTeX) are installed from `packages.txt`
- Secrets are securely managed by Streamlit Cloud
