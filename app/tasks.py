from celery import Celery
from config.celery_config import CELERY_CONFIG
from config.redis_config import REDIS_CONFIG
import redis
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Celery
celery_app = Celery('cyber_threat_intel')
celery_app.config_from_object(CELERY_CONFIG)

# Initialize Redis
redis_client = redis.Redis(**REDIS_CONFIG)

@celery_app.task
def update_threat_data():
    """Update threat data from various sources"""
    try:
        from data_generation import generate_threat_data
        df = generate_threat_data(100)
        redis_client.set('latest_threat_data', df.to_json())
        logger.info("Threat data updated successfully")
    except Exception as e:
        logger.error(f"Error updating threat data: {str(e)}")

@celery_app.task
def cleanup_old_reports():
    """Clean up old report files"""
    try:
        reports_dir = 'reports'
        if not os.path.exists(reports_dir):
            return
        
        # Delete reports older than 7 days
        cutoff = datetime.now() - timedelta(days=7)
        
        for filename in os.listdir(reports_dir):
            filepath = os.path.join(reports_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            
            if file_time < cutoff:
                os.remove(filepath)
                logger.info(f"Deleted old report: {filename}")
    except Exception as e:
        logger.error(f"Error cleaning up reports: {str(e)}")

@celery_app.task
def send_alert(threat_data):
    """Send alert for high-severity threats"""
    try:
        # Implementation for sending alerts (email, Slack, etc.)
        pass
    except Exception as e:
        logger.error(f"Error sending alert: {str(e)}") 