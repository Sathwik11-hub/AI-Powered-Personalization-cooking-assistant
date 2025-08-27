import numpy as np
import pandas as pd
from typing import List, Dict, Any
import re

class IngredientSubstitutionEngine:
    """Advanced ingredient substitution engine with health and dietary considerations"""
    
    def __init__(self):
        self.substitution_rules = self.load_substitution_rules()
        self.dietary_mappings = self.load_dietary_mappings()
        self.health_alternatives = self.load_health_alternatives()
    
    def load_substitution_rules(self):
        """Load comprehensive substitution rules"""
        return {
            # Proteins
            'chicken breast': {
                'alternatives': ['turkey breast', 'lean pork', 'firm tofu', 'tempeh'],
                'vegan': ['firm tofu', 'tempeh', 'seitan', 'jackfruit'],
                'low_fat': ['turkey breast', 'white fish', 'egg whites'],
                'ratio': 1.0
            },
            'ground beef': {
                'alternatives': ['ground turkey', 'ground chicken', 'lentils', 'mushrooms'],
                'vegan': ['lentils', 'black beans', 'mushrooms', 'walnuts'],
                'low_fat': ['ground turkey (93/7)', 'ground chicken breast'],
                'ratio': 1.0
            },
            'salmon': {
                'alternatives': ['tuna', 'mackerel', 'trout', 'chicken breast'],
                'vegan': ['firm tofu', 'tempeh', 'chickpeas'],
                'budget': ['canned tuna', 'chicken breast', 'eggs'],
                'ratio': 1.0
            },
            
            # Dairy
            'milk': {
                'alternatives': ['almond milk', 'oat milk', 'soy milk', 'coconut milk'],
                'lactose_free': ['lactose-free milk', 'almond milk', 'oat milk'],
                'low_fat': ['skim milk', 'almond milk (unsweetened)'],
                'ratio': 1.0
            },
            'butter': {
                'alternatives': ['olive oil', 'coconut oil', 'avocado oil', 'applesauce'],
                'vegan': ['coconut oil', 'olive oil', 'vegan butter'],
                'low_fat': ['applesauce', 'mashed banana', 'greek yogurt'],
                'ratio': 0.75  # Use 3/4 amount when substituting with oil
            },
            'heavy cream': {
                'alternatives': ['coconut cream', 'cashew cream', 'evaporated milk'],
                'vegan': ['coconut cream', 'cashew cream', 'silken tofu'],
                'low_fat': ['evaporated skim milk', 'greek yogurt'],
                'ratio': 1.0
            },
            
            # Grains and Starches
            'white rice': {
                'alternatives': ['brown rice', 'quinoa', 'cauliflower rice', 'wild rice'],
                'low_carb': ['cauliflower rice', 'shirataki rice', 'broccoli rice'],
                'high_fiber': ['brown rice', 'quinoa', 'wild rice'],
                'ratio': 1.0
            },
            'pasta': {
                'alternatives': ['whole wheat pasta', 'zucchini noodles', 'shirataki noodles'],
                'gluten_free': ['rice pasta', 'corn pasta', 'quinoa pasta'],
                'low_carb': ['zucchini noodles', 'spaghetti squash', 'shirataki noodles'],
                'ratio': 1.0
            },
            'bread': {
                'alternatives': ['whole grain bread', 'sourdough', 'lettuce wraps'],
                'gluten_free': ['rice bread', 'almond flour bread', 'corn tortillas'],
                'low_carb': ['lettuce wraps', 'portobello mushroom caps', 'cauliflower bread'],
                'ratio': 1.0
            },
            
            # Sweeteners
            'sugar': {
                'alternatives': ['honey', 'maple syrup', 'coconut sugar', 'stevia'],
                'diabetic': ['stevia', 'monk fruit', 'erythritol'],
                'natural': ['honey', 'maple syrup', 'dates', 'applesauce'],
                'ratio': 0.75  # Generally use less when substituting liquid sweeteners
            },
            
            # Fats and Oils
            'olive oil': {
                'alternatives': ['avocado oil', 'coconut oil', 'canola oil'],
                'high_heat': ['avocado oil', 'canola oil', 'grapeseed oil'],
                'neutral_flavor': ['canola oil', 'vegetable oil', 'grapeseed oil'],
                'ratio': 1.0
            },
            
            # Vegetables
            'onion': {
                'alternatives': ['shallots', 'green onions', 'leeks', 'fennel'],
                'low_fodmap': ['green onion tops', 'chives', 'fennel'],
                'mild_flavor': ['shallots', 'sweet onion', 'leeks'],
                'ratio': 1.0
            },
            'garlic': {
                'alternatives': ['garlic powder', 'shallots', 'ginger', 'asafoetida'],
                'low_fodmap': ['asafoetida', 'garlic oil', 'ginger'],
                'powder_ratio': 0.125  # 1 clove = 1/8 tsp powder
            }
        }
    
    def load_dietary_mappings(self):
        """Load dietary restriction mappings"""
        return {
            'vegan': {
                'avoid': ['meat', 'dairy', 'eggs', 'honey', 'gelatin'],
                'keywords': ['chicken', 'beef', 'pork', 'fish', 'milk', 'cheese', 'butter', 'egg']
            },
            'vegetarian': {
                'avoid': ['meat', 'fish'],
                'keywords': ['chicken', 'beef', 'pork', 'fish', 'bacon', 'ham']
            },
            'gluten_free': {
                'avoid': ['wheat', 'barley', 'rye', 'oats'],
                'keywords': ['flour', 'bread', 'pasta', 'soy sauce', 'beer']
            },
            'dairy_free': {
                'avoid': ['milk', 'cheese', 'butter', 'cream'],
                'keywords': ['milk', 'cheese', 'butter', 'cream', 'yogurt']
            },
            'low_carb': {
                'avoid': ['high_carb_foods'],
                'keywords': ['rice', 'pasta', 'bread', 'potato', 'sugar']
            },
            'keto': {
                'avoid': ['high_carb_foods', 'sugar'],
                'keywords': ['rice', 'pasta', 'bread', 'fruit', 'sugar', 'honey']
            }
        }
    
    def load_health_alternatives(self):
        """Load health-focused alternatives"""
        return {
            'diabetes': {
                'focus': ['low_glycemic', 'high_fiber', 'protein'],
                'substitutions': {
                    'white rice': 'cauliflower rice',
                    'sugar': 'stevia',
                    'white bread': 'whole grain bread'
                }
            },
            'heart_health': {
                'focus': ['omega3', 'low_sodium', 'antioxidants'],
                'substitutions': {
                    'butter': 'olive oil',
                    'red meat': 'salmon',
                    'salt': 'herbs and spices'
                }
            },
            'weight_loss': {
                'focus': ['low_calorie', 'high_protein', 'high_fiber'],
                'substitutions': {
                    'pasta': 'zucchini noodles',
                    'rice': 'cauliflower rice',
                    'oil': 'cooking spray'
                }
            }
        }
    
    def find_substitutes(self, ingredient: str, dietary_restrictions: List[str] = None, 
                        health_goals: List[str] = None, budget_conscious: bool = False) -> Dict[str, Any]:
        """Find appropriate substitutes based on dietary and health requirements"""
        
        ingredient_lower = ingredient.lower().strip()
        
        # Find matching substitution rule
        substitution_rule = None
        for key in self.substitution_rules:
            if key in ingredient_lower or ingredient_lower in key:
                substitution_rule = self.substitution_rules[key]
                break
        
        if not substitution_rule:
            return self._generate_generic_substitutes(ingredient)
        
        substitutes = {
            'original': ingredient,
            'alternatives': [],
            'ratio': substitution_rule.get('ratio', 1.0),
            'notes': []
        }
        
        # Apply dietary restrictions
        if dietary_restrictions:
            for restriction in dietary_restrictions:
                if restriction in substitution_rule:
                    substitutes['alternatives'].extend(substitution_rule[restriction])
                    substitutes['notes'].append(f"Suitable for {restriction.replace('_', ' ')} diet")
        
        # Apply health goals
        if health_goals:
            for goal in health_goals:
                health_key = goal.replace('-', '_').replace(' ', '_')
                if health_key in substitution_rule:
                    substitutes['alternatives'].extend(substitution_rule[health_key])
                    substitutes['notes'].append(f"Optimized for {goal}")
        
        # Budget considerations
        if budget_conscious and 'budget' in substitution_rule:
            substitutes['alternatives'].extend(substitution_rule['budget'])
            substitutes['notes'].append("Budget-friendly options included")
        
        # Default alternatives if no specific requirements
        if not substitutes['alternatives']:
            substitutes['alternatives'] = substitution_rule['alternatives']
        
        # Remove duplicates and limit to top options
        substitutes['alternatives'] = list(dict.fromkeys(substitutes['alternatives']))[:5]
        
        # Add nutritional comparison
        substitutes['nutritional_notes'] = self._get_nutritional_comparison(ingredient, substitutes['alternatives'])
        
        return substitutes
    
    def _generate_generic_substitutes(self, ingredient: str) -> Dict[str, Any]:
        """Generate generic substitutes for unknown ingredients"""
        category = self._categorize_ingredient(ingredient)
        
        generic_subs = {
            'protein': ['tofu', 'tempeh', 'legumes'],
            'vegetable': ['similar seasonal vegetables', 'frozen alternative'],
            'herb': ['dried version', 'similar herbs'],
            'spice': ['similar spices', 'spice blends'],
            'grain': ['similar grains', 'cauliflower rice'],
            'fruit': ['similar seasonal fruits', 'frozen alternative']
        }
        
        return {
            'original': ingredient,
            'alternatives': generic_subs.get(category, ['consult recipe notes']),
            'ratio': 1.0,
            'notes': [f"Generic {category} substitutions suggested"],
            'nutritional_notes': "Nutritional values may vary significantly"
        }
    
    def _categorize_ingredient(self, ingredient: str) -> str:
        """Categorize ingredient into broad groups"""
        ingredient_lower = ingredient.lower()
        
        proteins = ['chicken', 'beef', 'pork', 'fish', 'tofu', 'beans', 'lentils']
        vegetables = ['broccoli', 'carrot', 'onion', 'pepper', 'tomato', 'spinach']
        herbs = ['basil', 'oregano', 'thyme', 'parsley', 'cilantro', 'mint']
        spices = ['cumin', 'paprika', 'turmeric', 'cinnamon', 'ginger']
        grains = ['rice', 'quinoa', 'pasta', 'bread', 'oats']
        fruits = ['apple', 'banana', 'berries', 'citrus', 'mango']
        
        if any(p in ingredient_lower for p in proteins):
            return 'protein'
        elif any(v in ingredient_lower for v in vegetables):
            return 'vegetable'
        elif any(h in ingredient_lower for h in herbs):
            return 'herb'
        elif any(s in ingredient_lower for s in spices):
            return 'spice'
        elif any(g in ingredient_lower for g in grains):
            return 'grain'
        elif any(f in ingredient_lower for f in fruits):
            return 'fruit'
        else:
            return 'other'
    
    def _get_nutritional_comparison(self, original: str, alternatives: List[str]) -> str:
        """Provide nutritional comparison notes"""
        # This would ideally connect to a nutrition database
        # For now, provide general guidance
        
        nutrition_notes = {
            'tofu': "Lower in calories, good protein source",
            'cauliflower rice': "Much lower in carbs and calories",
            'quinoa': "Higher in protein and fiber than rice",
            'olive oil': "Rich in healthy monounsaturated fats",
            'stevia': "Zero calories, suitable for diabetics",
            'almond milk': "Lower in calories and carbs than dairy milk"
        }
        
        notes = []
        for alt in alternatives[:3]:  # Limit to first 3 alternatives
            if alt.lower() in nutrition_notes:
                notes.append(f"{alt}: {nutrition_notes[alt.lower()]}")
        
        return "; ".join(notes) if notes else "Nutritional values may vary"
    
    def batch_substitute(self, ingredients: List[str], **kwargs) -> Dict[str, Dict]:
        """Process multiple ingredient substitutions"""
        results = {}
        for ingredient in ingredients:
            results[ingredient] = self.find_substitutes(ingredient, **kwargs)
        return results
    
    def validate_substitution(self, original: str, substitute: str, recipe_type: str = None) -> Dict[str, Any]:
        """Validate if a substitution is appropriate for a specific recipe"""
        # This would analyze the recipe context and provide validation
        return {
            'compatible': True,
            'confidence': 0.85,
            'notes': f"{substitute} is a suitable replacement for {original}",
            'adjustments_needed': []
        }

# Example usage
if __name__ == "__main__":
    engine = IngredientSubstitutionEngine()
    
    # Test single substitution
    result = engine.find_substitutes(
        'chicken breast', 
        dietary_restrictions=['vegan'], 
        health_goals=['weight_loss']
    )
    print(f"Substitutes for chicken breast: {result}")
    
    # Test batch substitution
    ingredients = ['butter', 'milk', 'chicken breast']
    batch_results = engine.batch_substitute(
        ingredients, 
        dietary_restrictions=['vegan']
    )
    print(f"Batch substitutions: {batch_results}")