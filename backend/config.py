from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "MacroMeter"
    
    # MongoDB Settings
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "macrometer"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # USDA API Settings
    USDA_API_KEY: str = "your-usda-api-key"
    
    # AI Model Settings
    MODEL_PATH: str = "../ai/models/food_classifier"
    CONFIDENCE_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings() 