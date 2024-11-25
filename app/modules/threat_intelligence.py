# app/modules/threat_intelligence.py

import random
import time
from datetime import datetime
import ipaddress
import json

class ThreatIntelligence:
    def __init__(self):
        self.threat_categories = [
            "Malware", "Phishing", "DDoS", "Brute Force", 
            "SQL Injection", "Zero-day Exploit", "Ransomware"
        ]
        self.threat_sources = [
            "External Feed", "Internal Detection", "OSINT", 
            "Partner Network", "Honeypot"
        ]
        
    def generate_random_ip(self):
        """Generate a random IP address for demo purposes."""
        return str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))

    def get_threat_data(self):
        """Simulate fetching threat intelligence data."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        threat_data = {
            "timestamp": current_time,
            "source_ip": self.generate_random_ip(),
            "destination_ip": self.generate_random_ip(),
            "threat_type": random.choice(self.threat_categories),
            "severity_score": round(random.uniform(1, 10), 2),
            "source": random.choice(self.threat_sources),
            "confidence_score": round(random.uniform(0.1, 1.0), 2),
            "raw_indicators": {
                "port": random.randint(1, 65535),
                "protocol": random.choice(["TCP", "UDP", "HTTP", "HTTPS"]),
                "payload_hash": hex(random.getrandbits(128))[2:]
            }
        }
        return threat_data

    def get_historical_threats(self, count=100):
        """Generate historical threat data for initial dashboard population."""
        return [self.get_threat_data() for _ in range(count)]

    def save_threat_data(self, threat_data, filename="threat_data.json"):
        """Save threat data to a JSON file."""
        try:
            with open(filename, 'a') as f:
                json.dump(threat_data, f)
                f.write('\n')
        except Exception as e:
            print(f"Error saving threat data: {e}")