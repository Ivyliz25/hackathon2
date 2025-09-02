import os
import bcrypt
import mysql.connector
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")  # Needed for sessions

# ✅ MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",          # change if needed
    password="yourpassword",  # change if needed
    database="flavornest"
)
cursor = db.cursor(dictionary=True)

# ✅ Gemini config
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ------------------ AUTH ------------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # hash password
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
        db.commit()
        return jsonify({"message": "Signup successful"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        session["user_id"] = user["id"]   # ✅ store user id in session
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out"})


# ------------------ RECIPES ------------------

@app.route('/generate_recipe', methods=['GET'])
def generate_recipe():
    recipe_name = request.args.get('recipe_name')
    budget = request.args.get('budget', '10')
    region = request.args.get('region', 'global')
    diet = request.args.get('diet', 'any')

    if not recipe_name:
        return jsonify({'error': 'Missing recipe_name parameter'}), 400

    prompt = f"""
    Suggest 1 simple, low-cost, high-nutrition recipe with {recipe_name} for {region}.
    Ensure the total cost does not exceed ${budget}.
    Diet preference: {diet}.
    Prioritize cheap ingredients like rice, lentils, and vegetables.
    Provide:
    1. Ingredients with measurements
    2. Step-by-step instructions
    Format as plain text.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        if not response.text:
            return jsonify({'error': 'Empty response from Gemini'}), 500

        # ✅ Save to DB if user is logged in
        user_id = session.get("user_id")
        if user_id:
            cursor.execute(
                "INSERT INTO recipes (ingredients, suggestions, user_id) VALUES (%s, %s, %s)",
                (recipe_name, response.text, user_id)
            )
            db.commit()

        return jsonify({'result': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/my_recipes', methods=['GET'])
def my_recipes():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    cursor.execute("SELECT id, ingredients, suggestions FROM recipes WHERE user_id = %s", (user_id,))
    recipes = cursor.fetchall()

    return jsonify({'recipes': recipes})


# ------------------ MAIN ------------------

if __name__ == '__main__':
    app.run(debug=True)



