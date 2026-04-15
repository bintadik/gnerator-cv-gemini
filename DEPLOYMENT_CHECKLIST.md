# Streamlit Cloud Deployment Checklist ✅

## Pre-Deployment (Local Testing)

- [ ] Rotate your API keys (old ones are exposed)
  - Google Gemini: https://aistudio.google.com/app/apikey
  - OpenRouter: https://openrouter.ai/keys
- [ ] Remove `.env` file from git history if accidentally committed
  - Run: `git rm --cached .env && git commit -m "Remove .env"`
- [ ] Test locally with `streamlit run app.py`
- [ ] Verify diagnostics page works: `http://localhost:8501/pages/99_diagnostics`
- [ ] Test both Google Gemini and OpenRouter (if available)

## Configuration Files Verified ✅

- [x] `requirements.txt` - Only 6 packages, flexible versioning
- [x] `packages.txt` - Lightweight LaTeX (xetex)
- [x] `pyproject.toml` - Python >=3.9, matches requirements.txt
- [x] `.streamlit/config.toml` - Optimized for cloud
- [x] `.gitignore` - Protects `.env`
- [x] `pages/99_diagnostics.py` - Debugging tool ready

## GitHub Preparation

- [ ] Push all changes to GitHub:
  ```bash
  git add .
  git commit -m "Prepare for Streamlit Cloud deployment"
  git push origin main
  ```
- [ ] Verify repository is public (for free tier)
- [ ] Check no `.env` in recent commits: `git log --oneline -- .env`

## Streamlit Cloud Deployment

1. [ ] Go to https://share.streamlit.io
2. [ ] Click "New app"
3. [ ] Select repository, branch: `main`, file: `app.py`
4. [ ] Click "Deploy"
5. [ ] **Wait 3-5 minutes** for installation
6. [ ] Check if deployment was successful

## Adding Secrets

1. [ ] Once app is deployed, click ⚙️ (Settings)
2. [ ] Click "Secrets"
3. [ ] Add your API keys:
   ```toml
   gemini_api_key = "AIzaSy..."
   openrouter_api_key = "sk-or-v1-..."
   ```
4. [ ] Click "Save"
5. [ ] App restarts automatically

## Verification Steps

1. [ ] App homepage loads (might take 30 seconds)
2. [ ] Visit `/pages/99_diagnostics` to verify:
   - [ ] Python 3.9+
   - [ ] All packages installed
   - [ ] API keys configured
   - [ ] pdflatex available
3. [ ] Test CV generation with sample data
4. [ ] Test PDF compilation
5. [ ] Test cover letter generation

## Troubleshooting

If deployment fails at "Error installing requirements":

1. [ ] Check **Settings → Logs** for error details
2. [ ] Verify `requirements.txt` has correct syntax
3. [ ] Delete app and redeploy
4. [ ] Check all package names are spelled correctly
5. [ ] Make sure no `==` version pins (use `>=` only)

If "API Key not found":

1. [ ] Check secrets use **lowercase** names: `gemini_api_key` (not `GEMINI_API_KEY`)
2. [ ] Wait 1-2 minutes after adding secrets
3. [ ] Refresh browser tab
4. [ ] Visit diagnostics page to confirm keys loaded

If "pdflatex not found":

1. [ ] Wait 2-3 minutes after deployment
2. [ ] Check `packages.txt` has LaTeX packages
3. [ ] Visit `/pages/99_diagnostics` to check status

## Final Checklist

- [ ] App is accessible at `https://your-username-cv-generator.streamlit.app`
- [ ] Can generate CV for sample data
- [ ] PDF compilation works
- [ ] Cover letter generation works
- [ ] Both Google and OpenRouter models work
- [ ] Diagnostics page shows all green ✓

## Security Reminders

⚠️ **DO THIS NOW:**
1. [ ] Regenerate Google Gemini API key
2. [ ] Regenerate OpenRouter API key
3. [ ] Never commit `.env` to git
4. [ ] Use Streamlit Cloud Secrets, not environment variables

## Support

If you encounter issues:

1. **Check Diagnostics**: `/pages/99_diagnostics`
2. **View Logs**: Settings → Manage account → Logs
3. **Restart App**: Settings → Reboot
4. **Community Help**: https://discuss.streamlit.io

## Files Changed for Cloud Deployment

- `requirements.txt` - Pinned to core dependencies only
- `packages.txt` - Lightweight LaTeX
- `pyproject.toml` - Python 3.9+, removed Windows packages
- `.streamlit/config.toml` - Cloud optimized
- `pages/99_diagnostics.py` - NEW: Debug tool
- `DEPLOYMENT.md` - Updated with full troubleshooting
- `utils/ai_client.py` - Streamlit secrets support added
