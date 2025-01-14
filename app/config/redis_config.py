# Redis Configuration
REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True,
    'socket_timeout': 5,
    'retry_on_timeout': True
}

# Redis key prefixes
KEY_PREFIXES = {
    'threat_data': 'threat:',
    'cache': 'cache:',
    'session': 'session:'
}

# Cache expiration times (in seconds)
CACHE_EXPIRY = {
    'threat_data': 300,  # 5 minutes
    'statistics': 60,    # 1 minute
    'reports': 3600     # 1 hour
} 