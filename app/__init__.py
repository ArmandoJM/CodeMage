# app/__init__.py
import os
from flask import Flask
from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from .env.

app = Flask(__name__)
# Access the environment variable for the secret key
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'a_default_secret_key')

from app import routes  # Import routes at the end to avoid circular dependencies
