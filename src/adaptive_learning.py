import streamlit as st
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

class AdaptiveLearningEngine:
    """Adaptive learning system that learns user preferences over time"""
    
    def __init__(self):
        self.user_profiles = {}
        self.interaction_weights = {
            'view': 1.0,
            'cook': 3.0,
            'favorite': 5.0,
            'rate_high': 7.0,  # rating >= 4
            'rate_low': -2.0,  # rating < 3
            'skip': -1.0
        }
        self.preference_categories = [
            'cuisine_type', 'spice_level', 'cooking_time', 'difficulty',
            'dietary_restrictions', 'health_focus', 'ingredients'
        ]
    
    def initialize_user_profile(self, user_id: str, initial_preferences: Dict = None):
        """Initialize a new user profile"""
        self.user_profiles[user_id] = {
            'preferences': initial_preferences or {},
            'interaction_history': [],
            'learned_preferences': {
                'cuisines': {},
                'ingredients': {},
                'dietary_tags': {},
                'cooking_times': {},
                'spice_levels': {},
                'health_goals': {}
            },
            'recommendation_accuracy': [],
            'last_updated': pd.Timestamp.now()
        }
    
    def log_interaction(self, user_id: str, recipe_id: int, interaction_type: str, 
                       recipe_data: Dict, rating: int = None):
        """Log user interaction with a recipe"""
        if user_id not in self.user_profiles:
            self.initialize_user_profile(user_id)
        
        # Determine interaction weight
        if interaction_type == 'rate' and rating:
            weight = self.interaction_weights['rate_high'] if rating >= 4 else self.interaction_weights['rate_low']
        else:
            weight = self.interaction_weights.get(interaction_type, 1.0)
        
        # Log interaction
        interaction = {
            'recipe_id': recipe_id,
            'interaction_type': interaction_type,
            'weight': weight,
            'rating': rating,
            'timestamp': pd.Timestamp.now(),
            'recipe_features': self._extract_recipe_features(recipe_data)
        }
        
        self.user_profiles[user_id]['interaction_history'].append(interaction)
        
        # Update learned preferences
        self._update_learned_preferences(user_id, recipe_data, weight)
    
    def _extract_recipe_features(self, recipe_data: Dict) -> Dict:
        """Extract key features from recipe data"""
        return {
            'cuisine': recipe_data.get('cuisine', ''),
            'cooking_time': recipe_data.get('cooking_time', 0),
            'difficulty': recipe_data.get('difficulty', ''),
            'dietary_tags': recipe_data.get('dietary_tags', []),
            'health_conditions': recipe_data.get('health_conditions', []),
            'spice_level': 'spicy' in recipe_data.get('dietary_tags', []),
            'calories': recipe_data.get('nutrition', {}).get('calories', 0),
            'protein': recipe_data.get('nutrition', {}).get('protein', 0),
            'main_ingredients': recipe_data.get('ingredients', [])[:3]  # First 3 ingredients
        }
    
    def _update_learned_preferences(self, user_id: str, recipe_data: Dict, weight: float):
        """Update learned preferences based on interaction"""
        profile = self.user_profiles[user_id]
        learned = profile['learned_preferences']
        
        # Update cuisine preferences
        cuisine = recipe_data.get('cuisine', '')
        if cuisine:
            learned['cuisines'][cuisine] = learned['cuisines'].get(cuisine, 0) + weight
        
        # Update dietary tag preferences
        for tag in recipe_data.get('dietary_tags', []):
            learned['dietary_tags'][tag] = learned['dietary_tags'].get(tag, 0) + weight
        
        # Update cooking time preferences
        cooking_time = recipe_data.get('cooking_time', 0)
        time_category = self._categorize_cooking_time(cooking_time)
        learned['cooking_times'][time_category] = learned['cooking_times'].get(time_category, 0) + weight
        
        # Update ingredient preferences
        for ingredient in recipe_data.get('ingredients', [])[:5]:  # Top 5 ingredients
            learned['ingredients'][ingredient] = learned['ingredients'].get(ingredient, 0) + weight
        
        # Update health goal preferences
        for condition in recipe_data.get('health_conditions', []):
            learned['health_goals'][condition] = learned['health_goals'].get(condition, 0) + weight
        
        # Update spice level preferences
        if 'spicy' in recipe_data.get('dietary_tags', []):
            learned['spice_levels']['spicy'] = learned['spice_levels'].get('spicy', 0) + weight
        else:
            learned['spice_levels']['mild'] = learned['spice_levels'].get('mild', 0) + weight
        
        profile['last_updated'] = pd.Timestamp.now()
    
    def _categorize_cooking_time(self, cooking_time: int) -> str:
        """Categorize cooking time into buckets"""
        if cooking_time <= 20:
            return 'quick'
        elif cooking_time <= 45:
            return 'medium'
        else:
            return 'long'
    
    def get_user_preferences_summary(self, user_id: str) -> Dict:
        """Get a summary of user's learned preferences"""
        if user_id not in self.user_profiles:
            return {}
        
        learned = self.user_profiles[user_id]['learned_preferences']
        summary = {}
        
        # Get top preferences in each category
        for category, preferences in learned.items():
            if preferences:
                sorted_prefs = sorted(preferences.items(), key=lambda x: x[1], reverse=True)
                summary[category] = {
                    'top_preference': sorted_prefs[0][0] if sorted_prefs else None,
                    'top_score': sorted_prefs[0][1] if sorted_prefs else 0,
                    'all_preferences': dict(sorted_prefs[:5])  # Top 5
                }
        
        return summary
    
    def generate_personalized_recommendations(self, user_id: str, available_recipes: List[Dict], 
                                            limit: int = 10) -> List[Dict]:
        """Generate personalized recipe recommendations"""
        if user_id not in self.user_profiles:
            # Return popular recipes for new users
            return sorted(available_recipes, key=lambda x: x.get('rating', 0), reverse=True)[:limit]
        
        learned = self.user_profiles[user_id]['learned_preferences']
        scored_recipes = []
        
        for recipe in available_recipes:
            score = self._calculate_recipe_score(recipe, learned)
            recipe_with_score = recipe.copy()
            recipe_with_score['personalization_score'] = score
            scored_recipes.append(recipe_with_score)
        
        # Sort by personalization score
        scored_recipes.sort(key=lambda x: x['personalization_score'], reverse=True)
        
        return scored_recipes[:limit]
    
    def _calculate_recipe_score(self, recipe: Dict, learned_preferences: Dict) -> float:
        """Calculate personalization score for a recipe"""
        score = 0.0
        
        # Cuisine preference
        cuisine = recipe.get('cuisine', '')
        if cuisine in learned_preferences.get('cuisines', {}):
            score += learned_preferences['cuisines'][cuisine] * 0.3
        
        # Dietary tags preference
        for tag in recipe.get('dietary_tags', []):
            if tag in learned_preferences.get('dietary_tags', {}):
                score += learned_preferences['dietary_tags'][tag] * 0.2
        
        # Cooking time preference
        cooking_time = recipe.get('cooking_time', 0)
        time_category = self._categorize_cooking_time(cooking_time)
        if time_category in learned_preferences.get('cooking_times', {}):
            score += learned_preferences['cooking_times'][time_category] * 0.15
        
        # Ingredient preference
        for ingredient in recipe.get('ingredients', []):
            if ingredient in learned_preferences.get('ingredients', {}):
                score += learned_preferences['ingredients'][ingredient] * 0.1
        
        # Health goals preference
        for condition in recipe.get('health_conditions', []):
            if condition in learned_preferences.get('health_goals', {}):
                score += learned_preferences['health_goals'][condition] * 0.2
        
        # Spice level preference
        is_spicy = 'spicy' in recipe.get('dietary_tags', [])
        spice_prefs = learned_preferences.get('spice_levels', {})
        if is_spicy and 'spicy' in spice_prefs:
            score += spice_prefs['spicy'] * 0.05
        elif not is_spicy and 'mild' in spice_prefs:
            score += spice_prefs['mild'] * 0.05
        
        return max(0, score)  # Ensure non-negative score
    
    def get_recommendation_explanation(self, user_id: str, recipe: Dict) -> List[str]:
        """Explain why a recipe was recommended to the user"""
        if user_id not in self.user_profiles:
            return ["Recommended as a popular recipe"]
        
        learned = self.user_profiles[user_id]['learned_preferences']
        explanations = []
        
        # Check cuisine match
        cuisine = recipe.get('cuisine', '')
        if cuisine in learned.get('cuisines', {}) and learned['cuisines'][cuisine] > 2:
            explanations.append(f"You seem to enjoy {cuisine} cuisine")
        
        # Check dietary preferences
        matching_tags = []
        for tag in recipe.get('dietary_tags', []):
            if tag in learned.get('dietary_tags', {}) and learned['dietary_tags'][tag] > 1:
                matching_tags.append(tag)
        
        if matching_tags:
            explanations.append(f"Matches your preferences: {', '.join(matching_tags)}")
        
        # Check cooking time preference
        cooking_time = recipe.get('cooking_time', 0)
        time_category = self._categorize_cooking_time(cooking_time)
        if time_category in learned.get('cooking_times', {}) and learned['cooking_times'][time_category] > 1:
            explanations.append(f"Fits your preferred cooking time ({time_category})")
        
        # Check ingredient preferences
        liked_ingredients = []
        for ingredient in recipe.get('ingredients', []):
            if ingredient in learned.get('ingredients', {}) and learned['ingredients'][ingredient] > 1:
                liked_ingredients.append(ingredient)
        
        if liked_ingredients:
            explanations.append(f"Contains ingredients you like: {', '.join(liked_ingredients[:3])}")
        
        # Check health goals
        matching_goals = []
        for condition in recipe.get('health_conditions', []):
            if condition in learned.get('health_goals', {}) and learned['health_goals'][condition] > 1:
                matching_goals.append(condition.replace('-', ' ').replace('_', ' '))
        
        if matching_goals:
            explanations.append(f"Aligns with your health goals: {', '.join(matching_goals)}")
        
        return explanations if explanations else ["Recommended based on overall preferences"]
    
    def adapt_search_results(self, user_id: str, search_results: List[Dict]) -> List[Dict]:
        """Re-rank search results based on user preferences"""
        if user_id not in self.user_profiles:
            return search_results
        
        personalized = self.generate_personalized_recommendations(user_id, search_results, len(search_results))
        return personalized
    
    def get_user_insights(self, user_id: str) -> Dict:
        """Get insights about user's cooking preferences and habits"""
        if user_id not in self.user_profiles:
            return {}
        
        profile = self.user_profiles[user_id]
        interactions = profile['interaction_history']
        
        if not interactions:
            return {}
        
        insights = {
            'total_interactions': len(interactions),
            'favorite_recipes': len([i for i in interactions if i['interaction_type'] == 'favorite']),
            'recipes_cooked': len([i for i in interactions if i['interaction_type'] == 'cook']),
            'average_rating': np.mean([i['rating'] for i in interactions if i['rating']]) if any(i['rating'] for i in interactions) else None,
            'most_active_time': self._get_most_active_time(interactions),
            'cooking_frequency': len(interactions) / max(1, (pd.Timestamp.now() - min(i['timestamp'] for i in interactions)).days),
            'preference_strength': self._calculate_preference_strength(profile['learned_preferences'])
        }
        
        return insights
    
    def _get_most_active_time(self, interactions: List[Dict]) -> str:
        """Determine when user is most active"""
        if not interactions:
            return "Unknown"
        
        hours = [i['timestamp'].hour for i in interactions]
        most_common_hour = max(set(hours), key=hours.count)
        
        if 6 <= most_common_hour < 12:
            return "Morning"
        elif 12 <= most_common_hour < 17:
            return "Afternoon"
        elif 17 <= most_common_hour < 21:
            return "Evening"
        else:
            return "Night"
    
    def _calculate_preference_strength(self, learned_preferences: Dict) -> float:
        """Calculate how strong/defined the user's preferences are"""
        total_interactions = 0
        strong_preferences = 0
        
        for category, prefs in learned_preferences.items():
            for pref, score in prefs.items():
                total_interactions += abs(score)
                if abs(score) > 3:  # Strong preference threshold
                    strong_preferences += 1
        
        if total_interactions == 0:
            return 0.0
        
        return strong_preferences / max(1, len([p for category in learned_preferences.values() for p in category]))

