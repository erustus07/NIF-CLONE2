import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/niftaz_electronics')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}