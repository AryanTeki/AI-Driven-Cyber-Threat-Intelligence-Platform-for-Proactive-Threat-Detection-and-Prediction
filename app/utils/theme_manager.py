from flask import session
import dash_bootstrap_components as dbc

class ThemeManager:
    THEME_LIGHT = dbc.themes.BOOTSTRAP
    THEME_DARK = dbc.themes.DARKLY
    
    @staticmethod
    def get_theme():
        """Get current theme based on session or default"""
        return session.get('theme', 'dark')
    
    @staticmethod
    def set_theme(theme):
        """Set theme in session"""
        session['theme'] = theme
    
    @staticmethod
    def get_theme_stylesheet(theme=None):
        """Get stylesheet for specified theme"""
        if theme is None:
            theme = ThemeManager.get_theme()
            
        if theme == 'light':
            return ThemeManager.THEME_LIGHT
        return ThemeManager.THEME_DARK 