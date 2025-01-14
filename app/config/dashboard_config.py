class DashboardConfig:
    DEFAULT_CONFIG = {
        'refresh_interval': 5000,
        'default_view': 'threat_map',
        'charts': {
            'threat_map': True,
            'severity_distribution': True,
            'threat_types': True,
            'timeline': True
        },
        'theme': 'dark'
    }
    
    @staticmethod
    def load_config(user_id):
        """Load user-specific dashboard configuration"""
        # In production, fetch from database
        return DashboardConfig.DEFAULT_CONFIG
    
    @staticmethod
    def save_config(user_id, config):
        """Save user-specific dashboard configuration"""
        # In production, save to database
        pass 