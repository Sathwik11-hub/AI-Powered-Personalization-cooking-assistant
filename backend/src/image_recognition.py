import cv2
import numpy as np
from PIL import Image
import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from typing import List, Dict, Any, Tuple
import re

class ImageRecognitionEngine:
    """Advanced image recognition for ingredient and food identification"""
    
    def __init__(self):
        self.load_models()
        self.ingredient_keywords = self.load_ingredient_keywords()
        self.food_categories = self.load_food_categories()
    
    @st.cache_resource
    def load_models(_self):
        """Load image recognition models"""
        try:
            # BLIP model for image captioning
            processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            
            return {
                'blip_processor': processor,
                'blip_model': model
            }
        except Exception as e:
            st.error(f"Error loading models: {e}")
            return None
    
    def load_ingredient_keywords(self):
        """Load comprehensive ingredient keyword mapping"""
        return {
            'vegetables': [
                'tomato', 'tomatoes', 'onion', 'onions', 'carrot', 'carrots',
                'broccoli', 'spinach', 'lettuce', 'bell pepper', 'peppers',
                'cucumber', 'zucchini', 'eggplant', 'potato', 'potatoes',
                'garlic', 'ginger', 'mushroom', 'mushrooms', 'avocado',
                'corn', 'peas', 'beans', 'celery', 'cauliflower'
            ],
            'fruits': [
                'apple', 'apples', 'banana', 'bananas', 'orange', 'oranges',
                'lemon', 'lemons', 'lime', 'limes', 'strawberry', 'strawberries',
                'blueberry', 'blueberries', 'grape', 'grapes', 'pineapple',
                'mango', 'kiwi', 'peach', 'pear', 'cherry', 'cherries'
            ],
            'proteins': [
                'chicken', 'beef', 'pork', 'fish', 'salmon', 'tuna',
                'shrimp', 'eggs', 'tofu', 'beans', 'lentils', 'chickpeas',
                'turkey', 'lamb', 'bacon', 'ham', 'cheese', 'nuts'
            ],
            'grains': [
                'rice', 'pasta', 'bread', 'quinoa', 'oats', 'barley',
                'wheat', 'flour', 'cereal', 'noodles', 'couscous'
            ],
            'dairy': [
                'milk', 'cheese', 'yogurt', 'butter', 'cream', 'ice cream'
            ],
            'herbs_spices': [
                'basil', 'oregano', 'thyme', 'rosemary', 'parsley', 'cilantro',
                'mint', 'sage', 'cinnamon', 'pepper', 'salt', 'cumin',
                'paprika', 'turmeric', 'ginger', 'garlic'
            ]
        }
    
    def load_food_categories(self):
        """Load food category mappings for better classification"""
        return {
            'fresh_produce': ['vegetables', 'fruits'],
            'protein_sources': ['proteins', 'dairy'],
            'pantry_staples': ['grains', 'herbs_spices'],
            'cooking_essentials': ['oil', 'vinegar', 'sauce', 'broth']
        }
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better recognition"""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        """Comprehensive image analysis"""
        image = self.preprocess_image(image)
        
        analysis_result = {
            'raw_description': '',
            'identified_ingredients': [],
            'ingredient_categories': {},
            'confidence_scores': {},
            'recipe_suggestions': [],
            'cooking_methods': [],
            'estimated_servings': 1
        }
        
        # Get image description using BLIP
        try:
            models = self.load_models()
            if models:
                # Generate description
                inputs = models['blip_processor'](image, return_tensors="pt")
                out = models['blip_model'].generate(**inputs, max_length=100, num_beams=5)
                description = models['blip_processor'].decode(out[0], skip_special_tokens=True)
                
                analysis_result['raw_description'] = description
                
                # Extract ingredients from description
                ingredients = self.extract_ingredients_from_description(description)
                analysis_result['identified_ingredients'] = ingredients
                
                # Categorize ingredients
                analysis_result['ingredient_categories'] = self.categorize_ingredients(ingredients)
                
                # Suggest cooking methods
                analysis_result['cooking_methods'] = self.suggest_cooking_methods(ingredients)
                
                # Estimate servings
                analysis_result['estimated_servings'] = self.estimate_servings(ingredients, description)
                
        except Exception as e:
            st.error(f"Error in image analysis: {e}")
            analysis_result['raw_description'] = "Unable to analyze image"
        
        return analysis_result
    
    def extract_ingredients_from_description(self, description: str) -> List[str]:
        """Extract ingredients from image description"""
        description_lower = description.lower()
        identified_ingredients = []
        
        # Check for each ingredient category
        for category, ingredients in self.ingredient_keywords.items():
            for ingredient in ingredients:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(ingredient.lower()) + r'\b'
                if re.search(pattern, description_lower):
                    identified_ingredients.append(ingredient)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(identified_ingredients))
    
    def categorize_ingredients(self, ingredients: List[str]) -> Dict[str, List[str]]:
        """Categorize identified ingredients"""
        categorized = {category: [] for category in self.ingredient_keywords.keys()}
        
        for ingredient in ingredients:
            for category, category_ingredients in self.ingredient_keywords.items():
                if ingredient.lower() in [ing.lower() for ing in category_ingredients]:
                    categorized[category].append(ingredient)
                    break
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def suggest_cooking_methods(self, ingredients: List[str]) -> List[str]:
        """Suggest cooking methods based on identified ingredients"""
        cooking_methods = []
        
        # Method suggestions based on ingredients
        method_mappings = {
            'stir_fry': ['vegetables', 'bell pepper', 'broccoli', 'carrot'],
            'salad': ['lettuce', 'cucumber', 'tomato', 'avocado'],
            'soup': ['onion', 'carrot', 'celery', 'broth'],
            'pasta': ['pasta', 'noodles', 'tomato', 'cheese'],
            'grilling': ['chicken', 'beef', 'fish', 'vegetables'],
            'baking': ['chicken', 'fish', 'potato', 'vegetables'],
            'steaming': ['broccoli', 'cauliflower', 'fish', 'vegetables'],
            'roasting': ['potato', 'carrot', 'chicken', 'beef']
        }
        
        ingredient_set = set(ing.lower() for ing in ingredients)
        
        for method, method_ingredients in method_mappings.items():
            if any(ing in ingredient_set for ing in method_ingredients):
                cooking_methods.append(method.replace('_', ' ').title())
        
        return cooking_methods
    
    def estimate_servings(self, ingredients: List[str], description: str) -> int:
        """Estimate number of servings based on ingredients and description"""
        # Simple heuristic based on number of ingredients and description
        base_servings = 1
        
        # More ingredients typically mean more servings
        if len(ingredients) > 5:
            base_servings = 2
        if len(ingredients) > 8:
            base_servings = 3
        if len(ingredients) > 12:
            base_servings = 4
        
        # Look for quantity indicators in description
        quantity_words = ['many', 'several', 'bunch', 'lots', 'multiple']
        if any(word in description.lower() for word in quantity_words):
            base_servings += 1
        
        return min(6, max(1, base_servings))  # Cap between 1-6 servings
    
    def find_matching_recipes(self, analysis_result: Dict, recipe_database: List[Dict]) -> List[Dict]:
        """Find recipes that match identified ingredients"""
        identified_ingredients = set(ing.lower() for ing in analysis_result['identified_ingredients'])
        matching_recipes = []
        
        for recipe in recipe_database:
            recipe_ingredients = set(ing.lower() for ing in recipe.get('ingredients', []))
            
            # Calculate ingredient match percentage
            if recipe_ingredients:
                overlap = identified_ingredients.intersection(recipe_ingredients)
                match_percentage = len(overlap) / len(recipe_ingredients) * 100
                
                if match_percentage > 20:  # At least 20% ingredient match
                    recipe_with_score = recipe.copy()
                    recipe_with_score['ingredient_match_score'] = match_percentage
                    recipe_with_score['matching_ingredients'] = list(overlap)
                    matching_recipes.append(recipe_with_score)
        
        # Sort by match score
        matching_recipes.sort(key=lambda x: x['ingredient_match_score'], reverse=True)
        
        return matching_recipes
    
    def generate_recipe_suggestions(self, analysis_result: Dict) -> List[Dict]:
        """Generate recipe suggestions based on image analysis"""
        ingredients = analysis_result['identified_ingredients']
        categories = analysis_result['ingredient_categories']
        cooking_methods = analysis_result['cooking_methods']
        
        suggestions = []
        
        # Generate suggestions based on ingredient combinations
        if 'vegetables' in categories and 'proteins' in categories:
            suggestions.append({
                'recipe_type': 'Stir Fry',
                'description': f"Stir fry with {', '.join(categories['vegetables'])} and {', '.join(categories['proteins'])}",
                'cooking_time': 20,
                'difficulty': 'Easy'
            })
        
        if 'vegetables' in categories and len(categories['vegetables']) >= 3:
            suggestions.append({
                'recipe_type': 'Fresh Salad',
                'description': f"Mixed salad with {', '.join(categories['vegetables'])}",
                'cooking_time': 10,
                'difficulty': 'Easy'
            })
        
        if 'proteins' in categories and 'vegetables' in categories:
            suggestions.append({
                'recipe_type': 'Healthy Bowl',
                'description': f"Protein bowl with {', '.join(categories['proteins'])} and vegetables",
                'cooking_time': 25,
                'difficulty': 'Medium'
            })
        
        # Add cooking method suggestions
        for method in cooking_methods:
            suggestions.append({
                'recipe_type': f'{method} Recipe',
                'description': f'{method} using available ingredients',
                'cooking_time': 30,
                'difficulty': 'Medium'
            })
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def validate_ingredient_image(self, image: Image.Image) -> Dict[str, Any]:
        """Validate if image contains food/ingredients"""
        analysis = self.analyze_image(image)
        
        validation_result = {
            'is_food_image': False,
            'confidence': 0.0,
            'detected_items': analysis['identified_ingredients'],
            'suggestions': []
        }
        
        # Check if any food-related items were detected
        if analysis['identified_ingredients']:
            validation_result['is_food_image'] = True
            validation_result['confidence'] = min(0.9, len(analysis['identified_ingredients']) * 0.15)
        
        # Additional validation based on description
        food_keywords = ['food', 'ingredient', 'vegetable', 'fruit', 'meat', 'cooking', 'kitchen']
        description_lower = analysis['raw_description'].lower()
        
        if any(keyword in description_lower for keyword in food_keywords):
            validation_result['is_food_image'] = True
            validation_result['confidence'] = max(validation_result['confidence'], 0.6)
        
        # Provide suggestions if not a food image
        if not validation_result['is_food_image']:
            validation_result['suggestions'] = [
                "Try uploading a clearer image of ingredients",
                "Ensure good lighting and focus",
                "Include multiple ingredients in the frame",
                "Avoid cluttered backgrounds"
            ]
        
        return validation_result

# Streamlit integration functions
def display_image_analysis_results(analysis_result: Dict):
    """Display image analysis results in Streamlit"""
    st.subheader("📸 Image Analysis Results")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**AI Description:**")
        st.write(analysis_result['raw_description'])
        
        if analysis_result['identified_ingredients']:
            st.write("**Identified Ingredients:**")
            for ingredient in analysis_result['identified_ingredients']:
                st.write(f"• {ingredient}")
        else:
            st.warning("No ingredients clearly identified. Try a clearer image.")
    
    with col2:
        if analysis_result['ingredient_categories']:
            st.write("**Ingredient Categories:**")
            for category, ingredients in analysis_result['ingredient_categories'].items():
                if ingredients:
                    st.write(f"**{category.replace('_', ' ').title()}:** {', '.join(ingredients)}")
        
        if analysis_result['cooking_methods']:
            st.write("**Suggested Cooking Methods:**")
            for method in analysis_result['cooking_methods']:
                st.write(f"• {method}")
    
    # Display recipe suggestions
    if analysis_result.get('recipe_suggestions'):
        st.subheader("💡 Recipe Suggestions")
        suggestions = analysis_result['recipe_suggestions']
        
        for suggestion in suggestions:
            with st.expander(f"{suggestion['recipe_type']} ({suggestion['cooking_time']} min)"):
                st.write(suggestion['description'])
                st.write(f"**Difficulty:** {suggestion['difficulty']}")

def create_image_upload_interface():
    """Create image upload interface with validation"""
    st.subheader("📸 Upload Ingredient Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of ingredients you want to cook with"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            # Image validation
            engine = ImageRecognitionEngine()
            validation = engine.validate_ingredient_image(image)
            
            if validation['is_food_image']:
                st.success(f"✅ Food image detected (Confidence: {validation['confidence']:.1%})")
                
                if st.button("🔍 Analyze Image"):
                    with st.spinner("Analyzing image..."):
                        analysis_result = engine.analyze_image(image)
                        display_image_analysis_results(analysis_result)
                        return analysis_result
            else:
                st.warning("⚠️ This doesn't appear to be a food/ingredient image")
                st.write("**Suggestions:**")
                for suggestion in validation['suggestions']:
                    st.write(f"• {suggestion}")
    
    return None

# Example usage
if __name__ == "__main__":
    engine = ImageRecognitionEngine()
    
    # Test with example description
    test_description = "a bowl of fresh vegetables including tomatoes, onions, and bell peppers"
    ingredients = engine.extract_ingredients_from_description(test_description)
    print(f"Identified ingredients: {ingredients}")
    
    categories = engine.categorize_ingredients(ingredients)
    print(f"Categorized ingredients: {categories}")