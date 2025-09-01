import json
import streamlit as st
from typing import Dict, List, Any

class UserProfileManager:
    """Manage user profiles and preferences"""
    
    def __init__(self):
        self.default_profile = {
            'user_id': '',
            'name': '',
            'age_group': 'adult',
            'dietary_restrictions': [],
            'health_conditions': [],
            'cooking_skill': 'beginner',
            'preferred_cuisines': [],
            'spice_tolerance': 'medium',
            'cooking_time_preference': 'medium',
            'budget_preference': 'medium',
            'kitchen_equipment': [],
            'allergens': [],
            'nutrition_goals': {
                'calories': 2000,
                'protein': 50,
                'carbs': 250,
                'fat': 65
            },
            'preferences_learned': {
                'favorite_recipes': [],
                'disliked_ingredients': [],
                'cooking_patterns': {}
            },
            'created_at': '',
            'last_active': ''
        }
    
    def create_user_profile(self, user_data: Dict) -> Dict:
        """Create a new user profile"""
        profile = self.default_profile.copy()
        profile.update(user_data)
        return profile
    
    def update_profile_preferences(self, profile: Dict, preferences: Dict) -> Dict:
        """Update user preferences"""
        profile.update(preferences)
        return profile
    
    def get_dietary_recommendations(self, profile: Dict) -> List[str]:
        """Get dietary recommendations based on profile"""
        recommendations = []
        
        # Health condition recommendations
        health_conditions = profile.get('health_conditions', [])
        if 'diabetes' in health_conditions:
            recommendations.extend([
                "Focus on low-glycemic index foods",
                "Limit simple carbohydrates and sugars",
                "Include high-fiber foods"
            ])
        
        if 'heart_disease' in health_conditions:
            recommendations.extend([
                "Reduce sodium intake",
                "Choose lean proteins",
                "Include omega-3 rich foods"
            ])
        
        if 'weight_loss' in health_conditions:
            recommendations.extend([
                "Focus on high-protein, low-calorie foods",
                "Increase vegetable intake",
                "Control portion sizes"
            ])
        
        # Dietary restriction recommendations
        restrictions = profile.get('dietary_restrictions', [])
        if 'vegetarian' in restrictions:
            recommendations.append("Ensure adequate protein from plant sources")
        
        if 'vegan' in restrictions:
            recommendations.extend([
                "Monitor B12 intake",
                "Include variety of plant proteins",
                "Consider calcium-rich foods"
            ])
        
        return recommendations
    
    def calculate_nutrition_targets(self, profile: Dict) -> Dict:
        """Calculate personalized nutrition targets"""
        age_group = profile.get('age_group', 'adult')
        health_conditions = profile.get('health_conditions', [])
        goals = profile.get('nutrition_goals', {})
        
        # Base targets
        targets = {
            'calories': 2000,
            'protein': 50,
            'carbs': 250,
            'fat': 65,
            'fiber': 25,
            'sodium': 2300
        }
        
        # Adjust for age group
        if age_group == 'child':
            targets['calories'] = 1800
            targets['protein'] = 34
            targets['carbs'] = 225
        elif age_group == 'elderly':
            targets['protein'] = 60  # Higher protein for elderly
        
        # Adjust for health conditions
        if 'diabetes' in health_conditions:
            targets['carbs'] = 180  # Lower carbs
            targets['fiber'] = 35   # Higher fiber
        
        if 'heart_disease' in health_conditions:
            targets['sodium'] = 1500  # Lower sodium
        
        if 'weight_loss' in health_conditions:
            targets['calories'] = 1500  # Caloric deficit
            targets['protein'] = 75     # Higher protein
        
        # Override with user-specified goals
        targets.update(goals)
        
        return targets

