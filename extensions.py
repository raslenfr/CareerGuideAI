"""
Flask extensions initialization.
Import these in blueprints to avoid circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize extensions (will be bound to app in app.py)
db = SQLAlchemy()
bcrypt = Bcrypt()

