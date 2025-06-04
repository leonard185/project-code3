# config.py

import os

# Default to SQLite DB
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///health.db")

# Debug mode (useful for testing)
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
