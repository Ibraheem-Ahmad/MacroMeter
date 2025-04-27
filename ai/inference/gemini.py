from google.generativeai import GenerativeModel
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gemini setup
GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-2.5-flash-preview-04-17')

def recognize_ingredients(image_path: str):
    img = Image.open(image_path)

    prompt = ("""You are decomposing a complex dish into its main ingredients for nutritional analysis.

Please respond ONLY with a JSON object matching this schema:
{
  \"IngredientName\": [list of ingredient names (strings), using USDA standard ingredient names],
  \"IngredientPercentage\": [corresponding percentages (numbers, not strings), without % signs]
}
{
  \"IngredientName\": [\"grilled chicken\", \"white rice\", \"yogurt sauce\", \"lettuce\", \"tomatoes\"],
  \"IngredientPercentage\": [40.0, 35.0, 15.0, 5.0, 5.0]
}

"""

    )

    response = model.generate_content([prompt, img])

    if hasattr(response, 'text') and response.text:
        ingredients = []
        lines = response.text.strip().split("\n")
        for line in lines:
            if ":" in line:
                ingredient, percent = line.split(":", 1)
                ingredients.append({
                    "ingredient": ingredient.strip().lower(),
                    "percentage": percent.strip()
                })
        return ingredients
    else:
        raise ValueError("No valid text response from Gemini model.")

# ------------- TEST CODE BELOW ---------------- #

if __name__ == "__main__":
    # Put the path to a test image here
    test_image_path = "ai\inference\halalcart.jpg"  # <-- Change this to your own image path
    
    try:
        ingredients = recognize_ingredients(test_image_path)
        print("Recognized Ingredients:")
        print(ingredients)
    except Exception as e:
        print("Error:", e)
