import os

# Application settings
APP_NAME = "Cyber Threat Intelligence Platform"
DEBUG = True
SECRET_KEY = 'your-secret-key-here'  # Change in production

# Server settings
HOST = '0.0.0.0'
PORT = 8050

# Database settings (if using)
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')

# SIEM settings
SIEM_URL = os.getenv('SIEM_URL', 'http://localhost:9000')
SIEM_API_KEY = os.getenv('SIEM_API_KEY', 'default-key')

# Monitoring settings
MONITORING_INTERVAL = 5000  # milliseconds

# Reporting settings
REPORTS_DIR = 'reports'
LOGS_DIR = 'logs'

# Create required directories
for directory in [REPORTS_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True) 