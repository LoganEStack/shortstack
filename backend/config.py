import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATE_LIMIT=os.getenv('RATE_LIMIT')
    REDIS_URL=os.getenv("REDIS_URL")
    DOMAIN="https://go.shortstack.app/"
