import requests
import json
import logging

class SIEMIntegration:
    def __init__(self, siem_url, api_key):
        self.siem_url = siem_url
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, alert_data):
        """Send alert to SIEM system"""
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.siem_url}/api/alerts",
                headers=headers,
                json=alert_data
            )
            
            if response.status_code == 200:
                self.logger.info("Alert sent to SIEM successfully")
                return True
            else:
                self.logger.error(f"Failed to send alert to SIEM: {response.text}")
                return False
        except Exception as e:
            self.logger.error(f"SIEM integration error: {str(e)}")
            return False 