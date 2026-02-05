"""Gunicorn configuration for Render deployment."""
import os

# Bind to the PORT environment variable
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Worker settings
workers = 1
worker_class = "sync"
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
