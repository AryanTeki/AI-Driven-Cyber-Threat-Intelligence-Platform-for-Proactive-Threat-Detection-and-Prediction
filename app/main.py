# app/main.py

from flask import Flask, render_template, jsonify
from modules.threat_intelligence import ThreatIntelligence
from modules.ml_classifier import ThreatClassifier
from modules.log_monitor import LogMonitor
import threading
import queue
import logging
import time
import random

app = Flask(__name__)

# Initialize components
threat_intel = ThreatIntelligence()
classifier = ThreatClassifier()
log_monitor = LogMonitor()

# Create queues for real-time updates
log_queue = queue.Queue(maxsize=1000)
threat_queue = queue.Queue(maxsize=1000)

# Store recent data in memory
recent_logs = []
recent_threats = []
MAX_STORED_ITEMS = 1000

def process_log(log_entry):
    """Process incoming log entries."""
    global recent_logs
    recent_logs.append(log_entry)
    if len(recent_logs) > MAX_STORED_ITEMS:
        recent_logs.pop(0)
    log_queue.put(log_entry)

def process_threat(threat_data):
    """Process incoming threat data."""
    global recent_threats
    # Add ML classification
    severity_prediction = classifier.predict_severity(
        threat_data['severity_score'],
        threat_data['confidence_score']
    )
    threat_data['ml_severity'] = severity_prediction
    
    recent_threats.append(threat_data)
    if len(recent_threats) > MAX_STORED_ITEMS:
        recent_threats.pop(0)
    threat_queue.put(threat_data)

# Start background threads
def run_threat_collection():
    """Background thread for collecting threat data."""
    while True:
        threat_data = threat_intel.get_threat_data()
        process_threat(threat_data)
        time.sleep(random.uniform(1, 3))

def run_log_monitoring():
    """Background thread for monitoring logs."""
    while True:
        log_entry = log_monitor.generate_log_entry()
        process_log(log_entry)
        time.sleep(random.uniform(0.5, 2.0))

@app.route('/')
def index():
    """Render the main dashboard."""
    return render_template('dashboard.html')

@app.route('/api/latest-threats')
def get_latest_threats():
    """API endpoint for getting latest threats."""
    return jsonify(recent_threats[-50:])

@app.route('/api/latest-logs')
def get_latest_logs():
    """API endpoint for getting latest logs."""
    return jsonify(recent_logs[-50:])

def start_background_tasks():
    """Start background processing threads."""
    threat_thread = threading.Thread(target=run_threat_collection, daemon=True)
    log_thread = threading.Thread(target=run_log_monitoring, daemon=True)
    
    threat_thread.start()
    log_thread.start()

if __name__ == '__main__':
    # Initialize logging
    logging.basicConfig(level=logging.INFO)
    
    # Start background tasks
    start_background_tasks()
    
    # Run the Flask app
    app.run(debug=True, use_reloader=False)