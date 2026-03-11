import json
from datetime import datetime, timedelta
import random

def generate_demo_data():
    """Generate demo data for the cooking assistant"""
    
    # Sample user interactions for demo
    demo_interactions = [
        {
            "user_id": "demo_user_1",
            "recipe_id": 1,
            "interaction_type": "view",
            "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
            "rating": None
        },
        {
            "user_id": "demo_user_1", 
            "recipe_id": 1,
            "interaction_type": "cook",
            "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
            "rating": None
        },
        {
            "user_id": "demo_user_1",
            "recipe_id": 1,
            "interaction_type": "rate",
            "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
            "rating": 5
        },
        {
            "user_id": "demo_user_1",
            "recipe_id": 3,
            "interaction_type": "view",
            "timestamp": (datetime.now() - timedelta(days=3)).isoformat(),
            "rating": None
        },
        {
            "user_id": "demo_user_1",
            "recipe_id": 3,
            "interaction_type": "cook",
            "timestamp": (datetime.now() - timedelta(days=3)).isoformat(),
            "rating": None
        },
        {
            "user_id": "demo_user_1",
            "recipe_id": 3,
            "interaction_type": "rate",
            "timestamp": (datetime.now() - timedelta(days=3)).isoformat(),
            "rating": 4
        }
    ]
    
    # Sample meal plans
    demo_meal_plans = [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "meals": {
                "breakfast": {
                    "recipe_id": 6,
                    "recipe_name": "Avocado Toast with Egg",
                    "calories": 340
                },
                "lunch": {
                    "recipe_id": 1,
                    "recipe_name": "Mediterranean Quinoa Bowl", 
                    "calories": 420
                },
                "dinner": {
                    "recipe_id": 5,
                    "recipe_name": "Baked Salmon with Dill",
                    "calories": 367
                }
            },
            "total_calories": 1127,
            "nutritional_goals_met": True
        }
    ]
    
    # Sample cooking achievements
    demo_achievements = [
        {
            "achievement_id": "first_recipe",
            "name": "First Recipe Cooked!",
            "description": "Congratulations on cooking your first recipe",
            "icon": "🍳",
            "unlocked": True,
            "unlock_date": (datetime.now() - timedelta(days=5)).isoformat()
        },
        {
            "achievement_id": "vegetarian_week",
            "name": "Vegetarian Week",
            "description": "Cooked vegetarian meals for 7 days straight",
            "icon": "🥬",
            "unlocked": False,
            "progress": 3,
            "target": 7
        },
        {
            "achievement_id": "healthy_choice",
            "name": "Healthy Choice Champion",
            "description": "Chose healthy recipes 10 times",
            "icon": "💚",
            "unlocked": False,
            "progress": 6,
            "target": 10
        }
    ]
    
    # Sample ingredient inventory
    demo_inventory = {
        "vegetables": [
            {"name": "tomatoes", "quantity": 4, "unit": "pieces", "expiry": "2024-01-15"},
            {"name": "onion", "quantity": 2, "unit": "pieces", "expiry": "2024-01-20"},
            {"name": "bell peppers", "quantity": 3, "unit": "pieces", "expiry": "2024-01-12"},
            {"name": "spinach", "quantity": 1, "unit": "bag", "expiry": "2024-01-10"}
        ],
        "proteins": [
            {"name": "chicken breast", "quantity": 2, "unit": "lbs", "expiry": "2024-01-08"},
            {"name": "salmon fillet", "quantity": 4, "unit": "pieces", "expiry": "2024-01-09"},
            {"name": "eggs", "quantity": 12, "unit": "pieces", "expiry": "2024-01-18"}
        ],
        "pantry": [
            {"name": "quinoa", "quantity": 2, "unit": "cups", "expiry": "2024-06-01"},
            {"name": "olive oil", "quantity": 1, "unit": "bottle", "expiry": "2024-12-01"},
            {"name": "garlic", "quantity": 1, "unit": "bulb", "expiry": "2024-02-01"}
        ]
    }
    
    # Sample seasonal ingredients
    current_month = datetime.now().month
    seasonal_ingredients = {
        "winter": ["root vegetables", "citrus fruits", "hearty greens", "squash"],
        "spring": ["asparagus", "peas", "fresh herbs", "strawberries"],
        "summer": ["tomatoes", "zucchini", "berries", "stone fruits"],
        "fall": ["apples", "pumpkin", "brussels sprouts", "cranberries"]
    }
    
    season = ["winter", "winter", "spring", "spring", "spring", "summer", "summer", 
              "summer", "fall", "fall", "fall", "winter"][current_month - 1]
    
    demo_data = {
        "user_interactions": demo_interactions,
        "meal_plans": demo_meal_plans, 
        "achievements": demo_achievements,
        "inventory": demo_inventory,
        "seasonal_ingredients": seasonal_ingredients[season],
        "current_season": season,
        "generated_at": datetime.now().isoformat()
    }
    
    return demo_data