class RecipePersonalizer:
    """Personalize recipes based on user preferences"""
    
    def __init__(self):
        self.profile_manager = UserProfileManager()
    
    def personalize_recipe(self, recipe: Dict, user_profile: Dict) -> Dict:
        """Personalize a recipe for a specific user"""
        personalized = recipe.copy()
        
        # Adjust spice level
        spice_tolerance = user_profile.get('spice_tolerance', 'medium')
        if spice_tolerance == 'mild':
            personalized = self._reduce_spice(personalized)
        elif spice_tolerance == 'hot':
            personalized = self._increase_spice(personalized)
        
        # Adjust for dietary restrictions
        restrictions = user_profile.get('dietary_restrictions', [])
        if restrictions:
            personalized = self._apply_dietary_restrictions(personalized, restrictions)
        
        # Adjust for allergens
        allergens = user_profile.get('allergens', [])
        if allergens:
            personalized = self._remove_allergens(personalized, allergens)
        
        # Scale for cooking skill
        skill = user_profile.get('cooking_skill', 'beginner')
        if skill == 'beginner':
            personalized = self._simplify_recipe(personalized)
        elif skill == 'advanced':
            personalized = self._enhance_recipe(personalized)
        
        return personalized
    
    def _reduce_spice(self, recipe: Dict) -> Dict:
        """Reduce spice level in recipe"""
        # Identify and reduce spicy ingredients
        spicy_ingredients = ['chili', 'pepper', 'hot sauce', 'cayenne', 'paprika']
        
        modified_ingredients = []
        for ingredient in recipe.get('ingredients', []):
            ingredient_lower = ingredient.lower()
            if any(spice in ingredient_lower for spice in spicy_ingredients):
                modified_ingredients.append(f"Reduced {ingredient}")
            else:
                modified_ingredients.append(ingredient)
        
        recipe['ingredients'] = modified_ingredients
        recipe['notes'] = recipe.get('notes', []) + ["Spice level reduced for mild preference"]
        
        return recipe
    
    def _increase_spice(self, recipe: Dict) -> Dict:
        """Increase spice level in recipe"""
        # Add spicy ingredients or increase quantities
        recipe['ingredients'].append("Extra chili flakes (to taste)")
        recipe['notes'] = recipe.get('notes', []) + ["Spice level increased for hot preference"]
        
        return recipe
    
    def _apply_dietary_restrictions(self, recipe: Dict, restrictions: List[str]) -> Dict:
        """Apply dietary restrictions to recipe"""
        substitutions = []
        
        if 'vegetarian' in restrictions:
            # Replace meat with vegetarian alternatives
            meat_substitutions = {
                'chicken': 'tofu or tempeh',
                'beef': 'mushrooms or lentils',
                'pork': 'jackfruit or tempeh'
            }
            
            for meat, substitute in meat_substitutions.items():
                recipe['ingredients'] = [
                    ing.replace(meat, substitute) if meat in ing.lower() else ing
                    for ing in recipe['ingredients']
                ]
                if meat in str(recipe['ingredients']).lower():
                    substitutions.append(f"Replaced {meat} with {substitute}")
        
        if 'vegan' in restrictions:
            # Replace dairy and eggs
            vegan_substitutions = {
                'milk': 'plant-based milk',
                'cheese': 'nutritional yeast or vegan cheese',
                'butter': 'olive oil or vegan butter',
                'egg': 'flax egg or applesauce'
            }
            
            for dairy, substitute in vegan_substitutions.items():
                recipe['ingredients'] = [
                    ing.replace(dairy, substitute) if dairy in ing.lower() else ing
                    for ing in recipe['ingredients']
                ]
                if dairy in str(recipe['ingredients']).lower():
                    substitutions.append(f"Replaced {dairy} with {substitute}")
        
        if substitutions:
            recipe['dietary_modifications'] = substitutions
        
        return recipe
    
    def _remove_allergens(self, recipe: Dict, allergens: List[str]) -> Dict:
        """Remove or substitute allergenic ingredients"""
        allergen_substitutions = {
            'nuts': 'seeds or avoid',
            'dairy': 'dairy-free alternatives',
            'gluten': 'gluten-free alternatives',
            'soy': 'soy-free alternatives',
            'eggs': 'egg replacer'
        }
        
        modifications = []
        for allergen in allergens:
            if allergen in allergen_substitutions:
                substitute = allergen_substitutions[allergen]
                # Check if allergen present in ingredients
                allergen_present = any(allergen in ing.lower() for ing in recipe['ingredients'])
                if allergen_present:
                    modifications.append(f"⚠️ Contains {allergen} - use {substitute}")
        
        if modifications:
            recipe['allergen_warnings'] = modifications
        
        return recipe
    
    def _simplify_recipe(self, recipe: Dict) -> Dict:
        """Simplify recipe for beginners"""
        # Add helpful tips and simplify instructions
        if 'cooking_tips' not in recipe:
            recipe['cooking_tips'] = []
        
        recipe['cooking_tips'].extend([
            "Take your time with each step",
            "Prep all ingredients before starting",
            "Don't hesitate to taste and adjust seasoning"
        ])
        
        return recipe
    
    def _enhance_recipe(self, recipe: Dict) -> Dict:
        """Enhance recipe for advanced cooks"""
        # Add advanced techniques and variations
        if 'advanced_tips' not in recipe:
            recipe['advanced_tips'] = []
        
        recipe['advanced_tips'].extend([
            "Consider making your own spice blends",
            "Try different cooking techniques for variation",
            "Experiment with ingredient ratios to taste"
        ])
        
        return recipe

