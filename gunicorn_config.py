"""Gunicorn configuration for Render deployment."""
import os

# Read PORT from environment - Render sets this automatically
port = os.environ.get('PORT', '10000')
print(f"🔍 PORT environment variable: {port}")

# Bind to the PORT environment variable
bind = f"0.0.0.0:{port}"

# Worker settings
workers = 1
worker_class = "sync"
timeout = 120

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
