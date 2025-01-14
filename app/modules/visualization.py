import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DashboardManager:
    def __init__(self, app):
        self.app = app
        self._setup_callbacks()
        logger.info("DashboardManager initialized")
    
    def create_main_layout(self):
        """Create the main dashboard layout"""
        try:
            layout = dbc.Container([
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
            logger.info("Main layout created successfully")
            return layout
        except Exception as e:
            logger.error(f"Error creating main layout: {e}")
            return self._create_error_layout()
    
    def _create_error_layout(self):
        """Create a simple error layout"""
        return dbc.Container([
            html.H1("Cyber Threat Intelligence Platform"),
            html.Hr(),
            dbc.Alert(
                "Error loading dashboard components. Please check the logs.",
                color="danger"
            )
        ])
    
    def _create_header(self):
        try:
            return html.Div([
                html.H1("Cyber Threat Intelligence Dashboard"),
                html.P("Real-time threat monitoring and analysis")
            ])
        except Exception as e:
            logger.error(f"Error creating header: {e}")
            return html.Div()
    
    def _create_summary_cards(self):
        try:
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
        except Exception as e:
            logger.error(f"Error creating summary cards: {e}")
            return html.Div()
    
    def _create_threat_map(self):
        try:
            return html.Div([
                html.H3("Geographical Threat Distribution"),
                dcc.Graph(id="threat-map")
            ])
        except Exception as e:
            logger.error(f"Error creating threat map: {e}")
            return html.Div()
    
    def _create_trend_analysis(self):
        try:
            return html.Div([
                html.H3("Threat Trend Analysis"),
                dcc.Graph(id="trend-analysis")
            ])
        except Exception as e:
            logger.error(f"Error creating trend analysis: {e}")
            return html.Div()
    
    def _create_threat_distribution(self):
        try:
            return html.Div([
                html.H3("Threat Type Distribution"),
                dcc.Graph(id="threat-distribution")
            ])
        except Exception as e:
            logger.error(f"Error creating threat distribution: {e}")
            return html.Div()
    
    def _create_threat_table(self):
        try:
            return html.Div([
                html.H3("Recent Threats"),
                dbc.Table(id="threat-table")
            ])
        except Exception as e:
            logger.error(f"Error creating threat table: {e}")
            return html.Div()
    
    def _setup_callbacks(self):
        try:
            @self.app.callback(
                [Output("active-threats-count", "children"),
                 Output("risk-level", "children"),
                 Output("mitigated-count", "children"),
                 Output("alerts-count", "children")],
                [Input("interval-component", "n_intervals")]
            )
            def update_summary_cards(n):
                try:
                    # Get real-time data
                    return "25", "High", "12", "8"
                except Exception as e:
                    logger.error(f"Error updating summary cards: {e}")
                    return "N/A", "N/A", "N/A", "N/A"
            
            @self.app.callback(
                Output("threat-map", "figure"),
                [Input("interval-component", "n_intervals")]
            )
            def update_threat_map(n):
                try:
                    return self._generate_threat_map()
                except Exception as e:
                    logger.error(f"Error updating threat map: {e}")
                    return go.Figure()
            
            @self.app.callback(
                Output("trend-analysis", "figure"),
                [Input("interval-component", "n_intervals")]
            )
            def update_trend_analysis(n):
                try:
                    return self._generate_trend_chart()
                except Exception as e:
                    logger.error(f"Error updating trend analysis: {e}")
                    return go.Figure()
            
            @self.app.callback(
                Output("threat-distribution", "figure"),
                [Input("interval-component", "n_intervals")]
            )
            def update_threat_distribution(n):
                try:
                    return self._generate_distribution_chart()
                except Exception as e:
                    logger.error(f"Error updating threat distribution: {e}")
                    return go.Figure()
            
            logger.info("Callbacks set up successfully")
        except Exception as e:
            logger.error(f"Error setting up callbacks: {e}")
    
    def _generate_threat_map(self) -> go.Figure:
        try:
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
        except Exception as e:
            logger.error(f"Error generating threat map: {e}")
            return go.Figure()
    
    def _generate_trend_chart(self) -> go.Figure:
        try:
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
        except Exception as e:
            logger.error(f"Error generating trend chart: {e}")
            return go.Figure()
    
    def _generate_distribution_chart(self) -> go.Figure:
        try:
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
        except Exception as e:
            logger.error(f"Error generating distribution chart: {e}")
            return go.Figure() 