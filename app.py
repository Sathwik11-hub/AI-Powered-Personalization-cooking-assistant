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

# Try to import ML libraries (they may not be available on Vercel)
ML_AVAILABLE = False
try:
    from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
    import torch
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError:
    # ML libraries not available - running in lite mode
    pass

# Try to import voice libraries
VOICE_AVAILABLE = False
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    # Voice libraries not available
    pass

# Page configuration
st.set_page_config(
    page_title="AI-Powered Cooking Assistant",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .nutrition-metric {
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'dietary_restrictions': [],
            'spice_level': 'medium',
            'cuisine_preferences': [],
            'cooking_time_pref': 'medium',
            'favorite_recipes': [],
            'health_conditions': []
        }
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'cooking_mode' not in st.session_state:
        st.session_state.cooking_mode = False

# Load models and data
@st.cache_resource
def load_models():
    """Load AI models for various features"""
    if not ML_AVAILABLE:
        return None
    
    try:
        # Image captioning model for ingredient recognition
        image_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        image_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        
        # Sentence transformer for recipe similarity
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        return {
            'image_processor': image_processor,
            'image_model': image_model,
            'sentence_model': sentence_model
        }
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None

@st.cache_data
def load_recipe_data():
    """Load custom recipe dataset"""
    # Custom recipe data with nutritional information
    recipes_data = {
        'recipes': [
            {
                'id': 1,
                'name': 'Mediterranean Quinoa Bowl',
                'cuisine': 'Mediterranean',
                'ingredients': ['quinoa', 'chickpeas', 'cucumber', 'tomatoes', 'olives', 'feta cheese', 'olive oil', 'lemon'],
                'instructions': [
                    'Cook quinoa according to package directions',
                    'Drain and rinse chickpeas',
                    'Chop cucumber and tomatoes',
                    'Combine all ingredients in a bowl',
                    'Drizzle with olive oil and lemon juice',
                    'Season with salt and pepper'
                ],
                'cooking_time': 25,
                'difficulty': 'Easy',
                'servings': 2,
                'nutrition': {
                    'calories': 420,
                    'protein': 18,
                    'carbs': 58,
                    'fat': 14,
                    'fiber': 12,
                    'sodium': 380
                },
                'dietary_tags': ['vegetarian', 'gluten-free', 'high-protein'],
                'health_conditions': ['diabetes-friendly', 'heart-healthy', 'weight-loss'],
                'image_description': 'colorful quinoa bowl with vegetables'
            },
            {
                'id': 2,
                'name': 'Grilled Chicken with Herbs',
                'cuisine': 'American',
                'ingredients': ['chicken breast', 'rosemary', 'thyme', 'garlic', 'olive oil', 'lemon', 'salt', 'pepper'],
                'instructions': [
                    'Marinate chicken with herbs and olive oil for 30 minutes',
                    'Preheat grill to medium-high heat',
                    'Grill chicken for 6-7 minutes per side',
                    'Check internal temperature reaches 165°F',
                    'Let rest for 5 minutes before serving',
                    'Garnish with fresh herbs'
                ],
                'cooking_time': 45,
                'difficulty': 'Medium',
                'servings': 4,
                'nutrition': {
                    'calories': 285,
                    'protein': 35,
                    'carbs': 2,
                    'fat': 14,
                    'fiber': 0,
                    'sodium': 220
                },
                'dietary_tags': ['high-protein', 'low-carb', 'keto-friendly'],
                'health_conditions': ['diabetes-friendly', 'weight-loss', 'low-sodium'],
                'image_description': 'grilled chicken breast with herbs'
            },
            {
                'id': 3,
                'name': 'Vegetable Stir Fry',
                'cuisine': 'Asian',
                'ingredients': ['broccoli', 'bell peppers', 'carrots', 'snap peas', 'ginger', 'garlic', 'soy sauce', 'sesame oil'],
                'instructions': [
                    'Heat oil in a large wok or pan',
                    'Add ginger and garlic, stir for 30 seconds',
                    'Add harder vegetables first (carrots, broccoli)',
                    'Stir-fry for 3-4 minutes',
                    'Add softer vegetables (peppers, snap peas)',
                    'Add soy sauce and sesame oil',
                    'Stir-fry for 2-3 more minutes until tender-crisp'
                ],
                'cooking_time': 15,
                'difficulty': 'Easy',
                'servings': 3,
                'nutrition': {
                    'calories': 120,
                    'protein': 5,
                    'carbs': 18,
                    'fat': 4,
                    'fiber': 6,
                    'sodium': 580
                },
                'dietary_tags': ['vegetarian', 'vegan', 'low-calorie'],
                'health_conditions': ['diabetes-friendly', 'heart-healthy', 'weight-loss'],
                'image_description': 'colorful vegetable stir fry in wok'
            },
            {
                'id': 4,
                'name': 'Lentil Curry',
                'cuisine': 'Indian',
                'ingredients': ['red lentils', 'onion', 'tomatoes', 'ginger', 'garlic', 'turmeric', 'cumin', 'coriander', 'coconut milk'],
                'instructions': [
                    'Rinse lentils and set aside',
                    'Heat oil and sauté onions until golden',
                    'Add ginger, garlic, and spices',
                    'Add tomatoes and cook until soft',
                    'Add lentils and water, bring to boil',
                    'Simmer for 20-25 minutes until lentils are soft',
                    'Stir in coconut milk and simmer 5 more minutes'
                ],
                'cooking_time': 40,
                'difficulty': 'Medium',
                'servings': 4,
                'nutrition': {
                    'calories': 245,
                    'protein': 12,
                    'carbs': 35,
                    'fat': 8,
                    'fiber': 14,
                    'sodium': 240
                },
                'dietary_tags': ['vegetarian', 'vegan', 'high-fiber', 'high-protein'],
                'health_conditions': ['diabetes-friendly', 'heart-healthy'],
                'image_description': 'creamy red lentil curry with spices'
            },
            {
                'id': 5,
                'name': 'Baked Salmon with Dill',
                'cuisine': 'Scandinavian',
                'ingredients': ['salmon fillet', 'dill', 'lemon', 'olive oil', 'garlic', 'salt', 'pepper'],
                'instructions': [
                    'Preheat oven to 400°F',
                    'Place salmon on parchment-lined baking sheet',
                    'Drizzle with olive oil and lemon juice',
                    'Season with salt, pepper, and minced garlic',
                    'Top with fresh dill',
                    'Bake for 12-15 minutes until fish flakes easily'
                ],
                'cooking_time': 20,
                'difficulty': 'Easy',
                'servings': 2,
                'nutrition': {
                    'calories': 367,
                    'protein': 39,
                    'carbs': 1,
                    'fat': 22,
                    'fiber': 0,
                    'sodium': 180
                },
                'dietary_tags': ['high-protein', 'low-carb', 'omega-3-rich', 'keto-friendly'],
                'health_conditions': ['heart-healthy', 'low-sodium'],
                'image_description': 'baked salmon fillet with dill and lemon'
            }
        ],
        'ingredient_substitutions': {
            'quinoa': ['brown rice', 'bulgur wheat', 'cauliflower rice'],
            'chicken breast': ['turkey breast', 'tofu', 'tempeh'],
            'feta cheese': ['goat cheese', 'cottage cheese', 'nutritional yeast'],
            'olive oil': ['avocado oil', 'coconut oil', 'vegetable broth'],
            'soy sauce': ['tamari', 'coconut aminos', 'balsamic vinegar'],
            'coconut milk': ['cashew cream', 'almond milk', 'yogurt'],
            'salmon': ['tuna', 'mackerel', 'chicken breast'],
            'lentils': ['chickpeas', 'black beans', 'quinoa']
        }
    }
    
    return pd.DataFrame(recipes_data['recipes']), recipes_data['ingredient_substitutions']

def main():
    load_css()
    init_session_state()
    
    # Display deployment mode warning if ML is not available
    if not ML_AVAILABLE:
        st.warning("""
        ⚠️ **Lite Mode Active** - This version is running without ML/AI features due to deployment constraints.
        
        **Available features:**
        - ✅ Recipe browsing and search
        - ✅ Nutrition information
        - ✅ User preferences
        - ✅ Cooking tips
        
        **Disabled features:**
        - ❌ AI image recognition
        - ❌ Smart recipe recommendations  
        - ❌ NLP-powered search
        
        💡 **For full AI features**, deploy to [Streamlit Cloud](https://streamlit.io/cloud) - it's free and takes 2 minutes!
        """)
    
    # Load data and models
    recipes_df, substitutions = load_recipe_data()
    models = load_models()
    
    # Header
    st.markdown('<h1 class="main-header">🍳 AI-Powered Cooking Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar for user preferences and navigation
    with st.sidebar:
        st.header("🎯 Personalization")
        
        # User preferences
        st.subheader("Dietary Preferences")
        dietary_restrictions = st.multiselect(
            "Select dietary restrictions:",
            ['vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'nut-free', 'low-carb', 'keto-friendly'],
            default=st.session_state.user_preferences['dietary_restrictions']
        )
        
        health_conditions = st.multiselect(
            "Health conditions to consider:",
            ['diabetes', 'heart-disease', 'weight-loss', 'low-sodium', 'high-fiber'],
            default=st.session_state.user_preferences['health_conditions']
        )
        
        spice_level = st.select_slider(
            "Spice Level Preference:",
            options=['mild', 'medium', 'spicy'],
            value=st.session_state.user_preferences['spice_level']
        )
        
        cooking_time = st.select_slider(
            "Preferred Cooking Time:",
            options=['quick (<20 min)', 'medium (20-45 min)', 'long (45+ min)'],
            value='medium (20-45 min)'
        )
        
        # Update session state
        st.session_state.user_preferences.update({
            'dietary_restrictions': dietary_restrictions,
            'health_conditions': health_conditions,
            'spice_level': spice_level,
            'cooking_time_pref': cooking_time
        })
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Recipe Finder", 
        "📸 Image to Recipe", 
        "🔄 Ingredient Substitution", 
        "📊 Nutrition Analysis", 
        "🗣️ Voice Assistant",
        "👨‍🍳 Cooking Mode"
    ])
    
    with tab1:
        recipe_finder_tab(recipes_df, models)
    
    with tab2:
        image_to_recipe_tab(recipes_df, models)
    
    with tab3:
        substitution_tab(substitutions)
    
    with tab4:
        nutrition_analysis_tab(recipes_df)
    
    with tab5:
        voice_assistant_tab()
    
    with tab6:
        cooking_mode_tab(recipes_df)

def recipe_finder_tab(recipes_df, models):
    st.header("🔍 Recipe Finder")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("Search for recipes:", placeholder="Enter ingredients, cuisine, or recipe name...")
        
        col1a, col1b = st.columns(2)
        with col1a:
            cuisine_filter = st.selectbox("Filter by Cuisine:", 
                                        ['All'] + list(recipes_df['cuisine'].unique()))
        with col1b:
            difficulty_filter = st.selectbox("Filter by Difficulty:", 
                                           ['All'] + list(recipes_df['difficulty'].unique()))
    
    with col2:
        st.subheader("Quick Filters")
        show_vegetarian = st.checkbox("Vegetarian only")
        show_quick = st.checkbox("Quick recipes (<30 min)")
        show_healthy = st.checkbox("Health-conscious")
    
    # Filter recipes based on user preferences and filters
    filtered_recipes = filter_recipes(recipes_df, search_query, cuisine_filter, 
                                    difficulty_filter, show_vegetarian, show_quick, show_healthy)
    
    # Display filtered recipes
    if len(filtered_recipes) > 0:
        st.subheader(f"Found {len(filtered_recipes)} recipes:")
        
        for _, recipe in filtered_recipes.iterrows():
            display_recipe_card(recipe)
    else:
        st.warning("No recipes found matching your criteria. Try adjusting your filters!")

def filter_recipes(recipes_df, query, cuisine, difficulty, vegetarian, quick, healthy):
    """Filter recipes based on various criteria"""
    filtered = recipes_df.copy()
    
    # Text search
    if query:
        query_lower = query.lower()
        filtered = filtered[
            filtered['name'].str.lower().str.contains(query_lower, na=False) |
            filtered['ingredients'].astype(str).str.lower().str.contains(query_lower, na=False) |
            filtered['cuisine'].str.lower().str.contains(query_lower, na=False)
        ]
    
    # Cuisine filter
    if cuisine != 'All':
        filtered = filtered[filtered['cuisine'] == cuisine]
    
    # Difficulty filter
    if difficulty != 'All':
        filtered = filtered[filtered['difficulty'] == difficulty]
    
    # Vegetarian filter
    if vegetarian:
        filtered = filtered[filtered['dietary_tags'].astype(str).str.contains('vegetarian')]
    
    # Quick recipes filter
    if quick:
        filtered = filtered[filtered['cooking_time'] < 30]
    
    # Healthy filter
    if healthy:
        filtered = filtered[filtered['nutrition'].apply(lambda x: x['calories'] < 400)]
    
    return filtered

def display_recipe_card(recipe):
    """Display a recipe card with all details"""
    with st.container():
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(recipe['name'])
            st.write(f"**Cuisine:** {recipe['cuisine']}")
            st.write(f"**Cooking Time:** {recipe['cooking_time']} minutes")
            st.write(f"**Difficulty:** {recipe['difficulty']}")
            st.write(f"**Servings:** {recipe['servings']}")
        
        with col2:
            st.write("**Nutrition (per serving):**")
            nutrition = recipe['nutrition']
            st.write(f"Calories: {nutrition['calories']}")
            st.write(f"Protein: {nutrition['protein']}g")
            st.write(f"Carbs: {nutrition['carbs']}g")
            st.write(f"Fat: {nutrition['fat']}g")
        
        with col3:
            st.write("**Dietary Tags:**")
            for tag in recipe['dietary_tags']:
                st.write(f"• {tag}")
        
        # Ingredients
        st.write("**Ingredients:**")
        ingredients_text = ", ".join(recipe['ingredients'])
        st.write(ingredients_text)
        
        # Instructions toggle
        if st.button(f"Show Instructions - {recipe['name']}", key=f"instructions_{recipe['id']}"):
            st.write("**Instructions:**")
            for i, instruction in enumerate(recipe['instructions'], 1):
                st.write(f"{i}. {instruction}")
        
        # Add to favorites
        if st.button(f"❤️ Add to Favorites", key=f"fav_{recipe['id']}"):
            if recipe['id'] not in st.session_state.user_preferences['favorite_recipes']:
                st.session_state.user_preferences['favorite_recipes'].append(recipe['id'])
                st.success("Added to favorites!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()

def image_to_recipe_tab(recipes_df, models):
    st.header("📸 Image to Recipe")
    st.write("Upload an image of ingredients and get recipe suggestions!")
    
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            if models and st.button("Analyze Image and Suggest Recipes"):
                with st.spinner("Analyzing image..."):
                    # Use BLIP model to generate image description
                    try:
                        inputs = models['image_processor'](image, return_tensors="pt")
                        out = models['image_model'].generate(**inputs, max_length=50)
                        description = models['image_processor'].decode(out[0], skip_special_tokens=True)
                        
                        st.write(f"**Detected:** {description}")
                        
                        # Find matching recipes based on description
                        matching_recipes = find_recipes_by_description(recipes_df, description, models)
                        
                        if len(matching_recipes) > 0:
                            st.subheader("Suggested Recipes:")
                            for _, recipe in matching_recipes.head(3).iterrows():
                                display_recipe_card(recipe)
                        else:
                            st.info("No specific recipes found, but here are some popular options:")
                            for _, recipe in recipes_df.head(2).iterrows():
                                display_recipe_card(recipe)
                                
                    except Exception as e:
                        st.error(f"Error analyzing image: {e}")
                        st.info("Here are some popular recipes instead:")
                        for _, recipe in recipes_df.head(2).iterrows():
                            display_recipe_card(recipe)

def find_recipes_by_description(recipes_df, description, models):
    """Find recipes that match the image description"""
    if not ML_AVAILABLE or not models or 'sentence_model' not in models:
        # ML not available - return random popular recipes
        return recipes_df.head(3)
    
    try:
        # Only use ML features if available
        from sklearn.metrics.pairwise import cosine_similarity
        
        # Create embeddings for the description
        desc_embedding = models['sentence_model'].encode([description])
        
        # Create embeddings for recipe descriptions
        recipe_descriptions = recipes_df['image_description'].tolist()
        recipe_embeddings = models['sentence_model'].encode(recipe_descriptions)
        
        # Calculate similarities
        similarities = cosine_similarity(desc_embedding, recipe_embeddings)[0]
        
        # Add similarity scores and sort
        recipes_with_scores = recipes_df.copy()
        recipes_with_scores['similarity'] = similarities
        
        return recipes_with_scores.sort_values('similarity', ascending=False)
    
    except Exception as e:
        # If any error occurs, fall back to simple recipe list
        return recipes_df.head(3)

def substitution_tab(substitutions):
    st.header("🔄 Ingredient Substitution Engine")
    st.write("Missing an ingredient? Find suitable alternatives!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Find Substitutions")
        ingredient = st.selectbox(
            "Select ingredient to substitute:",
            list(substitutions.keys())
        )
        
        if ingredient:
            st.write(f"**Substitutions for {ingredient}:**")
            for sub in substitutions[ingredient]:
                st.write(f"• {sub}")
    
    with col2:
        st.subheader("Custom Substitution Request")
        custom_ingredient = st.text_input("Enter any ingredient:")
        dietary_need = st.selectbox(
            "Substitution reason:",
            ["Allergy", "Dietary preference", "Not available", "Healthier option"]
        )
        
        if st.button("Get Substitution Suggestions") and custom_ingredient:
            # This would ideally use an AI model to generate substitutions
            st.write("**AI-Suggested Substitutions:**")
            general_suggestions = get_general_substitutions(custom_ingredient, dietary_need)
            for suggestion in general_suggestions:
                st.write(f"• {suggestion}")

def get_general_substitutions(ingredient, reason):
    """Generate general substitution suggestions"""
    # This is a simplified version - in a real app, this would use AI/ML
    common_substitutions = {
        'butter': ['olive oil', 'coconut oil', 'applesauce', 'avocado'],
        'eggs': ['flax eggs', 'chia eggs', 'applesauce', 'banana'],
        'milk': ['almond milk', 'oat milk', 'coconut milk', 'soy milk'],
        'flour': ['almond flour', 'coconut flour', 'oat flour', 'rice flour'],
        'sugar': ['honey', 'maple syrup', 'stevia', 'monk fruit']
    }
    
    ingredient_lower = ingredient.lower()
    for key in common_substitutions:
        if key in ingredient_lower:
            return common_substitutions[key]
    
    return ["Consult a nutrition expert for specific substitutions"]

def nutrition_analysis_tab(recipes_df):
    st.header("📊 Nutrition Analysis")
    
    # Select recipe for analysis
    recipe_names = recipes_df['name'].tolist()
    selected_recipe_name = st.selectbox("Select a recipe to analyze:", recipe_names)
    
    if selected_recipe_name:
        recipe = recipes_df[recipes_df['name'] == selected_recipe_name].iloc[0]
        nutrition = recipe['nutrition']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"Nutrition Breakdown: {selected_recipe_name}")
            
            # Nutrition metrics
            metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
            
            with metrics_col1:
                st.metric("Calories", f"{nutrition['calories']}")
            with metrics_col2:
                st.metric("Protein", f"{nutrition['protein']}g")
            with metrics_col3:
                st.metric("Carbs", f"{nutrition['carbs']}g")
            with metrics_col4:
                st.metric("Fat", f"{nutrition['fat']}g")
            
            # Additional nutrients
            st.write("**Additional Nutrients:**")
            st.write(f"Fiber: {nutrition['fiber']}g")
            st.write(f"Sodium: {nutrition['sodium']}mg")
        
        with col2:
            # Macronutrient pie chart
            macros = {
                'Protein': nutrition['protein'] * 4,  # 4 calories per gram
                'Carbs': nutrition['carbs'] * 4,
                'Fat': nutrition['fat'] * 9  # 9 calories per gram
            }
            
            fig = px.pie(
                values=list(macros.values()),
                names=list(macros.keys()),
                title="Macronutrient Distribution (by calories)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Health assessment
        st.subheader("Health Assessment")
        assess_recipe_health(nutrition, recipe['health_conditions'])
        
        # Scaling calculator
        st.subheader("Portion Scaling")
        new_servings = st.number_input(
            f"Scale from {recipe['servings']} servings to:",
            min_value=1,
            max_value=20,
            value=recipe['servings']
        )
        
        if new_servings != recipe['servings']:
            scale_factor = new_servings / recipe['servings']
            st.write("**Scaled Nutrition (per total recipe):**")
            for nutrient, value in nutrition.items():
                if isinstance(value, (int, float)):
                    scaled_value = value * scale_factor
                    st.write(f"{nutrient.capitalize()}: {scaled_value:.1f}")

def assess_recipe_health(nutrition, health_conditions):
    """Assess recipe health based on nutritional content"""
    assessment = []
    
    # Calorie assessment
    if nutrition['calories'] < 300:
        assessment.append("✅ Low calorie")
    elif nutrition['calories'] > 500:
        assessment.append("⚠️ High calorie")
    else:
        assessment.append("✅ Moderate calorie")
    
    # Protein assessment
    if nutrition['protein'] > 20:
        assessment.append("✅ High protein")
    elif nutrition['protein'] < 10:
        assessment.append("⚠️ Low protein")
    
    # Sodium assessment
    if nutrition['sodium'] < 300:
        assessment.append("✅ Low sodium")
    elif nutrition['sodium'] > 600:
        assessment.append("⚠️ High sodium")
    
    # Fiber assessment
    if nutrition['fiber'] > 8:
        assessment.append("✅ High fiber")
    
    # Health condition compatibility
    if 'diabetes-friendly' in health_conditions:
        assessment.append("✅ Diabetes-friendly")
    if 'heart-healthy' in health_conditions:
        assessment.append("✅ Heart-healthy")
    if 'weight-loss' in health_conditions:
        assessment.append("✅ Weight-loss friendly")
    
    for item in assessment:
        st.write(item)

def voice_assistant_tab():
    st.header("🗣️ Voice Assistant")
    st.write("Hands-free cooking guidance with voice commands!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Voice Commands")
        st.write("**Available commands:**")
        st.write("• 'Find vegetarian recipes'")
        st.write("• 'What can I cook with chicken?'")
        st.write("• 'Start cooking mode'")
        st.write("• 'Next step'")
        st.write("• 'Repeat step'")
        st.write("• 'Set timer for 10 minutes'")
        
        if st.button("🎤 Start Voice Recognition"):
            with st.spinner("Listening..."):
                # Simulate voice recognition
                st.success("Voice command received: 'Find vegetarian recipes'")
                st.write("Processing your request...")
    
    with col2:
        st.subheader("Text-to-Speech")
        text_to_speak = st.text_area(
            "Enter text to convert to speech:",
            value="Welcome to your AI cooking assistant!"
        )
        
        if st.button("🔊 Speak Text"):
            st.audio("data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABA==")  # Placeholder
            st.success("Speaking...")

def cooking_mode_tab(recipes_df):
    st.header("👨‍🍳 Interactive Cooking Mode")
    
    if not st.session_state.cooking_mode:
        st.write("Select a recipe to start interactive cooking mode:")
        
        recipe_names = recipes_df['name'].tolist()
        selected_recipe = st.selectbox("Choose recipe:", recipe_names)
        
        if st.button("Start Cooking Mode"):
            st.session_state.cooking_mode = True
            st.session_state.current_recipe = recipes_df[recipes_df['name'] == selected_recipe].iloc[0]
            st.session_state.current_step = 0
            st.rerun()
    
    else:
        recipe = st.session_state.current_recipe
        current_step = st.session_state.current_step
        
        st.subheader(f"Cooking: {recipe['name']}")
        
        # Progress bar
        progress = (current_step + 1) / len(recipe['instructions'])
        st.progress(progress)
        st.write(f"Step {current_step + 1} of {len(recipe['instructions'])}")
        
        # Current step
        if current_step < len(recipe['instructions']):
            st.markdown(f"### Current Step:")
            st.markdown(f"**{recipe['instructions'][current_step]}**")
            
            # Timer functionality
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if st.button("⏮️ Previous Step") and current_step > 0:
                    st.session_state.current_step -= 1
                    st.rerun()
            
            with col2:
                if st.button("🔊 Repeat Step"):
                    st.info(f"Repeating: {recipe['instructions'][current_step]}")
            
            with col3:
                if st.button("⏭️ Next Step"):
                    st.session_state.current_step += 1
                    st.rerun()
            
            # Timer
            st.subheader("Timer")
            timer_minutes = st.number_input("Set timer (minutes):", min_value=1, max_value=60, value=5)
            if st.button("⏰ Start Timer"):
                st.success(f"Timer set for {timer_minutes} minutes!")
        
        else:
            st.success("🎉 Cooking Complete!")
            st.balloons()
            
            if st.button("Rate This Recipe"):
                rating = st.slider("Rating (1-5 stars):", 1, 5, 5)
                st.success(f"Thank you for rating! You gave {rating} stars.")
            
            if st.button("Exit Cooking Mode"):
                st.session_state.cooking_mode = False
                st.session_state.current_step = 0
                st.rerun()

if __name__ == "__main__":
    main()