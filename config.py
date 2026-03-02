import os
from dotenv import load_dotenv

# Load the variables from the .env file into the system environment
load_dotenv()

class Config:
    """
    Central configuration class. 
    Flask will read its settings from here.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-fallback-key')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/beehive_auth')