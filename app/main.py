# app/main.py

import os
from dash import Dash, html
import dash_bootstrap_components as dbc
from flask import Flask, session, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import modules with error handling
try:
    from modules.data_collection import DataCollector
    logger.info("Successfully imported DataCollector")
except ImportError as e:
    logger.error(f"Error importing DataCollector: {e}")
    DataCollector = None

try:
    from modules.ml_analysis import MLAnalyzer
    logger.info("Successfully imported MLAnalyzer")
except ImportError as e:
    logger.error(f"Error importing MLAnalyzer: {e}")
    MLAnalyzer = None

try:
    from modules.visualization import DashboardManager
    logger.info("Successfully imported DashboardManager")
except ImportError as e:
    logger.error(f"Error importing DashboardManager: {e}")
    DashboardManager = None

# Initialize Flask
server = Flask(__name__)
server.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = 'login'

# User model for authentication
class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

# Mock user database - replace with real database in production
users_db = {
    'admin': {
        'password': generate_password_hash('admin'),
        'role': 'admin'
    }
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        return User(user_id, user_id, users_db[user_id]['role'])
    return None

# Authentication routes
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users_db and check_password_hash(users_db[username]['password'], password):
            user = User(username, username, users_db[username]['role'])
            login_user(user)
            return redirect('/')
        else:
            flash('Invalid username or password')
    
    return '''
        <form method="post">
            <p><input type=text name=username placeholder="Username">
            <p><input type=password name=password placeholder="Password">
            <p><input type=submit value=Login>
        </form>
    '''

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Initialize Dash with updated parameters
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    url_base_pathname='/',
    use_pages=True  # Modern way to handle authentication in Dash
)

# Load configuration with error handling
config = {
    'otx_api_key': os.environ.get('OTX_API_KEY', 'demo-key'),
    'vt_api_key': os.environ.get('VT_API_KEY', 'demo-key'),
    'twitter_api_key': os.environ.get('TWITTER_API_KEY'),
    'twitter_api_secret': os.environ.get('TWITTER_API_SECRET'),
    'reddit_client_id': os.environ.get('REDDIT_CLIENT_ID'),
    'reddit_client_secret': os.environ.get('REDDIT_CLIENT_SECRET'),
    'reddit_user_agent': 'CTI Platform v1.0'
}

# Initialize modules with error handling
data_collector = None
ml_analyzer = None
dashboard_manager = None

if DataCollector:
    try:
        data_collector = DataCollector(config)
        logger.info("Successfully initialized DataCollector")
    except Exception as e:
        logger.error(f"Error initializing DataCollector: {e}")

if MLAnalyzer:
    try:
        ml_analyzer = MLAnalyzer(config)
        logger.info("Successfully initialized MLAnalyzer")
    except Exception as e:
        logger.error(f"Error initializing MLAnalyzer: {e}")

if DashboardManager:
    try:
        dashboard_manager = DashboardManager(app)
        logger.info("Successfully initialized DashboardManager")
    except Exception as e:
        logger.error(f"Error initializing DashboardManager: {e}")

# Set up the dashboard layout
if dashboard_manager:
    app.layout = dashboard_manager.create_main_layout()
else:
    # Fallback layout
    app.layout = dbc.Container([
        html.H1("Cyber Threat Intelligence Platform"),
        html.Hr(),
        dbc.Alert(
            "Some components are not available. Check the logs for details.",
            color="warning"
        )
    ])

# Add authentication to Dash routes using modern pattern
def protect_dashviews(app):
    for view_function in app.server.view_functions:
        if view_function.startswith(app.config.url_base_pathname):
            app.server.view_functions[view_function] = login_required(
                app.server.view_functions[view_function]
            )

protect_dashviews(app)

def start_background_tasks():
    """Start background tasks for data collection and analysis"""
    if not (data_collector and ml_analyzer):
        logger.warning("Background tasks disabled: required modules not available")
        return
    
    try:
        from celery import Celery
        
        celery = Celery('cti_platform',
                        broker='redis://localhost:6379/0',
                        backend='redis://localhost:6379/0')
        
        @celery.task
        def collect_and_analyze_data():
            try:
                # Collect threat data
                threat_data = data_collector.collect_threat_feeds()
                social_data = data_collector.monitor_social_media()
                
                # Analyze threats
                for threat in threat_data + social_data:
                    ml_analyzer.analyze_threat(threat)
                    # Store results in database
            except Exception as e:
                logger.error(f"Error in background task: {e}")
        
        # Schedule tasks
        celery.conf.beat_schedule = {
            'collect-and-analyze': {
                'task': 'collect_and_analyze_data',
                'schedule': 300.0  # every 5 minutes
            }
        }
        
        logger.info("Successfully initialized background tasks")
    except Exception as e:
        logger.error(f"Error setting up background tasks: {e}")

if __name__ == '__main__':
    # Start background tasks
    start_background_tasks()
    
    # Run the application
    app.run_server(debug=True, host='localhost', port=8050)