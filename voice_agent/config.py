import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    
    # Provider Settings
    ASR_PROVIDER = os.getenv('ASR_PROVIDER', 'openai') # or google
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
    
    # DB configuration (SQLite for local dev)
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///voice_agent.db')
