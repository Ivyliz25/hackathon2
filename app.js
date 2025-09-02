const FLASK_SERVER_URL = "https://coderscave-3.onrender.com"; // Change to your Flask server URL

document.addEventListener("DOMContentLoaded", () => {
  const generateBtn = document.getElementById("generate");
  const recipeOutput = document.getElementById("recipeOutput");

  generateBtn.addEventListener("click", async () => {
    const ingredients = document.getElementById("ingredients").value.trim();
    const cuisine = document.getElementById("cuisine").value.trim() || "global";
    const diet = document.getElementById("diet").value.trim() || "any";
    const servings = document.getElementById("servings").value || "2";

    if (!ingredients) {
      recipeOutput.innerHTML = "⚠️ Please enter at least one ingredient.";
      return;
    }

    recipeOutput.innerHTML = "🤖 Generating your recipe... Please wait.";

    try {
      const url = `${FLASK_SERVER_URL}/generate_recipe?recipe_name=${encodeURIComponent(
        ingredients
      )}&budget=${servings}&region=${encodeURIComponent(cuisine)}&diet=${encodeURIComponent(diet)}`;

      const response = await fetch(url);
      const data = await response.json();

      if (response.ok && data.result) {
        displayCollapsibleRecipe(data.result);
      } else {
        throw new Error(data.error || "Unexpected response from server");
      }
    } catch (error) {
      console.error("Error fetching recipe:", error);
      recipeOutput.innerHTML = `❌ Failed to generate recipe. Error: ${error.message}`;
    }
  });
});

// Display recipe in a collapsible card
function displayCollapsibleRecipe(text) {
  const recipeOutput = document.getElementById("recipeOutput");

  // Create collapsible card
  const card = document.createElement("div");
  card.className = "card";

  const header = document.createElement("h2");
  header.textContent = "AI-Generated Recipe 🍳";
  header.style.cursor = "pointer";

  const content = document.createElement("pre");
  content.textContent = text;
  content.style.display = "none";

  header.addEventListener("click", () => {
    content.style.display = content.style.display === "none" ? "block" : "none";
  });

  card.appendChild(header);
  card.appendChild(content);

  // Clear previous output
  recipeOutput.innerHTML = "";
  recipeOutput.appendChild(card);
}






