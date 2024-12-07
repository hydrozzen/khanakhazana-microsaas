from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load recipe and substitute data
with open("data/recipes.json") as f:
    recipes = json.load(f)

# Dummy substitution dictionary
default_substitutes = {
    "butter": "ghee",
    "paneer": "tofu",
    "cream": "coconut milk",
    "tomato": "tomato puree",
    "potato": "sweet potato"
}

@app.route('/')
def index():
    # Render the home page with the search bar
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # Get user-submitted ingredients
    user_ingredients = request.form.get('ingredients', '')
    user_ingredients = [i.strip().lower() for i in user_ingredients.split(",")]

    # Match recipes based on the user-provided ingredients
    matched_recipes = []
    for recipe in recipes:
        # Check how many ingredients the user doesn't have
        missing_ingredients = [
            ing for ing in recipe["ingredients"] if ing not in user_ingredients
        ]
        
        # Include recipes only if missing ingredients are <= 3
        if len(missing_ingredients) <= 3:
            # Map missing ingredients to their substitutes
            recipe_substitutes = {
                ing: default_substitutes.get(ing, "No substitute found") for ing in missing_ingredients
            }

            matched_recipes.append({
                "name": recipe["name"],
                "ingredients": recipe["ingredients"],  # Pass full ingredients list to template
                "instructions": recipe["instructions"],
                "missing_ingredients": missing_ingredients,
                "substitutes": recipe_substitutes
            })

    # Render results on the results page with all matched recipes
    return render_template('results.html', recipes=matched_recipes, user_ingredients=user_ingredients)

if __name__ == '__main__':
    app.run(debug=True)
