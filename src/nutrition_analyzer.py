import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class NutritionAnalyzer:
    """Comprehensive nutrition analysis and visualization"""
    
    def __init__(self):
        self.daily_values = self.load_daily_values()
        self.nutrient_categories = self.load_nutrient_categories()
        self.health_targets = self.load_health_targets()
    
    def load_daily_values(self):
        """Load recommended daily values for nutrients"""
        return {
            'calories': {'adult_male': 2500, 'adult_female': 2000, 'child': 1800},
            'protein': {'adult_male': 56, 'adult_female': 46, 'child': 34},  # grams
            'carbs': {'adult_male': 325, 'adult_female': 325, 'child': 260},  # grams
            'fat': {'adult_male': 78, 'adult_female': 65, 'child': 62},  # grams
            'fiber': {'adult_male': 38, 'adult_female': 25, 'child': 25},  # grams
            'sodium': {'adult_male': 2300, 'adult_female': 2300, 'child': 1900},  # mg
            'sugar': {'adult_male': 36, 'adult_female': 25, 'child': 25},  # grams
            'saturated_fat': {'adult_male': 20, 'adult_female': 20, 'child': 18},  # grams
        }
    
    def load_nutrient_categories(self):
        """Load nutrient categories for analysis"""
        return {
            'macronutrients': ['calories', 'protein', 'carbs', 'fat'],
            'micronutrients': ['vitamin_c', 'vitamin_d', 'iron', 'calcium'],
            'limiting_nutrients': ['sodium', 'sugar', 'saturated_fat'],
            'beneficial_nutrients': ['fiber', 'protein', 'omega3']
        }
    
    def load_health_targets(self):
        """Load health-specific nutrition targets"""
        return {
            'diabetes': {
                'carbs': {'max_percent': 45, 'focus': 'complex_carbs'},
                'fiber': {'min': 30},
                'sugar': {'max': 25},
                'glycemic_index': {'preference': 'low'}
            },
            'heart_health': {
                'saturated_fat': {'max_percent': 7},
                'sodium': {'max': 1500},
                'omega3': {'min': 1.1},
                'fiber': {'min': 25}
            },
            'weight_loss': {
                'calories': {'deficit': 500},  # 500 cal below maintenance
                'protein': {'min_percent': 25},
                'fiber': {'min': 30},
                'water_content': {'preference': 'high'}
            },
            'muscle_gain': {
                'protein': {'min': 1.6, 'unit': 'g_per_kg_bodyweight'},
                'calories': {'surplus': 300},
                'carbs': {'timing': 'post_workout'}
            }
        }
    
    def analyze_recipe_nutrition(self, nutrition_data: Dict, user_profile: Dict = None) -> Dict[str, Any]:
        """Comprehensive analysis of recipe nutrition"""
        
        analysis = {
            'nutrition_data': nutrition_data,
            'daily_value_percentages': {},
            'macronutrient_distribution': {},
            'health_scores': {},
            'recommendations': [],
            'warnings': []
        }
        
        # Calculate daily value percentages
        user_category = user_profile.get('category', 'adult_male') if user_profile else 'adult_male'
        
        for nutrient, value in nutrition_data.items():
            if nutrient in self.daily_values:
                daily_value = self.daily_values[nutrient][user_category]
                percentage = (value / daily_value) * 100
                analysis['daily_value_percentages'][nutrient] = round(percentage, 1)
        
        # Calculate macronutrient distribution
        total_calories = nutrition_data.get('calories', 1)
        analysis['macronutrient_distribution'] = {
            'protein_percent': round((nutrition_data.get('protein', 0) * 4 / total_calories) * 100, 1),
            'carbs_percent': round((nutrition_data.get('carbs', 0) * 4 / total_calories) * 100, 1),
            'fat_percent': round((nutrition_data.get('fat', 0) * 9 / total_calories) * 100, 1)
        }
        
        # Calculate health scores
        analysis['health_scores'] = self._calculate_health_scores(nutrition_data)
        
        # Generate recommendations and warnings
        analysis['recommendations'], analysis['warnings'] = self._generate_recommendations(
            nutrition_data, analysis['daily_value_percentages'], user_profile
        )
        
        return analysis
    
    def _calculate_health_scores(self, nutrition_data: Dict) -> Dict[str, float]:
        """Calculate various health scores for the recipe"""
        scores = {}
        
        # Nutrient density score (nutrients per calorie)
        calories = nutrition_data.get('calories', 1)
        protein = nutrition_data.get('protein', 0)
        fiber = nutrition_data.get('fiber', 0)
        
        scores['nutrient_density'] = min(100, ((protein + fiber * 2) / calories) * 100)
        
        # Heart health score
        sodium = nutrition_data.get('sodium', 0)
        saturated_fat = nutrition_data.get('saturated_fat', nutrition_data.get('fat', 0) * 0.3)
        
        heart_score = 100
        if sodium > 600:
            heart_score -= (sodium - 600) / 20
        if saturated_fat > 10:
            heart_score -= (saturated_fat - 10) * 5
        
        scores['heart_health'] = max(0, min(100, heart_score))
        
        # Weight management score
        calorie_density = calories / 100  # calories per 100g (estimated)
        fiber_bonus = min(20, fiber * 2)
        protein_bonus = min(30, protein)
        
        scores['weight_management'] = max(0, min(100, 100 - calorie_density + fiber_bonus + protein_bonus - 50))
        
        # Diabetes-friendly score
        carbs = nutrition_data.get('carbs', 0)
        sugar = nutrition_data.get('sugar', carbs * 0.2)  # estimate if not provided
        
        diabetes_score = 100
        if carbs > 30:
            diabetes_score -= (carbs - 30) * 2
        if sugar > 10:
            diabetes_score -= (sugar - 10) * 5
        diabetes_score += fiber * 3  # fiber bonus
        
        scores['diabetes_friendly'] = max(0, min(100, diabetes_score))
        
        return {k: round(v, 1) for k, v in scores.items()}
    
    def _generate_recommendations(self, nutrition_data: Dict, dv_percentages: Dict, 
                                 user_profile: Dict = None) -> Tuple[List[str], List[str]]:
        """Generate personalized recommendations and warnings"""
        recommendations = []
        warnings = []
        
        # Calorie recommendations
        calories = nutrition_data.get('calories', 0)
        if calories < 200:
            recommendations.append("Consider adding healthy fats or complex carbs to increase calorie content")
        elif calories > 600:
            recommendations.append("This is a high-calorie recipe - consider reducing portion size or balancing with lighter meals")
        
        # Protein recommendations
        protein_percent = dv_percentages.get('protein', 0)
        if protein_percent > 30:
            recommendations.append("Excellent protein source! Great for muscle maintenance and satiety")
        elif protein_percent < 10:
            recommendations.append("Consider adding protein sources like beans, nuts, or lean meat")
        
        # Fiber recommendations
        fiber = nutrition_data.get('fiber', 0)
        if fiber > 10:
            recommendations.append("High fiber content promotes digestive health and satiety")
        elif fiber < 3:
            recommendations.append("Consider adding vegetables, fruits, or whole grains for more fiber")
        
        # Sodium warnings
        sodium_percent = dv_percentages.get('sodium', 0)
        if sodium_percent > 25:
            warnings.append("High sodium content - consider reducing salt or using herbs and spices")
        
        # Fat analysis
        fat = nutrition_data.get('fat', 0)
        if fat > 25:
            warnings.append("High fat content - ensure they're healthy fats from sources like olive oil, nuts, or avocado")
        
        # User-specific recommendations
        if user_profile:
            health_goals = user_profile.get('health_goals', [])
            
            if 'weight_loss' in health_goals:
                if calories > 400:
                    recommendations.append("For weight loss, consider reducing portion size or adding more vegetables")
            
            if 'diabetes' in health_goals:
                carbs = nutrition_data.get('carbs', 0)
                if carbs > 45:
                    warnings.append("High carbohydrate content - monitor blood sugar if diabetic")
            
            if 'heart_health' in health_goals:
                sodium = nutrition_data.get('sodium', 0)
                if sodium > 400:
                    warnings.append("Consider reducing sodium for better heart health")
        
        return recommendations, warnings
    
    def create_nutrition_visualizations(self, nutrition_data: Dict, analysis: Dict) -> Dict[str, go.Figure]:
        """Create comprehensive nutrition visualizations"""
        figures = {}
        
        # 1. Macronutrient pie chart
        macro_dist = analysis['macronutrient_distribution']
        figures['macronutrients'] = px.pie(
            values=[macro_dist['protein_percent'], macro_dist['carbs_percent'], macro_dist['fat_percent']],
            names=['Protein', 'Carbohydrates', 'Fat'],
            title="Macronutrient Distribution",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        
        # 2. Daily value percentages bar chart
        dv_data = analysis['daily_value_percentages']
        nutrients = list(dv_data.keys())
        percentages = list(dv_data.values())
        
        colors = ['green' if p <= 100 else 'orange' if p <= 150 else 'red' for p in percentages]
        
        figures['daily_values'] = go.Figure(data=[
            go.Bar(x=nutrients, y=percentages, marker_color=colors)
        ])
        figures['daily_values'].update_layout(
            title="Percentage of Daily Values",
            xaxis_title="Nutrients",
            yaxis_title="% Daily Value",
            showlegend=False
        )
        figures['daily_values'].add_hline(y=100, line_dash="dash", line_color="red")
        
        # 3. Health scores radar chart
        health_scores = analysis['health_scores']
        categories = list(health_scores.keys())
        scores = list(health_scores.values())
        
        figures['health_scores'] = go.Figure()
        figures['health_scores'].add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name='Health Scores'
        ))
        figures['health_scores'].update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Health Score Analysis"
        )
        
        # 4. Nutrient comparison chart
        key_nutrients = ['protein', 'fiber', 'sodium', 'fat']
        nutrient_values = [nutrition_data.get(n, 0) for n in key_nutrients]
        
        figures['nutrients'] = go.Figure(data=[
            go.Bar(x=key_nutrients, y=nutrient_values, marker_color='#66D9EF')
        ])
        figures['nutrients'].update_layout(
            title="Key Nutrient Content",
            xaxis_title="Nutrients",
            yaxis_title="Amount (g or mg)"
        )
        
        return figures
    
    def compare_recipes(self, recipes_nutrition: List[Dict], recipe_names: List[str]) -> Dict[str, Any]:
        """Compare nutrition across multiple recipes"""
        comparison = {
            'recipes': recipe_names,
            'nutrition_comparison': {},
            'rankings': {},
            'recommendations': []
        }
        
        # Compare each nutrient across recipes
        all_nutrients = set()
        for nutrition in recipes_nutrition:
            all_nutrients.update(nutrition.keys())
        
        for nutrient in all_nutrients:
            values = [nutrition.get(nutrient, 0) for nutrition in recipes_nutrition]
            comparison['nutrition_comparison'][nutrient] = values
        
        # Rank recipes by different criteria
        comparison['rankings'] = {
            'lowest_calorie': self._rank_recipes(recipes_nutrition, 'calories', ascending=True),
            'highest_protein': self._rank_recipes(recipes_nutrition, 'protein', ascending=False),
            'highest_fiber': self._rank_recipes(recipes_nutrition, 'fiber', ascending=False),
            'lowest_sodium': self._rank_recipes(recipes_nutrition, 'sodium', ascending=True)
        }
        
        return comparison
    
    def _rank_recipes(self, recipes_nutrition: List[Dict], criteria: str, ascending: bool = True) -> List[int]:
        """Rank recipes based on a specific nutritional criteria"""
        values = [(i, nutrition.get(criteria, 0)) for i, nutrition in enumerate(recipes_nutrition)]
        sorted_values = sorted(values, key=lambda x: x[1], reverse=not ascending)
        return [i for i, _ in sorted_values]
    
    def get_meal_plan_nutrition(self, daily_recipes: List[Dict]) -> Dict[str, Any]:
        """Calculate cumulative nutrition for a day's meal plan"""
        total_nutrition = {}
        
        # Sum up all nutrients
        for recipe_nutrition in daily_recipes:
            for nutrient, value in recipe_nutrition.items():
                total_nutrition[nutrient] = total_nutrition.get(nutrient, 0) + value
        
        # Analyze daily totals
        daily_analysis = self.analyze_recipe_nutrition(total_nutrition)
        daily_analysis['meal_count'] = len(daily_recipes)
        daily_analysis['average_calories_per_meal'] = total_nutrition.get('calories', 0) / len(daily_recipes)
        
        return daily_analysis
    
    def suggest_recipe_modifications(self, nutrition_data: Dict, target_goals: List[str]) -> List[Dict[str, str]]:
        """Suggest specific recipe modifications to meet health goals"""
        modifications = []
        
        for goal in target_goals:
            if goal == 'reduce_sodium':
                if nutrition_data.get('sodium', 0) > 400:
                    modifications.append({
                        'goal': 'Reduce Sodium',
                        'current': f"{nutrition_data.get('sodium', 0)}mg",
                        'suggestion': 'Use herbs and spices instead of salt, rinse canned ingredients',
                        'impact': 'Reduces sodium by 30-50%'
                    })
            
            elif goal == 'increase_protein':
                if nutrition_data.get('protein', 0) < 15:
                    modifications.append({
                        'goal': 'Increase Protein',
                        'current': f"{nutrition_data.get('protein', 0)}g",
                        'suggestion': 'Add beans, nuts, Greek yogurt, or lean meat',
                        'impact': 'Can add 10-20g protein'
                    })
            
            elif goal == 'reduce_calories':
                if nutrition_data.get('calories', 0) > 400:
                    modifications.append({
                        'goal': 'Reduce Calories',
                        'current': f"{nutrition_data.get('calories', 0)} cal",
                        'suggestion': 'Reduce oil, use cooking spray, increase vegetables',
                        'impact': 'Can reduce by 100-200 calories'
                    })
            
            elif goal == 'increase_fiber':
                if nutrition_data.get('fiber', 0) < 5:
                    modifications.append({
                        'goal': 'Increase Fiber',
                        'current': f"{nutrition_data.get('fiber', 0)}g",
                        'suggestion': 'Add vegetables, switch to whole grains, include beans',
                        'impact': 'Can add 5-10g fiber'
                    })
        
        return modifications

# Example usage
if __name__ == "__main__":
    analyzer = NutritionAnalyzer()
    
    # Example recipe nutrition
    sample_nutrition = {
        'calories': 420,
        'protein': 18,
        'carbs': 58,
        'fat': 14,
        'fiber': 12,
        'sodium': 380
    }
    
    # Analyze nutrition
    analysis = analyzer.analyze_recipe_nutrition(sample_nutrition)
    print("Nutrition Analysis:", analysis)
    
    # Create visualizations
    figures = analyzer.create_nutrition_visualizations(sample_nutrition, analysis)
    print("Generated visualizations:", list(figures.keys()))