# Streamlit integration functions
def display_user_profile_setup():
    """Display user profile setup interface"""
    st.subheader("🔧 Set Up Your Cooking Profile")
    
    with st.form("user_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name (optional)")
            age_group = st.selectbox("Age Group", ['child', 'adult', 'elderly'])
            cooking_skill = st.selectbox("Cooking Skill Level", ['beginner', 'intermediate', 'advanced'])
            spice_tolerance = st.selectbox("Spice Tolerance", ['mild', 'medium', 'hot'])
        
        with col2:
            dietary_restrictions = st.multiselect(
                "Dietary Restrictions",
                ['vegetarian', 'vegan', 'pescatarian', 'keto', 'paleo', 'gluten-free']
            )
            
            health_conditions = st.multiselect(
                "Health Conditions",
                ['diabetes', 'heart_disease', 'weight_loss', 'high_blood_pressure', 'high_cholesterol']
            )
            
            allergens = st.multiselect(
                "Allergens to Avoid",
                ['nuts', 'dairy', 'eggs', 'soy', 'shellfish', 'gluten']
            )
        
        # Nutrition goals
        st.subheader("Nutrition Goals")
        col3, col4, col5, col6 = st.columns(4)
        
        with col3:
            target_calories = st.number_input("Daily Calories", min_value=1000, max_value=4000, value=2000)
        with col4:
            target_protein = st.number_input("Protein (g)", min_value=20, max_value=200, value=50)
        with col5:
            target_carbs = st.number_input("Carbs (g)", min_value=50, max_value=500, value=250)
        with col6:
            target_fat = st.number_input("Fat (g)", min_value=20, max_value=200, value=65)
        
        submitted = st.form_submit_button("Save Profile")
        
        if submitted:
            profile_data = {
                'name': name,
                'age_group': age_group,
                'cooking_skill': cooking_skill,
                'spice_tolerance': spice_tolerance,
                'dietary_restrictions': dietary_restrictions,
                'health_conditions': health_conditions,
                'allergens': allergens,
                'nutrition_goals': {
                    'calories': target_calories,
                    'protein': target_protein,
                    'carbs': target_carbs,
                    'fat': target_fat
                }
            }
            
            # Save to session state
            st.session_state.user_profile = profile_data
            st.success("Profile saved successfully!")
            
            return profile_data
    
    return None

def display_personalized_recommendations(user_profile: Dict):
    """Display personalized recommendations based on user profile"""
    if not user_profile:
        return
    
    st.subheader("🎯 Your Personalized Recommendations")
    
    profile_manager = UserProfileManager()
    recommendations = profile_manager.get_dietary_recommendations(user_profile)
    nutrition_targets = profile_manager.calculate_nutrition_targets(user_profile)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dietary Recommendations:**")
        for rec in recommendations:
            st.write(f"• {rec}")
    
    with col2:
        st.write("**Your Nutrition Targets:**")
        st.write(f"Calories: {nutrition_targets['calories']} kcal")
        st.write(f"Protein: {nutrition_targets['protein']} g")
        st.write(f"Carbs: {nutrition_targets['carbs']} g")
        st.write(f"Fat: {nutrition_targets['fat']} g")
        st.write(f"Fiber: {nutrition_targets['fiber']} g")
        st.write(f"Sodium: {nutrition_targets['sodium']} mg")

# Example usage
if __name__ == "__main__":
    profile_manager = UserProfileManager()
    personalizer = RecipePersonalizer()
    
    # Example user profile
    user_profile = {
        'dietary_restrictions': ['vegetarian'],
        'health_conditions': ['diabetes'],
        'spice_tolerance': 'mild',
        'cooking_skill': 'beginner',
        'allergens': ['nuts']
    }
    
    # Example recipe
    recipe = {
        'name': 'Spicy Chicken Curry',
        'ingredients': ['chicken breast', 'chili powder', 'nuts', 'milk'],
        'instructions': ['Complex cooking steps...']
    }
    
    # Personalize recipe
    personalized_recipe = personalizer.personalize_recipe(recipe, user_profile)
    print("Personalized recipe:", personalized_recipe)