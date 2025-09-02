const FLASK_SERVER_URL = "https://coderscave-3.onrender.com"; // your Flask server URL

document.addEventListener("DOMContentLoaded", () => {
  const generateBtn = document.getElementById("generate");
  const recipeOutput = document.getElementById("recipeOutput");

  generateBtn.addEventListener("click", async () => {
    const ingredients = document.getElementById("ingredients").value.trim();
    const cuisine = document.getElementById("cuisine").value.trim() || "global";
    const diet = document.getElementById("diet").value.trim() || "any";
    const servings = document.getElementById("servings").value || "2";

    if (!ingredients) {
      recipeOutput.innerHTML = `<div class="error-message">⚠️ Please enter at least one ingredient.</div>`;
      return;
    }

    recipeOutput.innerHTML = `<div class="loading">🤖 Generating recipes... Please wait.</div>`;

    try {
      const url = `${FLASK_SERVER_URL}/generate_recipe?recipe_name=${encodeURIComponent(
        ingredients
      )}&budget=${servings}&region=${encodeURIComponent(
        cuisine
      )}&diet=${encodeURIComponent(diet)}`;

      const response = await fetch(url);
      const data = await response.json();

      if (response.ok && data.result) {
        renderRecipes(data.result, recipeOutput);
      } else {
        throw new Error(data.error || "Unexpected response from server");
      }
    } catch (error) {
      console.error("Error:", error);
      recipeOutput.innerHTML = `<div class="error-message">❌ Failed to generate recipes. Error: ${error.message}</div>`;
    }
  });
});

/**
 * Render multiple recipes in boxes
 */
function renderRecipes(text, container) {
  container.innerHTML = "";

  // Split recipes based on "### Recipe"
  const recipes = text.split(/###\s*Recipe/i).filter(r => r.trim() !== "");

  if (recipes.length === 0) {
    container.innerHTML = `<div class="error-message">⚠️ No recipes generated. Try again.</div>`;
    return;
  }

  recipes.forEach((recipeText, index) => {
    const recipeBox = document.createElement("div");
    recipeBox.className = "recipe-box";
    recipeBox.innerHTML = `
      <h2>🍲 Recipe ${index + 1}</h2>
      <div class="recipe-content">${formatRecipe(recipeText)}</div>
    `;
    container.appendChild(recipeBox);
  });
}

/**
 * Format recipe text into clean HTML
 */
function formatRecipe(recipeText) {
  return recipeText
    .split("\n")
    .filter(line => line.trim() !== "")
    .map(line => {
      if (/^(\d+\.|🍴|🛒|🥣|💡|🔋)/.test(line)) {
        return `<p><strong>${line}</strong></p>`;
      }
      return `<p>${line}</p>`;
    })
    .join("");
}
document.addEventListener("click", function(e) {
  if (e.target.classList.contains("toggle-btn")) {
    const content = e.target.previousElementSibling;
    content.classList.toggle("expanded");

    if (content.classList.contains("expanded")) {
      e.target.textContent = "Show Less";
    } else {
      e.target.textContent = "Show More";
    }
  }
});






