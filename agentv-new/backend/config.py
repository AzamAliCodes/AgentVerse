import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

class Config:
    """Application configuration"""

    # MongoDB settings
    MONGO_URL: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME: str = os.environ.get('DB_NAME', 'agentverse')

    # Gemini API settings
    GEMINI_API_KEY: str = os.environ.get('GEMINI_API_KEY', '')

    # CORS settings
    CORS_ORIGINS: str = os.environ.get('CORS_ORIGINS', '*')

    # Server settings
    HOST: str = os.environ.get('HOST', '0.0.0.0')
    PORT: int = int(os.environ.get('PORT', 8000))

    # Logging
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')

config = Config()
