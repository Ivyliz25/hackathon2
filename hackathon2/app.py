from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/generate_recipe", methods=["GET"])
def generate_recipe():
    """
    Generate multiple affordable recipes using Gemini AI
    """
    ingredients = request.args.get("recipe_name")
    cuisine = request.args.get("region", "global")
    diet = request.args.get("diet", "any")
    servings = request.args.get("budget", "2")   # reused as servings

    if not ingredients:
        return jsonify({"error": "Missing recipe_name parameter"}), 400

    prompt = f"""
    You are a professional chef and nutritionist.
    Suggest 3 different affordable, high-nutrition recipes using these ingredients: {ingredients}.
    Cuisine preference: {cuisine}.
    Diet preference: {diet}.
    Servings: {servings} people.

    ⚡ Requirements:
    - Recipes must be budget-friendly and nutritious.
    - Use common, affordable ingredients.
    - Provide clear sections for each recipe.

    📌 Format:
    ### Recipe 1
    🍴 Recipe Name
    🛒 Ingredients (with measurements)
    🥣 Instructions (step by step)
    💡 Tips (optional)
    🔋 Nutrition Estimate (calories per serving)

    ### Recipe 2
    ...
    ### Recipe 3
    ...
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if not response.text:
            return jsonify({"error": "Empty response from Gemini"}), 500

        return jsonify({"result": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/submit_recipe", methods=["POST"])
def submit_recipe():
    """
    Accept user-submitted recipes
    """
    data = request.get_json()
    recipe_name = data.get("recipe_name")
    ingredients = data.get("ingredients")
    instructions = data.get("instructions")

    if not all([recipe_name, ingredients, instructions]):
        return jsonify({"error": "Missing required fields"}), 400

    # Here you could save to a database instead
    return jsonify({"message": "Recipe submitted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)