def get_trending_recipes():
    """Get sample trending recipes data"""
    return [
        {"recipe_id": 1, "name": "Mediterranean Quinoa Bowl", "trend_score": 95},
        {"recipe_id": 3, "name": "Vegetable Stir Fry", "trend_score": 88},
        {"recipe_id": 6, "name": "Avocado Toast with Egg", "trend_score": 82},
        {"recipe_id": 10, "name": "Black Bean Tacos", "trend_score": 79},
        {"recipe_id": 5, "name": "Baked Salmon with Dill", "trend_score": 75}
    ]

def get_regional_recipes(region="North America"):
    """Get sample regional recipes"""
    regional_data = {
        "North America": [
            {"recipe_id": 2, "name": "Grilled Chicken with Herbs"},
            {"recipe_id": 6, "name": "Avocado Toast with Egg"},
            {"recipe_id": 10, "name": "Black Bean Tacos"}
        ],
        "Mediterranean": [
            {"recipe_id": 1, "name": "Mediterranean Quinoa Bowl"},
            {"recipe_id": 8, "name": "Greek Salad"}
        ],
        "Asian": [
            {"recipe_id": 3, "name": "Vegetable Stir Fry"},
            {"recipe_id": 7, "name": "Thai Green Curry"}
        ],
        "European": [
            {"recipe_id": 9, "name": "Mushroom Risotto"},
            {"recipe_id": 5, "name": "Baked Salmon with Dill"}
        ]
    }
    
    return regional_data.get(region, regional_data["North America"])

def get_budget_meal_suggestions(budget_level="medium"):
    """Get budget-appropriate meal suggestions"""
    budget_meals = {
        "low": [
            {"recipe_id": 3, "name": "Vegetable Stir Fry", "estimated_cost": 8},
            {"recipe_id": 4, "name": "Lentil Curry", "estimated_cost": 6},
            {"recipe_id": 10, "name": "Black Bean Tacos", "estimated_cost": 7}
        ],
        "medium": [
            {"recipe_id": 1, "name": "Mediterranean Quinoa Bowl", "estimated_cost": 12},
            {"recipe_id": 6, "name": "Avocado Toast with Egg", "estimated_cost": 10},
            {"recipe_id": 8, "name": "Greek Salad", "estimated_cost": 11}
        ],
        "high": [
            {"recipe_id": 5, "name": "Baked Salmon with Dill", "estimated_cost": 18},
            {"recipe_id": 7, "name": "Thai Green Curry", "estimated_cost": 16},
            {"recipe_id": 9, "name": "Mushroom Risotto", "estimated_cost": 15}
        ]
    }
    
    return budget_meals.get(budget_level, budget_meals["medium"])

# Sample cooking tips database
cooking_tips = {
    "beginner": [
        "Read the entire recipe before starting",
        "Prep all ingredients before cooking (mise en place)",
        "Start with simple recipes and gradually try more complex ones",
        "Don't be afraid to taste and adjust seasoning",
        "Keep your knives sharp for safer and easier cooking"
    ],
    "intermediate": [
        "Learn to cook by smell and sound, not just timers",
        "Understand the science behind cooking techniques", 
        "Experiment with spice combinations",
        "Master basic mother sauces",
        "Learn proper knife techniques for efficiency"
    ],
    "advanced": [
        "Focus on perfecting techniques rather than following recipes exactly",
        "Understand ingredient substitutions and their effects",
        "Learn to balance flavors: sweet, salty, sour, bitter, umami",
        "Experiment with different cooking methods for the same ingredient",
        "Create your own spice blends and flavor profiles"
    ]
}

# Sample food safety tips
food_safety_tips = [
    "Keep hot foods hot (above 140°F) and cold foods cold (below 40°F)",
    "Wash hands thoroughly before and after handling food",
    "Use separate cutting boards for meat and vegetables",
    "Cook meat to proper internal temperatures",
    "Don't leave perishable foods at room temperature for more than 2 hours",
    "Store leftovers promptly and use within 3-4 days",
    "When in doubt, throw it out - trust your senses"
]

if __name__ == "__main__":
    # Generate and save demo data
    demo_data = generate_demo_data()
    
    with open("demo_data.json", "w") as f:
        json.dump(demo_data, f, indent=2)
    
    print("Demo data generated successfully!")
    print(f"Generated data for {len(demo_data['user_interactions'])} interactions")
    print(f"Current season: {demo_data['current_season']}")
    print(f"Seasonal ingredients: {demo_data['seasonal_ingredients']}")