import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
