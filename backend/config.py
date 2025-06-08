import os
from dotenv import load_dotenv
from pathlib import Path


ENV = "development"

# Load variables from .env into environment
BASE_DIR = Path(__file__).resolve().parent
dotenv_path = BASE_DIR / f".env.{ENV}"
load_dotenv(dotenv_path)

class Config:
    API_KEY = os.getenv('API_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RATE_LIMIT=os.getenv('RATE_LIMIT')
    REDIS_URL=os.getenv("REDIS_URL")
    DOMAIN="https://go.shortstack.app/"
