import sys
import os

path = '/home/LittleBunnehGod/Promethean-Unified-Platform'
if path not in sys.path:
    sys.path.append(path)

os.environ['PYTHONPATH'] = path
os.environ.setdefault("FLASK_ENV", "production")

from backend.app import app as application
