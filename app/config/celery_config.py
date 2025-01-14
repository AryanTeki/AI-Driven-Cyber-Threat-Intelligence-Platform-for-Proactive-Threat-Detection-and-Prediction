from datetime import timedelta

# Celery Configuration
CELERY_CONFIG = {
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'worker_concurrency': 4,
    'task_time_limit': 3600,  # 1 hour
}

# Periodic task schedule
CELERY_BEAT_SCHEDULE = {
    'update-threat-data': {
        'task': 'app.tasks.update_threat_data',
        'schedule': timedelta(minutes=5),
    },
    'analyze-trends': {
        'task': 'app.tasks.analyze_trends',
        'schedule': timedelta(minutes=15),
    },
    'cleanup-old-reports': {
        'task': 'app.tasks.cleanup_old_reports',
        'schedule': timedelta(hours=24),
    },
} 