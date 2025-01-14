# app/main.py

import os
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from flask import Flask, session, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import importlib

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Function to safely import modules
def safe_import(module_name, class_name):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        return getattr(module, class_name)
    except ImportError as e:
        logger.error(f"Error importing {class_name} from {module_name}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error importing {class_name} from {module_name}: {str(e)}")
        return None

# Import modules with improved error handling
DataCollector = safe_import('data_collection', 'DataCollector')
MLAnalyzer = safe_import('ml_analysis', 'MLAnalyzer')
DashboardManager = safe_import('visualization', 'DashboardManager')

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
        <!DOCTYPE html>
        <html>
        <head>
            <title>Login - Cyber Threat Intelligence Platform</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
            <style>
                body {
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .login-container {
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
                    width: 100%;
                    max-width: 400px;
                }
                .login-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .login-header i {
                    font-size: 3rem;
                    color: #1e3c72;
                    margin-bottom: 20px;
                }
                .form-control {
                    border-radius: 20px;
                    padding: 12px 20px;
                }
                .btn-login {
                    background: linear-gradient(45deg, #1e3c72, #2a5298);
                    border: none;
                    border-radius: 20px;
                    padding: 12px;
                    width: 100%;
                    color: white;
                    font-weight: bold;
                    margin-top: 20px;
                }
                .btn-login:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="login-header">
                    <i class="fas fa-shield-alt"></i>
                    <h2>Welcome Back</h2>
                    <p class="text-muted">Sign in to your account</p>
                </div>
                <form method="post">
                    <div class="mb-3">
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-user"></i></span>
                            <input type="text" name="username" class="form-control" placeholder="Username" required>
                        </div>
                    </div>
                    <div class="mb-3">
                        <div class="input-group">
                            <span class="input-group-text"><i class="fas fa-lock"></i></span>
                            <input type="password" name="password" class="form-control" placeholder="Password" required>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-login">Sign In</button>
                </form>
            </div>
        </body>
        </html>
    '''

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Initialize modules with improved error handling
def initialize_module(module_class, config, module_name):
    if module_class:
        try:
            instance = module_class(config)
            logger.info(f"Successfully initialized {module_name}")
            return instance
        except Exception as e:
            logger.error(f"Error initializing {module_name}: {str(e)}")
            return None
    return None

# Load configuration
config = {
    'otx_api_key': os.environ.get('OTX_API_KEY', 'demo-key'),
    'vt_api_key': os.environ.get('VT_API_KEY', 'demo-key'),
    'twitter_api_key': os.environ.get('TWITTER_API_KEY'),
    'twitter_api_secret': os.environ.get('TWITTER_API_SECRET'),
    'reddit_client_id': os.environ.get('REDDIT_CLIENT_ID'),
    'reddit_client_secret': os.environ.get('REDDIT_CLIENT_SECRET'),
    'reddit_user_agent': 'CTI Platform v1.0'
}

# Initialize modules
data_collector = initialize_module(DataCollector, config, "DataCollector")
ml_analyzer = initialize_module(MLAnalyzer, config, "MLAnalyzer")

# Initialize Dash app first
app = Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
    ],
    url_base_pathname='/',
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Then initialize dashboard manager
dashboard_manager = initialize_module(DashboardManager, app, "DashboardManager")

# Create a function to generate the fallback layout with more detailed status information
def create_fallback_layout():
    status_items = []
    
    # Check each component's status
    components = {
        'Data Collector': data_collector,
        'ML Analyzer': ml_analyzer,
        'Dashboard Manager': dashboard_manager
    }
    
    for name, component in components.items():
        status = "Available" if component else "Not Available"
        color = "success" if component else "danger"
        status_items.append(
            dbc.ListGroupItem(
                [
                    html.I(
                        className=f"fas {'fa-check' if component else 'fa-times'} me-2",
                        style={'color': 'green' if component else 'red'}
                    ),
                    f"{name}: {status}"
                ],
                color=color
            )
        )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.I(className="fas fa-shield-alt fa-3x mb-3", style={'color': '#1e3c72'}),
                    html.H1("Cyber Threat Intelligence Platform", className="header-title"),
                    html.Hr(),
                    dbc.Alert([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Some components are not available. Please check the component status below."
                    ], color="warning", className="fade-in mb-4"),
                    html.H4("Component Status", className="mb-3"),
                    dbc.ListGroup(status_items, className="mb-4"),
                    html.Div([
                        html.H4("Troubleshooting Steps:", className="mb-3"),
                        html.Ol([
                            html.Li("Check if all required Python packages are installed"),
                            html.Li("Verify environment variables are properly set"),
                            html.Li("Check application logs for detailed error messages"),
                            html.Li("Ensure all required API keys are configured")
                        ])
                    ])
                ], className="text-center py-5")
            ])
        ])
    ], fluid=True, className="px-4 py-3")

# Set up the dashboard layout
if dashboard_manager:
    app.layout = dashboard_manager.create_main_layout()
else:
    app.layout = create_fallback_layout()

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