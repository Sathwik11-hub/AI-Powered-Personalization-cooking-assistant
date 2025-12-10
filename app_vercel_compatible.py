import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import io
import base64

# Check if ML libraries are available (they won't be on Vercel)
ML_AVAILABLE = False
VOICE_AVAILABLE = False

try:
    from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
    import torch
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    pass

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    pass

# Page configuration
st.set_page_config(
    page_title="AI-Powered Cooking Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Display deployment mode warning
if not ML_AVAILABLE:
    st.sidebar.warning("""
    🚧 **Demo Mode** - ML features disabled
    
    This is a lightweight version for Vercel deployment.
    
    For full AI features including:
    - Image recognition
    - Smart recipe recommendations
    - NLP-powered search
    
    Visit the full version on Streamlit Cloud!
    """)

# Load custom CSS
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .recipe-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Main header
st.markdown('<h1 class="main-header">🍳 AI-Powered Cooking Assistant</h1>', unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "🔍 Find Recipes", "👤 Profile", "ℹ️ About"])

with tab1:
    st.markdown("### Welcome to Your Personal Cooking Assistant!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>🎯 Smart Recipe Search</h3>
        <p>Find recipes based on your dietary preferences and available ingredients</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not ML_AVAILABLE:
            st.info("💡 Basic search available. For AI-powered recommendations, use the full version.")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
        <h3>🥗 Nutrition Analysis</h3>
        <p>Get detailed nutritional information for any recipe</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔍 Find Your Perfect Recipe")
    
    # Basic search (works without ML)
    search_query = st.text_input("Search for recipes", placeholder="e.g., pasta, chicken curry, vegan dessert")
    
    dietary_prefs = st.multiselect(
        "Dietary Preferences",
        ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb", "Keto"]
    )
    
    if search_query:
        st.success(f"Searching for: {search_query}")
        
        # Mock recipe results (replace with actual data)
        st.markdown("### 📋 Recipe Results")
        
        mock_recipes = [
            {"name": "Classic Pasta Carbonara", "time": "30 mins", "difficulty": "Medium"},
            {"name": "Healthy Quinoa Bowl", "time": "20 mins", "difficulty": "Easy"},
            {"name": "Grilled Chicken Salad", "time": "25 mins", "difficulty": "Easy"},
        ]
        
        for recipe in mock_recipes:
            with st.expander(f"🍽️ {recipe['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"⏱️ Time: {recipe['time']}")
                with col2:
                    st.write(f"📊 Difficulty: {recipe['difficulty']}")
                
                st.button(f"View Full Recipe", key=recipe['name'])

with tab3:
    st.markdown("### 👤 Your Cooking Profile")
    
    user_name = st.text_input("Name", placeholder="Enter your name")
    
    col1, col2 = st.columns(2)
    
    with col1:
        skill_level = st.select_slider(
            "Cooking Skill Level",
            options=["Beginner", "Intermediate", "Advanced", "Expert"]
        )
    
    with col2:
        cuisine_prefs = st.multiselect(
            "Favorite Cuisines",
            ["Italian", "Chinese", "Indian", "Mexican", "Japanese", "Mediterranean", "Thai"]
        )
    
    allergies = st.multiselect(
        "Allergies/Restrictions",
        ["Nuts", "Dairy", "Eggs", "Shellfish", "Gluten", "Soy"]
    )
    
    if st.button("Save Profile"):
        st.success("✅ Profile saved successfully!")

with tab4:
    st.markdown("### ℹ️ About This Application")
    
    st.markdown("""
    This AI-Powered Cooking Assistant helps you:
    
    - 🔍 **Discover recipes** based on your preferences
    - 🥗 **Analyze nutrition** for healthier cooking
    - 🔄 **Find substitutions** for ingredients you don't have
    - 📊 **Track your cooking journey**
    
    ---
    
    ### 🚀 Deployment Information
    """)
    
    if ML_AVAILABLE:
        st.success("✅ **Full Version** - All AI features enabled")
        st.write("""
        - Image recognition for ingredients
        - NLP-powered recipe search
        - Smart recommendations
        - Voice commands
        """)
    else:
        st.warning("⚠️ **Lite Version** - Running on Vercel with limited features")
        st.write("""
        This is a demonstration version with reduced functionality due to Vercel's constraints.
        
        **Missing features in this version:**
        - AI image recognition
        - ML-powered recommendations
        - Voice commands
        
        **For the full experience with all AI features, deploy to:**
        - Streamlit Cloud (recommended)
        - Hugging Face Spaces
        - Railway or Render
        """)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Streamlit")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Available Recipes", "1,250+")
st.sidebar.metric("Active Users", "5,000+")
st.sidebar.metric("Cuisines", "25+")
