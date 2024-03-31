# app/__init__.py
from flask import Flask

app = Flask(__name__)

from app import routes  # Import routes at the end to avoid circular dependencies
