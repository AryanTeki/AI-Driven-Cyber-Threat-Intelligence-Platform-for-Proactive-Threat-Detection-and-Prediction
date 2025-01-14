import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from typing import Dict, List

class DashboardManager:
    def __init__(self, app):
        self.app = app
        self._setup_callbacks()
    
    def create_main_layout(self):
        """Create the main dashboard layout"""
        return dbc.Container([
            self._create_header(),
            html.Hr(),
            self._create_summary_cards(),
            html.Hr(),
            self._create_threat_map(),
            html.Hr(),
            dbc.Row([
                dbc.Col(self._create_trend_analysis(), md=6),
                dbc.Col(self._create_threat_distribution(), md=6)
            ]),
            html.Hr(),
            self._create_threat_table(),
            dcc.Interval(
                id='interval-component',
                interval=5*1000,  # in milliseconds
                n_intervals=0
            )
        ])
    
    def _create_header(self):
        return html.Div([
            html.H1("Cyber Threat Intelligence Dashboard"),
            html.P("Real-time threat monitoring and analysis")
        ])
    
    def _create_summary_cards(self):
        return dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Active Threats", className="card-title"),
                    html.H2(id="active-threats-count")
                ])
            ]), md=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Risk Level", className="card-title"),
                    html.H2(id="risk-level")
                ])
            ]), md=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Mitigated", className="card-title"),
                    html.H2(id="mitigated-count")
                ])
            ]), md=3),
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Alerts", className="card-title"),
                    html.H2(id="alerts-count")
                ])
            ]), md=3)
        ])
    
    def _create_threat_map(self):
        return html.Div([
            html.H3("Geographical Threat Distribution"),
            dcc.Graph(id="threat-map")
        ])
    
    def _create_trend_analysis(self):
        return html.Div([
            html.H3("Threat Trend Analysis"),
            dcc.Graph(id="trend-analysis")
        ])
    
    def _create_threat_distribution(self):
        return html.Div([
            html.H3("Threat Type Distribution"),
            dcc.Graph(id="threat-distribution")
        ])
    
    def _create_threat_table(self):
        return html.Div([
            html.H3("Recent Threats"),
            dbc.Table(id="threat-table")
        ])
    
    def _setup_callbacks(self):
        @self.app.callback(
            [Output("active-threats-count", "children"),
             Output("risk-level", "children"),
             Output("mitigated-count", "children"),
             Output("alerts-count", "children")],
            [Input("interval-component", "n_intervals")]
        )
        def update_summary_cards(n):
            # Get real-time data
            return "25", "High", "12", "8"
        
        @self.app.callback(
            Output("threat-map", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_threat_map(n):
            # Create world map with threat locations
            return self._generate_threat_map()
        
        @self.app.callback(
            Output("trend-analysis", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_trend_analysis(n):
            # Create trend analysis chart
            return self._generate_trend_chart()
        
        @self.app.callback(
            Output("threat-distribution", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_threat_distribution(n):
            # Create threat distribution chart
            return self._generate_distribution_chart()
    
    def _generate_threat_map(self) -> go.Figure:
        # Sample data - replace with real data
        df = pd.DataFrame({
            'lat': [40.7128, 51.5074, 35.6762],
            'lon': [-74.0060, -0.1278, 139.6503],
            'threat_level': ['High', 'Medium', 'Low']
        })
        
        fig = px.scatter_mapbox(
            df,
            lat='lat',
            lon='lon',
            color='threat_level',
            mapbox_style='carto-positron',
            zoom=1
        )
        return fig
    
    def _generate_trend_chart(self) -> go.Figure:
        # Sample data - replace with real data
        df = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=10),
            'threats': [10, 15, 13, 17, 20, 18, 22, 25, 23, 28]
        })
        
        fig = px.line(
            df,
            x='date',
            y='threats',
            title='Threat Trends Over Time'
        )
        return fig
    
    def _generate_distribution_chart(self) -> go.Figure:
        # Sample data - replace with real data
        df = pd.DataFrame({
            'type': ['Malware', 'Phishing', 'DDoS', 'Ransomware'],
            'count': [30, 25, 15, 20]
        })
        
        fig = px.pie(
            df,
            values='count',
            names='type',
            title='Threat Type Distribution'
        )
        return fig 