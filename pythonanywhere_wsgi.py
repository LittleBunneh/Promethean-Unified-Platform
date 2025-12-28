"""PythonAnywhere WSGI Configuration for Promethean-Unified-Platform"""
import os
import sys
from pathlib import Path

# Add the backend directory to the path
project_home = '/home/littlebunneh/Promethean-Unified-Platform'
sys.path.insert(0, project_home)
sys.path.insert(0, os.path.join(project_home, 'backend'))

# Set environment to production
os.environ['FLASK_ENV'] = 'production'

# Load environment variables from .env file
if os.path.exists(os.path.join(project_home, '.env')):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
