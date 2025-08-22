"""
Configuration settings for Healthcare BERT QA System
"""

import os
from pathlib import Path
from typing import Dict, Any

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

class Config:
    """Base configuration class"""
    
    # Application settings
    APP_NAME = "Healthcare BERT QA System"
    VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    
    # Model settings
    BIOBERT_MODEL_NAME = os.getenv("BIOBERT_MODEL_NAME", "dmis-lab/biobert-base-cased-v1.1")
    SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
    MAX_SEQUENCE_LENGTH = int(os.getenv("MAX_SEQUENCE_LENGTH", 512))
    
    # Data directories
    DATA_DIR = BASE_DIR / "data"
    DOCUMENTS_DIR = DATA_DIR / "documents"
    DATASETS_DIR = DATA_DIR / "datasets"
    EMBEDDINGS_DIR = DATA_DIR / "embeddings"
    
    # Model directories
    MODELS_DIR = BASE_DIR / "models"
    BIOBERT_DIR = MODELS_DIR / "biobert"
    CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"
    
    # Vector search settings
    FAISS_INDEX_PATH = EMBEDDINGS_DIR / "document_index.faiss"
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 512))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 5))
    
    # QA settings
    MIN_CONFIDENCE_SCORE = float(os.getenv("MIN_CONFIDENCE_SCORE", 0.1))
    MAX_ANSWER_LENGTH = int(os.getenv("MAX_ANSWER_LENGTH", 100))
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/healthcare_qa.db")
    
    # Redis settings (for caching)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TIMEOUT = int(os.getenv("CACHE_TIMEOUT", 3600))  # 1 hour
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "healthcare-qa-secret-key-change-in-production")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 60))
    
    # Healthcare-specific settings
    MEDICAL_DISCLAIMER = (
        "This system provides information for educational purposes only. "
        "It is not intended to replace professional medical advice, diagnosis, or treatment. "
        "Always consult with qualified healthcare professionals for medical decisions."
    )
    
    # Supported document types
    SUPPORTED_DOCUMENT_TYPES = [".pdf", ".txt", ".docx", ".html"]
    
    # API settings
    API_PREFIX = "/api/v1"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.DATA_DIR,
            cls.DOCUMENTS_DIR,
            cls.DATASETS_DIR,
            cls.EMBEDDINGS_DIR,
            cls.MODELS_DIR,
            cls.BIOBERT_DIR,
            cls.CHECKPOINTS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = "DEBUG"

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = "WARNING"
    
    # Override security settings for production
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    if not SECRET_KEY and FLASK_ENV == 'production':
        raise ValueError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = "sqlite:///:memory:"

# Configuration mapping
config_map: Dict[str, Any] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")
    
    return config_map.get(config_name, DevelopmentConfig)