# Streamlit integration functions
def display_adaptive_learning_insights(learning_engine: AdaptiveLearningEngine, user_id: str):
    """Display adaptive learning insights in Streamlit"""
    st.subheader("🧠 Your Learning Profile")
    
    if user_id not in learning_engine.user_profiles:
        st.info("Start interacting with recipes to build your personalized profile!")
        return
    
    # Get user insights
    insights = learning_engine.get_user_insights(user_id)
    preferences_summary = learning_engine.get_user_preferences_summary(user_id)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Interactions", insights.get('total_interactions', 0))
    with col2:
        st.metric("Recipes Cooked", insights.get('recipes_cooked', 0))
    with col3:
        st.metric("Favorites", insights.get('favorite_recipes', 0))
    with col4:
        avg_rating = insights.get('average_rating')
        st.metric("Avg Rating", f"{avg_rating:.1f}" if avg_rating else "N/A")
    
    # Display top preferences
    if preferences_summary:
        st.subheader("Your Top Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'cuisines' in preferences_summary:
                st.write("**Favorite Cuisines:**")
                for cuisine, score in list(preferences_summary['cuisines']['all_preferences'].items())[:3]:
                    st.write(f"• {cuisine} ({score:.1f})")
            
            if 'dietary_tags' in preferences_summary:
                st.write("**Dietary Preferences:**")
                for tag, score in list(preferences_summary['dietary_tags']['all_preferences'].items())[:3]:
                    st.write(f"• {tag.replace('_', ' ')} ({score:.1f})")
        
        with col2:
            if 'cooking_times' in preferences_summary:
                st.write("**Cooking Time Preference:**")
                for time_cat, score in list(preferences_summary['cooking_times']['all_preferences'].items())[:3]:
                    st.write(f"• {time_cat} recipes ({score:.1f})")
            
            if 'health_goals' in preferences_summary:
                st.write("**Health Focus:**")
                for goal, score in list(preferences_summary['health_goals']['all_preferences'].items())[:3]:
                    st.write(f"• {goal.replace('_', ' ')} ({score:.1f})")

def display_recommendation_explanations(learning_engine: AdaptiveLearningEngine, user_id: str, recipe: Dict):
    """Display why a recipe was recommended"""
    explanations = learning_engine.get_recommendation_explanation(user_id, recipe)
    
    if explanations and explanations != ["Recommended as a popular recipe"]:
        st.info("💡 **Why this recipe for you:** " + "; ".join(explanations))

# Example usage
if __name__ == "__main__":
    # Initialize learning engine
    learning_engine = AdaptiveLearningEngine()
    
    # Example usage
    user_id = "test_user"
    learning_engine.initialize_user_profile(user_id)
    
    # Example recipe data
    recipe_data = {
        'id': 1,
        'name': 'Spicy Thai Curry',
        'cuisine': 'Thai',
        'cooking_time': 30,
        'difficulty': 'Medium',
        'dietary_tags': ['spicy', 'gluten-free'],
        'health_conditions': ['heart-healthy'],
        'ingredients': ['chicken', 'curry paste', 'coconut milk'],
        'nutrition': {'calories': 380, 'protein': 28}
    }
    
    # Log interactions
    learning_engine.log_interaction(user_id, 1, 'view', recipe_data)
    learning_engine.log_interaction(user_id, 1, 'cook', recipe_data)
    learning_engine.log_interaction(user_id, 1, 'rate', recipe_data, rating=5)
    
    # Get recommendations
    recommendations = learning_engine.generate_personalized_recommendations(user_id, [recipe_data])
    print("Personalized recommendations:", len(recommendations))