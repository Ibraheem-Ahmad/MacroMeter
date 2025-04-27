import requests
from dotenv import load_dotenv
import os

# Load .env from project root directory
load_dotenv()

USDA_API_KEY = os.getenv("USDA_API_KEY")
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_macros_usda(ingredient_name: str):
    params = {
        "query": ingredient_name,
        "pageSize": 1,  # Get the top match
        "api_key": USDA_API_KEY,
    }
    
    response = requests.get(USDA_API_URL, params=params)
    data = response.json()
    
    if "foods" not in data or not data["foods"]:
        raise ValueError(f"No results found for {ingredient_name}")
    
    food = data["foods"][0]
    
    # Pull important nutrients
    macros = {
        "calories": None,
        "protein_g": None,
        "carbs_g": None,
        "fat_g": None
    }
    
    for nutrient in food["foodNutrients"]:
        if nutrient["nutrientName"] == "Energy":
            macros["calories"] = nutrient["value"]
        elif nutrient["nutrientName"] == "Protein":
            macros["protein_g"] = nutrient["value"]
        elif nutrient["nutrientName"] == "Carbohydrate, by difference":
            macros["carbs_g"] = nutrient["value"]
        elif nutrient["nutrientName"] == "Total lipid (fat)":
            macros["fat_g"] = nutrient["value"]
    
    return macros




def calculate_total_macros(ingredients: list, total_weight_g: float):
    macros_total = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0
    }
    
    n = len(ingredients)
    if n == 0:
        raise ValueError("No ingredients found.")
    
    weight_per_ingredient = total_weight_g / n

    for ingredient in ingredients:
        try:
            macros = get_macros_usda(ingredient)
        except Exception as e:
            print(f"Warning: Couldn't fetch macros for '{ingredient}'. Skipping.")
            continue
        
        if macros["calories"] is None:
            continue  # Skip if bad data
        
        scaling_factor = weight_per_ingredient / 100  # USDA gives per 100g
        
        macros_total["calories"] += macros["calories"] * scaling_factor
        macros_total["protein_g"] += macros["protein_g"] * scaling_factor
        macros_total["carbs_g"] += macros["carbs_g"] * scaling_factor
        macros_total["fat_g"] += macros["fat_g"] * scaling_factor

    # Round nicely
    for key in macros_total:
        macros_total[key] = round(macros_total[key], 2)
    
    return macros_total

if __name__ == "__main__":
    # === Test get_macros_usda ===
    try:
        ingredient = "chicken breast"
        macros = get_macros_usda(ingredient)
        print(f"Macros for '{ingredient}':", macros)
    except Exception as e:
        print("Error fetching macros:", e)

    # === Test calculate_total_macros ===
    try:
        ingredients_list = ["chicken breast", "white rice", "broccoli"]
        total_weight_grams = 450  # Let's say total dish weighs 450g

        total_macros = calculate_total_macros(ingredients_list, total_weight_grams)
        print("\nTotal Macros for dish (450g):", total_macros)
    except Exception as e:
        print("Error calculating total macros:", e)
