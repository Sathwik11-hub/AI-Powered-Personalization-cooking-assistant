import json
import pandas as pd
from datetime import datetime

class RecipeDatabase:
    """Extended recipe database with more recipes and functionality"""
    
    def __init__(self):
        self.recipes = self.load_extended_recipes()
        self.substitutions = self.load_substitutions()
        self.user_interactions = []
    
    def load_extended_recipes(self):
        """Load comprehensive recipe database"""
        return [
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
                'image_description': 'colorful quinoa bowl with vegetables',
                'season': 'all',
                'budget_level': 'medium'
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
                'image_description': 'grilled chicken breast with herbs',
                'season': 'summer',
                'budget_level': 'medium'
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
                'image_description': 'colorful vegetable stir fry in wok',
                'season': 'all',
                'budget_level': 'low'
            },
            {
                'id': 4,
                'name': 'Spicy Lentil Curry',
                'cuisine': 'Indian',
                'ingredients': ['red lentils', 'onion', 'tomatoes', 'ginger', 'garlic', 'turmeric', 'cumin', 'coriander', 'coconut milk', 'chili'],
                'instructions': [
                    'Rinse lentils and set aside',
                    'Heat oil and sauté onions until golden',
                    'Add ginger, garlic, and spices',
                    'Add tomatoes and cook until soft',
                    'Add lentils and water, bring to boil',
                    'Simmer for 20-25 minutes until lentils are soft',
                    'Stir in coconut milk and chili, simmer 5 more minutes'
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
                'dietary_tags': ['vegetarian', 'vegan', 'high-fiber', 'high-protein', 'spicy'],
                'health_conditions': ['diabetes-friendly', 'heart-healthy'],
                'image_description': 'creamy red lentil curry with spices',
                'season': 'winter',
                'budget_level': 'low'
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
                'image_description': 'baked salmon fillet with dill and lemon',
                'season': 'all',
                'budget_level': 'high'
            },
            {
                'id': 6,
                'name': 'Avocado Toast with Egg',
                'cuisine': 'American',
                'ingredients': ['whole grain bread', 'avocado', 'egg', 'lime', 'salt', 'pepper', 'red pepper flakes'],
                'instructions': [
                    'Toast bread until golden brown',
                    'Mash avocado with lime juice, salt, and pepper',
                    'Fry or poach egg to desired doneness',
                    'Spread avocado mixture on toast',
                    'Top with egg',
                    'Sprinkle with red pepper flakes'
                ],
                'cooking_time': 10,
                'difficulty': 'Easy',
                'servings': 1,
                'nutrition': {
                    'calories': 340,
                    'protein': 14,
                    'carbs': 28,
                    'fat': 22,
                    'fiber': 12,
                    'sodium': 320
                },
                'dietary_tags': ['vegetarian', 'high-fiber', 'healthy-fats'],
                'health_conditions': ['heart-healthy', 'weight-loss'],
                'image_description': 'avocado toast topped with fried egg',
                'season': 'all',
                'budget_level': 'medium'
            },
            {
                'id': 7,
                'name': 'Thai Green Curry',
                'cuisine': 'Thai',
                'ingredients': ['chicken breast', 'green curry paste', 'coconut milk', 'thai basil', 'eggplant', 'bamboo shoots', 'fish sauce', 'palm sugar'],
                'instructions': [
                    'Heat coconut milk in a wok until oil separates',
                    'Add green curry paste and fry until fragrant',
                    'Add chicken and cook until almost done',
                    'Add vegetables and remaining coconut milk',
                    'Season with fish sauce and palm sugar',
                    'Simmer until vegetables are tender',
                    'Garnish with thai basil'
                ],
                'cooking_time': 30,
                'difficulty': 'Medium',
                'servings': 4,
                'nutrition': {
                    'calories': 380,
                    'protein': 28,
                    'carbs': 12,
                    'fat': 26,
                    'fiber': 4,
                    'sodium': 720
                },
                'dietary_tags': ['spicy', 'high-protein', 'gluten-free'],
                'health_conditions': ['diabetes-friendly'],
                'image_description': 'green curry with chicken and vegetables',
                'season': 'all',
                'budget_level': 'medium'
            },
            {
                'id': 8,
                'name': 'Greek Salad',
                'cuisine': 'Greek',
                'ingredients': ['tomatoes', 'cucumber', 'red onion', 'olives', 'feta cheese', 'olive oil', 'oregano', 'lemon juice'],
                'instructions': [
                    'Chop tomatoes, cucumber, and red onion',
                    'Combine vegetables in a large bowl',
                    'Add olives and crumbled feta cheese',
                    'Drizzle with olive oil and lemon juice',
                    'Season with oregano, salt, and pepper',
                    'Toss gently and let marinate for 10 minutes'
                ],
                'cooking_time': 15,
                'difficulty': 'Easy',
                'servings': 4,
                'nutrition': {
                    'calories': 180,
                    'protein': 6,
                    'carbs': 12,
                    'fat': 14,
                    'fiber': 4,
                    'sodium': 420
                },
                'dietary_tags': ['vegetarian', 'gluten-free', 'low-calorie', 'mediterranean'],
                'health_conditions': ['heart-healthy', 'weight-loss'],
                'image_description': 'fresh greek salad with feta and olives',
                'season': 'summer',
                'budget_level': 'medium'
            },
            {
                'id': 9,
                'name': 'Mushroom Risotto',
                'cuisine': 'Italian',
                'ingredients': ['arborio rice', 'mushrooms', 'onion', 'garlic', 'white wine', 'vegetable broth', 'parmesan', 'butter'],
                'instructions': [
                    'Sauté mushrooms and set aside',
                    'Heat broth in a separate pan',
                    'Sauté onion and garlic until soft',
                    'Add rice and stir for 2 minutes',
                    'Add wine and stir until absorbed',
                    'Add warm broth one ladle at a time, stirring constantly',
                    'Fold in mushrooms, butter, and parmesan'
                ],
                'cooking_time': 45,
                'difficulty': 'Hard',
                'servings': 4,
                'nutrition': {
                    'calories': 420,
                    'protein': 12,
                    'carbs': 65,
                    'fat': 14,
                    'fiber': 3,
                    'sodium': 480
                },
                'dietary_tags': ['vegetarian', 'comfort-food'],
                'health_conditions': [],
                'image_description': 'creamy mushroom risotto with parmesan',
                'season': 'fall',
                'budget_level': 'high'
            },
            {
                'id': 10,
                'name': 'Black Bean Tacos',
                'cuisine': 'Mexican',
                'ingredients': ['black beans', 'corn tortillas', 'avocado', 'lime', 'cilantro', 'red onion', 'cumin', 'chili powder'],
                'instructions': [
                    'Heat black beans with cumin and chili powder',
                    'Warm tortillas in a dry pan',
                    'Mash avocado with lime juice',
                    'Dice red onion and chop cilantro',
                    'Fill tortillas with beans',
                    'Top with avocado, onion, and cilantro',
                    'Serve with lime wedges'
                ],
                'cooking_time': 20,
                'difficulty': 'Easy',
                'servings': 3,
                'nutrition': {
                    'calories': 320,
                    'protein': 14,
                    'carbs': 52,
                    'fat': 8,
                    'fiber': 16,
                    'sodium': 380
                },
                'dietary_tags': ['vegetarian', 'vegan', 'high-fiber', 'gluten-free'],
                'health_conditions': ['diabetes-friendly', 'heart-healthy', 'weight-loss'],
                'image_description': 'black bean tacos with avocado and cilantro',
                'season': 'all',
                'budget_level': 'low'
            }
        ]
    
    def load_substitutions(self):
        """Load ingredient substitution database"""
        return {
            'quinoa': ['brown rice', 'bulgur wheat', 'cauliflower rice', 'farro'],
            'chicken breast': ['turkey breast', 'tofu', 'tempeh', 'seitan'],
            'feta cheese': ['goat cheese', 'cottage cheese', 'nutritional yeast', 'ricotta'],
            'olive oil': ['avocado oil', 'coconut oil', 'vegetable broth', 'butter'],
            'soy sauce': ['tamari', 'coconut aminos', 'balsamic vinegar', 'worcestershire sauce'],
            'coconut milk': ['cashew cream', 'almond milk', 'heavy cream', 'oat milk'],
            'salmon': ['tuna', 'mackerel', 'chicken breast', 'tofu'],
            'lentils': ['chickpeas', 'black beans', 'quinoa', 'split peas'],
            'eggs': ['flax eggs', 'chia eggs', 'applesauce', 'banana'],
            'butter': ['olive oil', 'coconut oil', 'applesauce', 'avocado'],
            'milk': ['almond milk', 'oat milk', 'coconut milk', 'soy milk'],
            'flour': ['almond flour', 'coconut flour', 'oat flour', 'rice flour'],
            'sugar': ['honey', 'maple syrup', 'stevia', 'monk fruit'],
            'breadcrumbs': ['crushed nuts', 'oat flour', 'panko', 'cornmeal'],
            'cream': ['coconut cream', 'cashew cream', 'greek yogurt', 'silken tofu']
        }
    
    def get_recipes_by_criteria(self, **criteria):
        """Filter recipes based on multiple criteria"""
        filtered_recipes = self.recipes.copy()
        
        for key, value in criteria.items():
            if value and key in ['cuisine', 'difficulty', 'season']:
                filtered_recipes = [r for r in filtered_recipes if r.get(key) == value]
            elif value and key == 'max_time':
                filtered_recipes = [r for r in filtered_recipes if r.get('cooking_time', 0) <= value]
            elif value and key == 'dietary_tags':
                filtered_recipes = [r for r in filtered_recipes if any(tag in r.get('dietary_tags', []) for tag in value)]
            elif value and key == 'health_conditions':
                filtered_recipes = [r for r in filtered_recipes if any(condition in r.get('health_conditions', []) for condition in value)]
        
        return filtered_recipes
    
    def log_user_interaction(self, user_id, recipe_id, interaction_type, rating=None):
        """Log user interactions for adaptive learning"""
        interaction = {
            'user_id': user_id,
            'recipe_id': recipe_id,
            'interaction_type': interaction_type,  # 'view', 'cook', 'favorite', 'rate'
            'rating': rating,
            'timestamp': datetime.now().isoformat()
        }
        self.user_interactions.append(interaction)
    
    def get_personalized_recommendations(self, user_id, limit=5):
        """Get personalized recipe recommendations based on user history"""
        user_interactions = [i for i in self.user_interactions if i['user_id'] == user_id]
        
        if not user_interactions:
            # Return popular recipes for new users
            return self.recipes[:limit]
        
        # Simple recommendation based on past preferences
        preferred_cuisines = []
        preferred_dietary_tags = []
        
        for interaction in user_interactions:
            if interaction['rating'] and interaction['rating'] >= 4:
                recipe = next((r for r in self.recipes if r['id'] == interaction['recipe_id']), None)
                if recipe:
                    preferred_cuisines.append(recipe['cuisine'])
                    preferred_dietary_tags.extend(recipe['dietary_tags'])
        
        # Find similar recipes
        recommendations = []
        for recipe in self.recipes:
            score = 0
            if recipe['cuisine'] in preferred_cuisines:
                score += 2
            if any(tag in preferred_dietary_tags for tag in recipe['dietary_tags']):
                score += 1
            recipe['recommendation_score'] = score
        
        # Sort by score and return top recommendations
        sorted_recipes = sorted(self.recipes, key=lambda x: x.get('recommendation_score', 0), reverse=True)
        return sorted_recipes[:limit]

# Usage example
if __name__ == "__main__":
    db = RecipeDatabase()
    
    # Example queries
    vegetarian_recipes = db.get_recipes_by_criteria(dietary_tags=['vegetarian'])
    quick_recipes = db.get_recipes_by_criteria(max_time=20)
    
    print(f"Found {len(vegetarian_recipes)} vegetarian recipes")
    print(f"Found {len(quick_recipes)} quick recipes")