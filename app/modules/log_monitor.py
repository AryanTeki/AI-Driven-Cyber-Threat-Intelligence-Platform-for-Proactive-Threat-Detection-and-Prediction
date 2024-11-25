# app/modules/log_monitor.py

import time
from datetime import datetime
import random
import json

class LogMonitor:
    def __init__(self):
        self.log_types = [
            "Authentication", "Network", "System", "Application",
            "Security", "Firewall", "Database"
        ]
        self.status_codes = [
            "SUCCESS", "FAILURE", "WARNING", "ERROR", "INFO"
        ]
        
    def generate_log_entry(self):
        """Generate a simulated log entry."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = {
            "timestamp": current_time,
            "log_type": random.choice(self.log_types),
            "status": random.choice(self.status_codes),
            "source_ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "user": f"user_{random.randint(1000, 9999)}",
            "message": self._generate_log_message(),
            "event_id": random.randint(1000, 9999)
        }
        return log_entry
    
    def _generate_log_message(self):
        """Generate a meaningful log message based on log type and status."""
        messages = {
            "Authentication": [
                "Failed login attempt",
                "Successful login",
                "Password reset requested",
                "Account locked"
            ],
            "Network": [
                "Connection timeout",
                "Port scan detected",
                "Network interface down",
                "Bandwidth threshold exceeded"
            ],
            "Security": [
                "Firewall rule violation",
                "Intrusion attempt detected",
                "Malicious payload blocked",
                "Security policy violation"
            ]
        }
        return random.choice(messages.get(random.choice(list(messages.keys()))))
    
    def get_logs(self, count=50):
        """Generate multiple log entries."""
        return [self.generate_log_entry() for _ in range(count)]
    
    def monitor_logs(self, callback=None):
        """Start monitoring logs with a callback function."""
        while True:
            log_entry = self.generate_log_entry()
            if callback:
                callback(log_entry)
            time.sleep(random.uniform(0.5, 2.0))  # Random delay between logs