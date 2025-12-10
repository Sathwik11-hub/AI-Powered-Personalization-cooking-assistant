# 🚀 Deploying AI-Powered Cooking Assistant to Vercel

This guide walks you through deploying your Streamlit-based AI Cooking Assistant to Vercel using VS Code and GitHub Copilot.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Configuration Files](#configuration-files)
4. [VS Code Tasks Workflow](#vs-code-tasks-workflow)
5. [Deployment Steps](#deployment-steps)
6. [Troubleshooting](#troubleshooting)
7. [Environment Variables](#environment-variables)

---

## ✅ Prerequisites

### Install Required Tools

1. **VS Code** with extensions:
   - Git (built-in)
   - GitHub Copilot (recommended)
   - Python extension
   - (Optional) Vercel extension

2. **Python 3.9+** installed on your machine

3. **Node.js & npm** (required for Vercel CLI)

4. **Vercel CLI** - Install globally:
   ```bash
   npm install -g vercel
   ```

5. **Git repository** with remote (GitHub, GitLab, etc.)

### Verify Installations

Run these commands to verify:

```bash
python --version      # Should be 3.9+
node --version        # Should be 18+
npm --version
vercel --version
git --version
```

---

## 📁 Project Structure

Your project now includes the following Vercel deployment files:

```
AI-Powered-Personalization-cooking-assistant/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel configuration
├── package.json                # Node.js package file (for Vercel)
├── api/
│   └── index.py               # Vercel serverless function wrapper
├── scripts/
│   └── verify-build-output.py # Build verification script
├── .vscode/
│   └── tasks.json             # VS Code tasks for automation
├── src/                       # Source code modules
├── data/                      # Data files
└── static/                    # Static assets (CSS, JS)
```

---

## ⚙️ Configuration Files

### 1. `vercel.json`

Configures Vercel to run your Python/Streamlit app:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "PYTHONUNBUFFERED": "1",
    "STREAMLIT_SERVER_PORT": "8501",
    "STREAMLIT_SERVER_HEADLESS": "true"
  }
}
```

### 2. `api/index.py`

Vercel serverless function handler that runs Streamlit:

```python
from http.server import BaseHTTPRequestHandler
from streamlit.web import cli as stcli
import sys

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        sys.argv = ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
        sys.exit(stcli.main())
```

### 3. `package.json`

Minimal Node.js configuration for Vercel compatibility:

- Defines npm scripts for development and deployment
- Ensures Vercel recognizes the project

---

## 🎯 VS Code Tasks Workflow

Press `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux) → **Tasks: Run Task** and select:

### Available Tasks

1. **Install Python Dependencies**
   - Runs: `pip install -r requirements.txt`
   - Use this first to set up your environment

2. **Run Streamlit Dev Server**
   - Runs: `streamlit run app.py`
   - Test your app locally before deploying

3. **Build (Verify Python Syntax)**
   - Runs: `python -m py_compile app.py src/*.py data/*.py`
   - Checks all Python files for syntax errors

4. **Verify Build Output**
   - Runs: `python scripts/verify-build-output.py`
   - Comprehensive check of all required files and dependencies

5. **Deploy to Vercel (Production)**
   - Runs: `vercel --prod --confirm`
   - Deploys to production environment

6. **Deploy to Vercel (Preview)**
   - Runs: `vercel`
   - Creates a preview deployment for testing

7. **Full Build & Deploy Pipeline**
   - Runs all verification steps + deployment in sequence
   - One-click deployment workflow

8. **Login to Vercel**
   - Runs: `vercel login`
   - Authenticate with Vercel CLI

---

## 🚀 Deployment Steps

### Step 1: Initial Setup

1. **Clone and open your project in VS Code**
   ```bash
   cd AI-Powered-Personalization-cooking-assistant
   code .
   ```

2. **Install Python dependencies locally**
   - Run Task: **Install Python Dependencies**
   - Or manually: `pip install -r requirements.txt`

3. **Test locally**
   - Run Task: **Run Streamlit Dev Server**
   - Visit `http://localhost:8501` to verify your app works

### Step 2: Verify Build

1. **Run syntax check**
   - Run Task: **Build (Verify Python Syntax)**
   - Ensures all Python files compile without errors

2. **Run comprehensive verification**
   - Run Task: **Verify Build Output**
   - This checks:
     - ✅ All required files exist
     - ✅ Python syntax is valid
     - ✅ Dependencies are listed
     - ✅ Directory structure is correct

### Step 3: Authenticate with Vercel

1. **Login to Vercel**
   - Run Task: **Login to Vercel**
   - Or manually: `vercel login`
   - Follow the browser authentication flow

### Step 4: Deploy

#### Option A: Preview Deployment (Testing)

1. Run Task: **Deploy to Vercel (Preview)**
2. Vercel will:
   - Detect your project
   - Ask for project name (accept default or customize)
   - Create a preview URL
3. Test the preview URL before going to production

#### Option B: Production Deployment

1. Run Task: **Deploy to Vercel (Production)**
2. Or use the full pipeline: **Full Build & Deploy Pipeline**
3. Vercel will deploy to your production URL

#### Option C: GitHub Integration (Recommended)

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel Dashboard:**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel auto-detects Python and deploys
   - Every push to `main` triggers automatic deployment

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Skipping cache upload - no files prepared"

**Cause:** Vercel couldn't find build output or detect the framework.

**Solutions:**
1. Ensure `vercel.json` exists in root directory
2. Verify `app.py` is in the root directory
3. Check that `requirements.txt` has all dependencies
4. Run verification script: `python scripts/verify-build-output.py`

#### Issue 2: "Module not found" errors during deployment

**Cause:** Missing dependencies in `requirements.txt`.

**Solutions:**
1. Ensure all imports in your code are listed in `requirements.txt`
2. Pin versions for critical packages (e.g., `streamlit==1.28.1`)
3. Test locally first: `pip install -r requirements.txt`

#### Issue 3: Deployment timeout

**Cause:** Large dependencies (like PyTorch) take time to install.

**Solutions:**
1. Use lighter versions: `torch-cpu` instead of full `torch`
2. Consider alternative hosting for heavy ML apps (Streamlit Cloud, Hugging Face Spaces)
3. Use Vercel's build time limits (Pro plan has higher limits)

#### Issue 4: Streamlit app doesn't load

**Cause:** Streamlit serverless function configuration.

**Solutions:**
1. Check `api/index.py` is correctly configured
2. Verify environment variables in `vercel.json`
3. Look at Vercel deployment logs for specific errors

### Debug Commands

Run these in VS Code terminal:

```bash
# Check Python syntax locally
python -m py_compile app.py

# Run verification script
python scripts/verify-build-output.py

# Test Vercel configuration locally
vercel dev

# View deployment logs
vercel logs

# Get detailed debug output
vercel --debug --prod
```

---

## 🔐 Environment Variables

### Setting Environment Variables in Vercel

1. **Via Vercel Dashboard:**
   - Go to your project → Settings → Environment Variables
   - Add variables like `OPENAI_API_KEY`, `HF_TOKEN`, etc.

2. **Via Vercel CLI:**
   ```bash
   vercel env add OPENAI_API_KEY
   # Paste your key when prompted
   ```

3. **For local development:**
   Create a `.env` file (add to `.gitignore`):
   ```env
   OPENAI_API_KEY=your-key-here
   HF_TOKEN=your-token-here
   ```

### Required Environment Variables

Based on your `app.py`, you may need:

- `OPENAI_API_KEY` (if using OpenAI features)
- `HF_TOKEN` (for Hugging Face models)
- Any other API keys or secrets

**⚠️ IMPORTANT:** Never commit API keys to Git. Always use environment variables.

---

## 📝 GitHub Copilot Prompts

Use these prompts with Copilot to customize your deployment:

### Prompt 1: Optimize for Vercel
```javascript
// Copilot: Review vercel.json and suggest optimizations for a Streamlit app
// with heavy ML dependencies (transformers, torch). How can I reduce build time?
```

### Prompt 2: Add Health Check
```python
# Copilot: Create a /health endpoint in api/index.py that returns JSON status
# Include Python version, Streamlit version, and timestamp
```

### Prompt 3: Create GitHub Actions
```yaml
# Copilot: Generate a GitHub Actions workflow that:
# 1. Runs on push to main
# 2. Installs Python dependencies
# 3. Runs verify-build-output.py
# 4. Only deploys to Vercel if verification passes
```

### Prompt 4: Add Monitoring
```python
# Copilot: Add basic error logging and performance monitoring to app.py
# Log errors to a file and track page load times
```

---

## 🎉 Success Checklist

After deployment, verify:

- [ ] ✅ App loads at Vercel URL
- [ ] ✅ All pages and features work
- [ ] ✅ Images and static assets load correctly
- [ ] ✅ No console errors in browser DevTools
- [ ] ✅ ML models load (may be slow on first load)
- [ ] ✅ User interactions work (file upload, form submission, etc.)
- [ ] ✅ Mobile responsiveness (test on phone)

---

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [GitHub Actions + Vercel](https://vercel.com/guides/how-can-i-use-github-actions-with-vercel)

---

## 🆘 Need Help?

1. Check Vercel deployment logs: `vercel logs`
2. Run local verification: `python scripts/verify-build-output.py`
3. Test locally first: `streamlit run app.py`
4. Review Vercel documentation for Python/Streamlit
5. Consider alternative platforms (Streamlit Cloud, Hugging Face Spaces) for heavy ML apps

---

**Note:** Vercel has limitations for Streamlit apps due to serverless function constraints. For production ML applications with large models, consider platforms optimized for Streamlit:

- **Streamlit Cloud** (free tier available)
- **Hugging Face Spaces** (free for public projects)
- **AWS/GCP/Azure** with dedicated instances

This Vercel setup works best for:
- Demos and prototypes
- Lightweight Streamlit apps
- Apps with smaller ML models
- Preview deployments for testing

---

**Happy Deploying! 🚀**
