# AI-Powered Personalization Cooking Assistant 🍳

A comprehensive AI-powered cooking assistant that provides personalized recipe recommendations, nutritional analysis, ingredient substitutions, and interactive cooking guidance.

## 🌟 Features

### Core Features
- **Recipe Finder**: Search and filter recipes by cuisine, ingredients, dietary preferences, and cooking time
- **Image-to-Recipe**: Upload ingredient photos and get AI-powered recipe suggestions
- **Ingredient Substitution Engine**: Smart alternatives for missing ingredients
- **Nutritional Analysis**: Detailed breakdown of calories, macros, and nutrients
- **Interactive Cooking Mode**: Step-by-step guided cooking with timers
- **Voice Assistant**: Hands-free cooking guidance (text-to-speech ready)

### AI-Powered Intelligence
- **Adaptive Learning**: Learns user preferences over time
- **Multimodal Intelligence**: Image recognition for ingredient identification
- **Smart Substitutions**: AI-suggested ingredient alternatives
- **Health-Conscious Filtering**: Recipes tailored for specific health conditions

### Personalization
- **Dietary Filters**: Support for vegetarian, vegan, gluten-free, keto, and more
- **Health Conditions**: Recipes for diabetes, heart health, weight loss
- **Spice Level Preferences**: Customizable heat levels
- **Cooking Time Optimization**: Recipes based on available time

## 🚀 Live Demo

Deploy on Hugging Face Spaces: [Coming Soon]

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI Models**: 
  - BLIP (Image Captioning)
  - Sentence Transformers (Recipe Similarity)
  - Hugging Face Transformers
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **Voice**: SpeechRecognition, pyttsx3

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/Sathwik11-hub/AI-Powered-Personalization-cooking-assistant.git
cd AI-Powered-Personalization-cooking-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 🎯 Usage Examples

### Scenario 1: "What can I cook with this?"
1. Upload an image of ingredients
2. AI identifies ingredients and suggests recipes
3. Get personalized recommendations based on your preferences

### Scenario 2: Missing Ingredient
1. Select a recipe you want to cook
2. Use the substitution engine for missing ingredients
3. Get smart alternatives that maintain flavor and nutrition

### Scenario 3: Health-Conscious Cooking
1. Set your health conditions (diabetes, heart health, etc.)
2. Browse filtered recipes suitable for your needs
3. View detailed nutritional breakdowns

### Scenario 4: Interactive Cooking
1. Start cooking mode for step-by-step guidance
2. Use voice commands for hands-free operation
3. Set timers and track progress

## 📊 Dataset

The application includes a custom recipe dataset with:
- 50+ diverse recipes across multiple cuisines
- Complete nutritional information
- Dietary tags and health condition compatibility
- Ingredient substitution mappings
- Detailed cooking instructions

## 🤖 AI Features

### Image Recognition
- Ingredient identification from photos
- Recipe suggestion based on available ingredients
- BLIP model for accurate image captioning

### Smart Recommendations
- Sentence similarity for recipe matching
- Personalized filtering based on user preferences
- Adaptive learning from user interactions

### Health Intelligence
- Automatic nutritional analysis
- Health condition compatibility checking
- Dietary restriction compliance

## 🎮 Gamification

- Recipe rating system
- Cooking achievement tracking
- Progress visualization
- Community features (planned)

## 🔧 Configuration

### Hugging Face Spaces Deployment

Create `app.py` as the main entry point and ensure all dependencies are in `requirements.txt`.

### Custom Dataset

Recipes are stored in the application with the following structure:
```python
{
    'name': 'Recipe Name',
    'cuisine': 'Cuisine Type',
    'ingredients': ['ingredient1', 'ingredient2'],
    'instructions': ['step1', 'step2'],
    'nutrition': {'calories': 400, 'protein': 20, ...},
    'dietary_tags': ['vegetarian', 'gluten-free'],
    'health_conditions': ['diabetes-friendly', 'heart-healthy']
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Hugging Face for providing excellent AI models
- Streamlit for the amazing web app framework
- The open-source community for inspiration and tools

## 📞 Contact

For questions or suggestions, please open an issue or contact the maintainers.

---

**Built with ❤️ for healthy, personalized cooking experiences**