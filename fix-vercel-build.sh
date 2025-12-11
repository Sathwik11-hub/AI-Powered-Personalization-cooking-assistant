#!/bin/bash

# ========================================================================
# OPTION 1: Deploy to Streamlit Cloud (RECOMMENDED)
# ========================================================================
# 
# Your requirements.txt already has all ML packages - PERFECT!
# Just deploy using Streamlit Cloud web UI:
#
# 1. Go to: https://streamlit.io/cloud
# 2. Sign in with GitHub  
# 3. Click "New app"
# 4. Fill in:
#    Repository: Sathwik11-hub/AI-Powered-Personalization-cooking-assistant
#    Branch: main
#    Main file: app.py
# 5. Click "Deploy"
#
# Done! All ML features will work perfectly.
# ========================================================================

echo "========================================================================="
echo "🎯 Your build is failing because Vercel CANNOT handle ML packages"
echo "========================================================================="
echo ""
echo "Your requirements.txt contains:"
echo "  - torch (1GB)"
echo "  - transformers (500MB)"  
echo "  - sentence-transformers (300MB)"
echo "  Total: >1.5GB"
echo ""
echo "Vercel limit: 250MB"
echo "Result: BUILD WILL ALWAYS FAIL on Vercel"
echo ""
echo "========================================================================="
echo "✅ SOLUTION: Deploy to Streamlit Cloud instead"
echo "========================================================================="
echo ""
echo "1. Go to: https://streamlit.io/cloud"
echo "2. Sign in with GitHub"
echo "3. New app → Your repo → main branch → app.py"
echo "4. Deploy!"
echo ""
echo "Time: 2 minutes"
echo "Cost: FREE"
echo "Result: ALL features working!"
echo ""
echo "========================================================================="
echo "⚠️  ALTERNATIVE: Make Vercel work (limited features)"
echo "========================================================================="
echo ""
read -p "Strip ML packages for Vercel deployment? (y/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Creating Vercel-compatible requirements.txt..."
    
    cat > requirements.txt << 'EOF'
# Vercel-compatible requirements (ML features DISABLED)
# Total size: ~50MB (within Vercel 250MB limit)

streamlit==1.28.1
pandas==2.1.3
numpy==1.24.3
pillow==10.1.0
requests==2.31.0
plotly==5.17.0
python-dotenv==1.0.0

# REMOVED FOR VERCEL (packages too large or require compilation):
# torch==2.1.1                  (1000MB + requires CUDA/compilation)
# transformers==4.35.2          (500MB + depends on torch)
# torchvision==0.16.1           (100MB + depends on torch)
# sentence-transformers==2.2.2  (300MB + depends on torch)
# scikit-learn==1.3.2           (100MB + may need compilation)
# gradio==3.50.2                (using streamlit only)
# matplotlib==3.8.2             (not essential)
# seaborn==0.13.0               (not essential)
# opencv-python-headless        (can be large)
# speechrecognition             (not needed for web)
# pyttsx3                       (not needed for web)
# datasets==2.14.6              (200MB, too large)
# huggingface_hub               (not needed without models)
# python-speech-features        (not needed)
# openai==1.3.7                 (can add back if only using API)
EOF

    echo "✅ Created minimal requirements.txt"
    echo ""
    echo "⚠️  WARNING: These features will NOT work on Vercel:"
    echo "  - AI image recognition"
    echo "  - ML-powered recommendations"
    echo "  - NLP semantic search"
    echo ""
    echo "Your app.py already handles missing ML gracefully."
    echo ""
    echo "Next steps:"
    echo "1. git add requirements.txt"
    echo "2. git commit -m 'Vercel-compatible requirements (ML disabled)'"
    echo "3. git push origin main"
    echo "4. Wait for Vercel build (will succeed this time)"
    echo ""
else
    echo ""
    echo "Cancelled. No changes made."
    echo ""
    echo "✅ RECOMMENDED: Deploy to Streamlit Cloud for full ML features!"
    echo "   → https://streamlit.io/cloud"
    echo ""
fi
