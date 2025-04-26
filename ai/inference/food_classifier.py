import tensorflow as tf
import numpy as np
from pathlib import Path
from typing import List, Tuple

class FoodClassifier:
    def __init__(self, model_path: str):
        self.model = tf.keras.models.load_model(model_path)
        self.class_names = self._load_class_names()
        
    def _load_class_names(self) -> List[str]:
        # TODO: Load actual class names from a file
        return ["apple", "banana", "chicken", "rice", "broccoli"]  # Example classes
        
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        # Resize image to model's expected size
        image = tf.image.resize(image, (224, 224))
        # Normalize pixel values
        image = image / 255.0
        # Add batch dimension
        image = tf.expand_dims(image, 0)
        return image
        
    def predict(self, image: np.ndarray, confidence_threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Predict food items in the image.
        
        Args:
            image: Input image as numpy array
            confidence_threshold: Minimum confidence score to consider a prediction
            
        Returns:
            List of tuples containing (class_name, confidence_score)
        """
        # Preprocess image
        processed_image = self.preprocess_image(image)
        
        # Get predictions
        predictions = self.model.predict(processed_image)
        
        # Get top predictions above threshold
        top_predictions = []
        for i, score in enumerate(predictions[0]):
            if score > confidence_threshold:
                top_predictions.append((self.class_names[i], float(score)))
                
        return sorted(top_predictions, key=lambda x: x[1], reverse=True)
        
    def get_nutrition_info(self, food_class: str, weight_grams: float) -> dict:
        """
        Get nutrition information for a food item.
        
        Args:
            food_class: Name of the food class
            weight_grams: Weight in grams
            
        Returns:
            Dictionary containing nutrition information
        """
        # TODO: Implement USDA API integration
        # This is a placeholder implementation
        nutrition_data = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }
        
        # Example nutrition data (per 100g)
        nutrition_per_100g = {
            "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
            "chicken": {"calories": 239, "protein": 27, "carbs": 0, "fat": 14},
            "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
            "broccoli": {"calories": 34, "protein": 2.8, "carbs": 6.6, "fat": 0.4}
        }
        
        if food_class in nutrition_per_100g:
            base_nutrition = nutrition_per_100g[food_class]
            for key in nutrition_data:
                nutrition_data[key] = (base_nutrition[key] * weight_grams) / 100
                
        return nutrition_data 