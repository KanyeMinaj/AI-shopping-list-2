"""
Configuration file for the AI Shopping List Generator
"""
import os
from dataclasses import dataclass

@dataclass
class Config:
    # API Keys
    GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY")
    YOUTUBE_API_KEY: str = os.environ.get("YOUTUBE_API_KEY")
    
    # YouTube API settings
    YOUTUBE_API_SERVICE_NAME: str = "youtube"
    YOUTUBE_API_VERSION: str = "v3"
    MAX_RESULTS: int = 5
    
    # Model settings
    GROQ_MODEL: str = "llama3-8b-8192"
    TEMPERATURE: float = 0.2
    
    # File paths
    RECIPE_DATA_DIR: str = "data/recipes"
    MODEL_DIR: str = "models"
    
    # Recipe extraction settings
    MIN_VIDEO_DURATION: int = 60  # seconds
    MAX_VIDEO_DURATION: int = 1800  # 30 minutes
    
    @classmethod
    def validate(cls):
        """Validate that required API keys are set"""
        config = cls()
        if not config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY environment variable is required")
        return config
