import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
from typing import Dict, List
import logging
from datetime import datetime, timedelta
import numpy as np
import random

logger = logging.getLogger(__name__)

# Mock data generation for SOC activities
class SOCDataGenerator:
    def __init__(self):
        self.threat_types = ['Malware', 'Phishing', 'DDoS', 'Ransomware', 'Data Exfiltration', 'SQL Injection', 
                           'Zero-Day Exploit', 'APT', 'Insider Threat', 'Supply Chain Attack']
        self.threat_sources = ['External', 'Internal', 'Unknown', 'Nation State', 'Cybercrime Group', 
                             'Hacktivist', 'Malicious Insider', 'Third Party']
        self.attack_vectors = ['Email', 'Web', 'Network', 'USB', 'Social Engineering', 'Cloud Services', 
                             'Remote Access', 'IoT Devices']
        self.locations = {
            'New York': {'lat': 40.7128, 'lon': -74.0060},
            'London': {'lat': 51.5074, 'lon': -0.1278},
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503},
            'Sydney': {'lat': -33.8688, 'lon': 151.2093},
            'Moscow': {'lat': 55.7558, 'lon': 37.6173},
            'Singapore': {'lat': 1.3521, 'lon': 103.8198},
            'Dubai': {'lat': 25.2048, 'lon': 55.2708},
            'Paris': {'lat': 48.8566, 'lon': 2.3522},
            'Berlin': {'lat': 52.5200, 'lon': 13.4050},
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777}
        }
        self.status_options = ['Active', 'Investigating', 'Mitigated', 'Resolved', 'Escalated']
        self.severity_levels = ['Critical', 'High', 'Medium', 'Low']

    def generate_threat_data(self, n_threats=50):
        threats = []
        current_time = datetime.now()
        
        for i in range(n_threats):
            threat_time = current_time - timedelta(minutes=random.randint(0, 60))
            severity = np.random.choice(self.severity_levels, p=[0.1, 0.2, 0.4, 0.3])
            status = np.random.choice(self.status_options, p=[0.3, 0.3, 0.2, 0.1, 0.1])
            
            threat = {
                'id': f'THR-{i+1:04d}',
                'type': random.choice(self.threat_types),
                'source': random.choice(self.threat_sources),
                'vector': random.choice(self.attack_vectors),
                'severity': severity,
                'status': status,
                'time': threat_time.strftime('%Y-%m-%d %H:%M:%S'),
                'location': random.choice(list(self.locations.keys())),
                'ip_address': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}',
                'affected_systems': random.randint(1, 10),
                'detection_method': random.choice(['SIEM', 'IDS', 'EDR', 'User Report', 'Threat Intel']),
                'confidence': random.randint(60, 100)
            }
            threats.append(threat)
        
        return pd.DataFrame(threats)

# Enhanced DashboardManager class
class DashboardManager:
    def __init__(self, app):
        self.app = app
        self.data_generator = SOCDataGenerator()
        self.current_page = 'dashboard'
        self._setup_callbacks()
        self._inject_custom_css()
        logger.info("DashboardManager initialized successfully")

    def create_main_layout(self):
        return html.Div([
            dcc.Location(id='url', refresh=False),
            self._create_navbar(),
            html.Div(id='page-content', className="px-4 py-3")
        ])

    def _create_navbar(self):
        return dbc.Navbar(
            dbc.Container([
                html.A(
                    dbc.Row([
                        dbc.Col(html.I(className="fas fa-shield-alt mr-2")),
                        dbc.Col(dbc.NavbarBrand("SOC Platform", className="ml-2")),
                    ], align="center", className="g-0"),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
                        dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
                        dbc.NavItem(dbc.NavLink("Reports", href="/reports")),
                        dbc.NavItem(dbc.NavLink("Threat Hunting", href="/threat-hunting")),
                        dbc.NavItem(dbc.NavLink("Incidents", href="/incidents")),
                        dbc.NavItem(dbc.NavLink("Training", href="/training")),
                        dbc.NavItem(dbc.NavLink("Settings", href="/settings")),
                    ], className="ml-auto", navbar=True),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]),
            color="dark",
            dark=True,
            className="mb-4",
        )

    def _setup_callbacks(self):
        """Set up all callbacks for the dashboard"""
        # Navbar toggle callback
        @self.app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        # Page routing callback
        @self.app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
        )
        def display_page(pathname):
            try:
                if pathname == '/dashboard' or pathname == '/':
                    return self._create_dashboard_page()
                elif pathname == '/analytics':
                    return self._create_analytics_page()
                elif pathname == '/reports':
                    return self._create_reports_page()
                elif pathname == '/threat-hunting':
                    return self._create_threat_hunting_page()
                elif pathname == '/incidents':
                    return self._create_incidents_page()
                elif pathname == '/training':
                    return self._create_training_page()
                elif pathname == '/settings':
                    return self._create_settings_page()
                else:
                    return self._create_dashboard_page()
            except Exception as e:
                logger.error(f"Error in page routing: {e}")
                return html.Div("Error loading page")

        # Dashboard callbacks
        @self.app.callback(
            [Output("active-threats-count", "children"),
             Output("risk-level", "children"),
             Output("mitigated-count", "children"),
             Output("alerts-count", "children")],
            [Input("interval-component", "n_intervals")]
        )
        def update_summary_cards(n):
            try:
                df = self.data_generator.generate_threat_data()
                active_threats = len(df[df['status'] == 'Active'])
                risk_level = "High" if active_threats > 10 else "Medium" if active_threats > 5 else "Low"
                mitigated = len(df[df['status'] == 'Mitigated'])
                alerts = len(df[df['severity'].isin(['Critical', 'High'])])
                return str(active_threats), risk_level, str(mitigated), str(alerts)
            except Exception as e:
                logger.error(f"Error updating summary cards: {e}")
                return "N/A", "N/A", "N/A", "N/A"

        @self.app.callback(
            Output("threat-map", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_threat_map(n):
            try:
                df = self.data_generator.generate_threat_data()
                locations = self.data_generator.locations
                
                fig = go.Figure()
                
                # Add threat points
                fig.add_trace(go.Scattergeo(
                    lon=[locations[loc]['lon'] for loc in df['location']],
                    lat=[locations[loc]['lat'] for loc in df['location']],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=['red' if s == 'Critical' else 'orange' if s == 'High' else 'yellow' if s == 'Medium' else 'green' 
                               for s in df['severity']],
                        opacity=0.7,
                        symbol='circle',
                        line=dict(width=1, color='white')
                    ),
                    text=df.apply(lambda x: f"Location: {x['location']}<br>Type: {x['type']}<br>Severity: {x['severity']}", axis=1),
                    hoverinfo='text'
                ))
                
                fig.update_layout(
                    geo=dict(
                        projection_type='equirectangular',
                        showland=True,
                        showcountries=True,
                        showocean=True,
                        countrywidth=0.5,
                        landcolor='rgb(43, 49, 55)',
                        oceancolor='rgb(52, 58, 64)',
                        showcoastlines=True,
                        coastlinecolor='rgba(255, 255, 255, 0.2)',
                        showframe=False,
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    height=400
                )
                
                return fig
            except Exception as e:
                logger.error(f"Error updating threat map: {e}")
                return go.Figure()

        @self.app.callback(
            Output("trend-analysis", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_trend_analysis(n):
            try:
                df = self.data_generator.generate_threat_data()
                df['time'] = pd.to_datetime(df['time'])
                hourly_counts = df.groupby([pd.Grouper(key='time', freq='H'), 'severity']).size().reset_index(name='count')
                
                fig = go.Figure()
                
                for severity in df['severity'].unique():
                    severity_data = hourly_counts[hourly_counts['severity'] == severity]
                    fig.add_trace(go.Scatter(
                        x=severity_data['time'],
                        y=severity_data['count'],
                        name=severity,
                        mode='lines+markers',
                        line=dict(width=2),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title='24-Hour Threat Activity',
                    xaxis_title='Time',
                    yaxis_title='Number of Threats',
                    showlegend=True,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300
                )
                
                return fig
            except Exception as e:
                logger.error(f"Error updating trend analysis: {e}")
                return go.Figure()

        @self.app.callback(
            Output("threat-distribution", "figure"),
            [Input("interval-component", "n_intervals")]
        )
        def update_threat_distribution(n):
            try:
                df = self.data_generator.generate_threat_data()
                type_counts = df['type'].value_counts()
                
                fig = go.Figure(data=[go.Pie(
                    labels=type_counts.index,
                    values=type_counts.values,
                    hole=0.6,
                    marker=dict(colors=px.colors.qualitative.Set3),
                    textinfo='label+percent',
                    hoverinfo='label+value'
                )])
                
                fig.update_layout(
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=300,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                
                return fig
            except Exception as e:
                logger.error(f"Error updating threat distribution: {e}")
                return go.Figure()

        @self.app.callback(
            Output("recent-alerts-content", "children"),
            [Input("interval-component", "n_intervals")]
        )
        def update_recent_alerts(n):
            try:
                df = self.data_generator.generate_threat_data()
                recent_alerts = df.nlargest(5, 'time')
                
                alert_items = []
                for _, alert in recent_alerts.iterrows():
                    severity_colors = {
                        "Critical": "danger",
                        "High": "warning",
                        "Medium": "info",
                        "Low": "success"
                    }
                    alert_items.append(
                        dbc.ListGroupItem([
                            html.Div([
                                html.Div([
                                    html.Strong(f"{alert['type']}", className="mb-1"),
                                    dbc.Badge(alert['severity'], 
                                            color=severity_colors.get(alert['severity'], "primary"),
                                            className="ml-2")
                                ], className="d-flex justify-content-between align-items-center"),
                                html.P(f"Location: {alert['location']}", className="mb-0 small"),
                                html.Small(alert['time'], className="text-muted")
                            ])
                        ])
                    )
                
                return dbc.ListGroup(alert_items)
            except Exception as e:
                logger.error(f"Error updating recent alerts: {e}")
                return html.Div("Error loading alerts")

        @self.app.callback(
            Output("threat-table-content", "children"),
            [Input("interval-component", "n_intervals")]
        )
        def update_threat_table(n):
            try:
                df = self.data_generator.generate_threat_data()
                
                table_header = [
                    html.Thead(html.Tr([
                        html.Th("ID"),
                        html.Th("Type"),
                        html.Th("Source"),
                        html.Th("Severity"),
                        html.Th("Status"),
                        html.Th("Location"),
                        html.Th("Time")
                    ]))
                ]
                
                rows = []
                for _, threat in df.iterrows():
                    severity_colors = {
                        "Critical": "danger",
                        "High": "warning",
                        "Medium": "info",
                        "Low": "success"
                    }
                    status_colors = {
                        "Active": "danger",
                        "Investigating": "warning",
                        "Contained": "info",
                        "Resolved": "success"
                    }
                    rows.append(html.Tr([
                        html.Td(threat['id']),
                        html.Td(threat['type']),
                        html.Td(threat['source']),
                        html.Td(dbc.Badge(
                            threat['severity'],
                            color=severity_colors.get(threat['severity'], "primary")
                        )),
                        html.Td(dbc.Badge(
                            threat['status'],
                            color=status_colors.get(threat['status'], "primary")
                        )),
                        html.Td(threat['location']),
                        html.Td(threat['time'])
                    ]))
                
                table_body = [html.Tbody(rows)]
                
                return dbc.Table(
                    table_header + table_body,
                    bordered=True,
                    hover=True,
                    responsive=True,
                    striped=True,
                    className="align-middle"
                )
            except Exception as e:
                logger.error(f"Error updating threat table: {e}")
                return html.Div("Error loading threat data")

        # Analytics page callbacks
        @self.app.callback(
            [Output("threat-intel-summary", "figure"),
             Output("attack-vector-chart", "figure"),
             Output("severity-chart", "figure"),
             Output("detection-methods-chart", "figure"),
             Output("threat-timeline", "figure")],
            [Input("analytics-interval", "n_intervals")]
        )
        def update_analytics_charts(n):
            try:
                df = self.data_generator.generate_threat_data()
                return (
                    self._create_threat_intel_visualization(df),
                    self._create_attack_vector_visualization(df),
                    self._create_severity_visualization(df),
                    self._create_detection_visualization(df),
                    self._create_timeline_visualization(df)
                )
            except Exception as e:
                logger.error(f"Error updating analytics charts: {e}")
                return tuple(go.Figure() for _ in range(5))

        # Report generation callback
        @self.app.callback(
            Output("generate-report-btn", "disabled"),
            [Input("report-type", "value"),
             Input("time-range", "value"),
             Input("report-sections", "value")]
        )
        def update_report_button(report_type, time_range, sections):
            return not all([report_type, time_range, sections])

    def _create_header(self, title):
        """Create page header with title"""
        return html.Div([
            html.H1(title, className="header-title fade-in"),
            html.P("Real-time monitoring and analysis", className="text-center mb-4 text-muted fade-in")
        ], className="text-center mb-5")

    def _inject_custom_css(self):
        """Inject custom CSS into the app"""
        self.app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>SOC Platform</title>
                {%favicon%}
                {%css%}
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
                <style>
                    :root {
                        --primary-color: #2c3e50;
                        --secondary-color: #34495e;
                        --accent-color: #3498db;
                        --background-color: #1a1a1a;
                        --card-bg: rgba(40, 44, 52, 0.95);
                        --text-color: #ecf0f1;
                        --text-muted: #95a5a6;
                        --success-color: #27ae60;
                        --warning-color: #f39c12;
                        --danger-color: #c0392b;
                        --info-color: #2980b9;
                    }
                    
                    body {
                        font-family: 'Inter', sans-serif;
                        background: var(--background-color);
                        color: var(--text-color);
                    }
                    
                    .card {
                        background: var(--card-bg);
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    
                    .card-header {
                        background: rgba(0, 0, 0, 0.2);
                        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                        padding: 1rem;
                        color: var(--text-color);
                    }
                    
                    .card-body {
                        background: var(--card-bg);
                        color: var(--text-color);
                    }
                    
                    .table {
                        color: var(--text-color) !important;
                    }
                    
                    .table-dark {
                        background-color: var(--card-bg) !important;
                    }
                    
                    .table-dark td,
                    .table-dark th {
                        color: var(--text-color) !important;
                        border-color: rgba(255, 255, 255, 0.1) !important;
                    }
                    
                    .list-group-item {
                        background: var(--card-bg) !important;
                        border-color: rgba(255, 255, 255, 0.1) !important;
                        color: var(--text-color) !important;
                    }
                    
                    .form-control {
                        background-color: rgba(255, 255, 255, 0.1) !important;
                        border-color: rgba(255, 255, 255, 0.1) !important;
                        color: var(--text-color) !important;
                    }
                    
                    .form-control:focus {
                        background-color: rgba(255, 255, 255, 0.15) !important;
                        border-color: var(--accent-color) !important;
                        color: var(--text-color) !important;
                    }
                    
                    .custom-control-label {
                        color: var(--text-color) !important;
                    }
                    
                    .custom-switch .custom-control-label::before {
                        background-color: rgba(255, 255, 255, 0.1) !important;
                    }
                    
                    .text-light {
                        color: var(--text-color) !important;
                    }
                    
                    .bg-dark {
                        background-color: var(--card-bg) !important;
                    }
                    
                    /* Additional styles for better visibility */
                    .checklist-option {
                        color: var(--text-color) !important;
                    }
                    
                    .custom-control-label::before,
                    .custom-control-label::after {
                        background-color: var(--accent-color) !important;
                    }
                    
                    .custom-switch .custom-control-input:checked ~ .custom-control-label::before {
                        background-color: var(--accent-color) !important;
                    }
                    
                    /* Ensure text contrast */
                    h1, h2, h3, h4, h5, h6, p, span, div {
                        color: var(--text-color);
                    }
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''

    def _create_dashboard_page(self):
        """Create the main dashboard page"""
        try:
            return dbc.Container([
                self._create_header("Security Operations Dashboard"),
                self._create_alert_section(),
                self._create_summary_cards(),
                dbc.Row([
                    dbc.Col([
                        self._create_threat_map(),
                        self._create_trend_analysis(),
                    ], md=8),
                    dbc.Col([
                        self._create_threat_distribution(),
                        self._create_recent_alerts(),
                    ], md=4),
                ], className="mb-4"),
                dbc.Row([
                    dbc.Col(self._create_threat_table(), md=12),
                ]),
                dcc.Interval(
                    id='interval-component',
                    interval=5*1000,
                    n_intervals=0
                ),
            ], fluid=True)
        except Exception as e:
            logger.error(f"Error creating dashboard page: {e}")
            return html.Div("Error loading dashboard")

    def _create_analytics_page(self):
        """Create the analytics page"""
        try:
            return dbc.Container([
                self._create_header("Threat Analytics"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Threat Intelligence Overview"),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='threat-intel-summary',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], className="mb-4"),
                        dbc.Card([
                            dbc.CardHeader("Attack Vector Analysis"),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='attack-vector-chart',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], className="mb-4")
                    ], md=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Severity Distribution"),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='severity-chart',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], className="mb-4"),
                        dbc.Card([
                            dbc.CardHeader("Detection Methods"),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='detection-methods-chart',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], className="mb-4")
                    ], md=6)
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Threat Timeline"),
                            dbc.CardBody([
                                dcc.Graph(
                                    id='threat-timeline',
                                    config={'displayModeBar': False}
                                )
                            ])
                        ], className="mb-4")
                    ], md=12)
                ]),
                dcc.Interval(
                    id='analytics-interval',
                    interval=10*1000,
                    n_intervals=0
                )
            ], fluid=True)
        except Exception as e:
            logger.error(f"Error creating analytics page: {e}")
            return html.Div("Error loading analytics")

    def _create_reports_page(self):
        """Create the reports page"""
        try:
            return dbc.Container([
                self._create_header("Security Reports"),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Generate Report"),
                            dbc.CardBody([
                                dbc.Form([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("Report Type"),
                                            dbc.Select(
                                                id="report-type",
                                                options=[
                                                    {"label": "Executive Summary", "value": "executive"},
                                                    {"label": "Incident Report", "value": "incident"},
                                                    {"label": "Threat Analysis", "value": "threat"},
                                                    {"label": "Compliance Report", "value": "compliance"},
                                                    {"label": "Performance Metrics", "value": "performance"}
                                                ],
                                                value="executive"
                                            )
                                        ], md=6),
                                        dbc.Col([
                                            dbc.Label("Time Range"),
                                            dbc.Select(
                                                id="time-range",
                                                options=[
                                                    {"label": "Last 24 Hours", "value": "24h"},
                                                    {"label": "Last 7 Days", "value": "7d"},
                                                    {"label": "Last 30 Days", "value": "30d"},
                                                    {"label": "Custom Range", "value": "custom"}
                                                ],
                                                value="24h"
                                            )
                                        ], md=6)
                                    ], className="mb-3"),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("Include Sections"),
                                            dbc.Checklist(
                                                id="report-sections",
                                                options=[
                                                    {"label": "Executive Summary", "value": "summary"},
                                                    {"label": "Threat Analysis", "value": "threats"},
                                                    {"label": "Incident Details", "value": "incidents"},
                                                    {"label": "Mitigation Actions", "value": "actions"},
                                                    {"label": "Recommendations", "value": "recommendations"}
                                                ],
                                                value=["summary", "threats", "incidents"]
                                            )
                                        ])
                                    ], className="mb-3"),
                                    dbc.Button(
                                        "Generate Report",
                                        id="generate-report-btn",
                                        color="primary",
                                        disabled=False
                                    )
                                ])
                            ])
                        ], className="mb-4")
                    ], md=12)
                ])
            ], fluid=True)
        except Exception as e:
            logger.error(f"Error creating reports page: {e}")
            return html.Div("Error loading reports")

    def _create_report_item(self, title, description, time, author):
        """Create a report list item"""
        return dbc.ListGroupItem([
            dbc.Row([
                dbc.Col([
                    html.H5(title, className="mb-1"),
                    html.P(description, className="mb-1"),
                    html.Small([
                        html.I(className="fas fa-clock mr-1"),
                        f"Generated {time} by {author}"
                    ], className="text-muted")
                ], md=9),
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button([
                            html.I(className="fas fa-download mr-1"),
                            "Download"
                        ], color="primary", size="sm", className="mr-2"),
                        dbc.Button([
                            html.I(className="fas fa-share-alt mr-1"),
                            "Share"
                        ], color="info", size="sm", className="mr-2"),
                        dbc.Button([
                            html.I(className="fas fa-trash-alt mr-1"),
                            "Delete"
                        ], color="danger", size="sm")
                    ], className="float-right")
                ], md=3, className="d-flex align-items-center")
            ])
        ])

    def _create_threat_hunting_page(self):
        """Create threat hunting page with enhanced functionality"""
        return dbc.Container([
            self._create_header("Threat Hunting"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Hunt Query Builder"),
                        dbc.CardBody([
                            dbc.Form([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Data Source"),
                                        dbc.Select(
                                            id="data-source",
                                            options=[
                                                {"label": "Network Logs", "value": "network"},
                                                {"label": "Endpoint Logs", "value": "endpoint"},
                                                {"label": "SIEM Events", "value": "siem"},
                                                {"label": "Threat Intel", "value": "intel"}
                                            ]
                                        )
                                    ], md=4),
                                    dbc.Col([
                                        dbc.Label("Time Range"),
                                        dbc.Select(
                                            id="hunt-time-range",
                                            options=[
                                                {"label": "Last Hour", "value": "1h"},
                                                {"label": "Last 24 Hours", "value": "24h"},
                                                {"label": "Last 7 Days", "value": "7d"},
                                                {"label": "Custom", "value": "custom"}
                                            ]
                                        )
                                    ], md=4),
                                    dbc.Col([
                                        dbc.Label("Hunt Type"),
                                        dbc.Select(
                                            id="hunt-type",
                                            options=[
                                                {"label": "IOC Search", "value": "ioc"},
                                                {"label": "Behavior Analysis", "value": "behavior"},
                                                {"label": "Pattern Match", "value": "pattern"},
                                                {"label": "Anomaly Detection", "value": "anomaly"}
                                            ]
                                        )
                                    ], md=4)
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Search Query"),
                                        dbc.Textarea(
                                            id="hunt-query",
                                            placeholder="Enter your hunt query...",
                                            style={"height": "100px"}
                                        )
                                    ])
                                ], className="mb-3"),
                                dbc.Button([
                                    html.I(className="fas fa-search mr-2"),
                                    "Start Hunt"
                                ], color="primary")
                            ])
                        ])
                    ], className="mb-4")
                ], md=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Active Hunts"),
                        dbc.CardBody([
                            dbc.ListGroup([
                                self._create_hunt_item(
                                    "Ransomware Behavior Detection",
                                    "Hunting for signs of ransomware activity",
                                    "In Progress",
                                    "75"
                                ),
                                self._create_hunt_item(
                                    "C2 Communication Pattern",
                                    "Detecting potential command & control traffic",
                                    "Completed",
                                    "100"
                                ),
                                self._create_hunt_item(
                                    "Data Exfiltration",
                                    "Identifying unusual data transfers",
                                    "In Progress",
                                    "45"
                                )
                            ])
                        ])
                    ])
                ], md=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Hunt Results"),
                        dbc.CardBody([
                            dbc.Tabs([
                                dbc.Tab([
                                    html.Div([
                                        html.H5("Findings", className="mb-3"),
                                        dbc.ListGroup([
                                            self._create_finding_item(
                                                "Suspicious PowerShell Activity",
                                                "Multiple encoded commands detected",
                                                "High"
                                            ),
                                            self._create_finding_item(
                                                "Unusual Network Connection",
                                                "Connection to known malicious IP",
                                                "Critical"
                                            ),
                                            self._create_finding_item(
                                                "Registry Modification",
                                                "Persistence mechanism detected",
                                                "Medium"
                                            )
                                        ])
                                    ], className="mt-3")
                                ], label="Findings"),
                                dbc.Tab([
                                    dcc.Graph(
                                        figure=self._create_hunt_metrics(),
                                        config={'displayModeBar': False}
                                    )
                                ], label="Metrics")
                            ])
                        ])
                    ])
                ], md=6)
            ])
        ], fluid=True)

    def _create_hunt_item(self, title, description, status, progress):
        """Create a hunt list item"""
        status_colors = {
            "In Progress": "warning",
            "Completed": "success",
            "Failed": "danger"
        }
        return dbc.ListGroupItem([
            html.Div([
                html.H5(title, className="mb-1"),
                html.P(description, className="mb-1"),
                dbc.Progress(
                    value=int(progress),
                    color=status_colors.get(status, "primary"),
                    className="mb-2",
                    style={"height": "4px"}
                ),
                html.Div([
                    dbc.Badge(status, color=status_colors.get(status, "primary"), className="mr-2"),
                    html.Small(f"Progress: {progress}%", className="text-muted")
                ])
            ])
        ])

    def _create_finding_item(self, title, description, severity):
        """Create a finding list item"""
        severity_colors = {
            "Critical": "danger",
            "High": "warning",
            "Medium": "info",
            "Low": "success"
        }
        return dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.H6(title, className="mb-1"),
                    html.Small(description, className="text-muted")
                ]),
                dbc.Badge(severity, color=severity_colors.get(severity, "primary"))
            ], className="d-flex justify-content-between align-items-center")
        ])

    def _create_hunt_metrics(self):
        """Create hunt metrics visualization"""
        # Sample data for hunt metrics
        categories = ['IOCs Found', 'False Positives', 'True Positives', 'Pending Review']
        values = [45, 15, 25, 5]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['#3498db', '#e74c3c', '#2ecc71', '#f1c40f']
            )
        ])
        
        fig.update_layout(
            title='Hunt Metrics Overview',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        return fig

    def _create_incidents_page(self):
        """Create incidents page with enhanced functionality"""
        return dbc.Container([
            self._create_header("Incident Management"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Active Incidents"),
                        dbc.CardBody([
                            dbc.Tabs([
                                dbc.Tab([
                                    self._create_incident_table()
                                ], label="All Incidents"),
                                dbc.Tab([
                                    self._create_incident_timeline()
                                ], label="Timeline"),
                                dbc.Tab([
                                    self._create_incident_metrics()
                                ], label="Metrics")
                            ])
                        ])
                    ], className="mb-4")
                ], md=12)
            ]),
            dbc.Row([
                dbc.Col([
                    self._create_incident_details()
                ], md=8),
                dbc.Col([
                    self._create_incident_actions()
                ], md=4)
            ])
        ], fluid=True)

    def _create_incident_table(self):
        """Create incident table with filtering and sorting"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Input(
                        id="incident-search",
                        placeholder="Search incidents...",
                        type="text",
                        className="mb-3"
                    )
                ], md=6),
                dbc.Col([
                    dbc.Select(
                        id="incident-filter",
                        options=[
                            {"label": "All Incidents", "value": "all"},
                            {"label": "Critical", "value": "critical"},
                            {"label": "High", "value": "high"},
                            {"label": "Medium", "value": "medium"},
                            {"label": "Low", "value": "low"}
                        ],
                        value="all",
                        className="mb-3"
                    )
                ], md=3),
                dbc.Col([
                    dbc.Select(
                        id="incident-sort",
                        options=[
                            {"label": "Newest First", "value": "newest"},
                            {"label": "Oldest First", "value": "oldest"},
                            {"label": "Highest Severity", "value": "severity"},
                            {"label": "Status", "value": "status"}
                        ],
                        value="newest",
                        className="mb-3"
                    )
                ], md=3)
            ]),
            dbc.Table([
                html.Thead([
                    html.Tr([
                        html.Th("ID"),
                        html.Th("Title"),
                        html.Th("Severity"),
                        html.Th("Status"),
                        html.Th("Assigned To"),
                        html.Th("Last Updated"),
                        html.Th("Actions")
                    ])
                ]),
                html.Tbody([
                    self._create_incident_row(
                        "INC-001",
                        "Ransomware Attack",
                        "Critical",
                        "Active",
                        "John Doe",
                        "10 min ago"
                    ),
                    self._create_incident_row(
                        "INC-002",
                        "Phishing Campaign",
                        "High",
                        "Investigating",
                        "Jane Smith",
                        "30 min ago"
                    ),
                    self._create_incident_row(
                        "INC-003",
                        "Data Exfiltration",
                        "High",
                        "Contained",
                        "Mike Johnson",
                        "1 hour ago"
                    )
                ])
            ], bordered=True, hover=True, responsive=True, striped=True)
        ])

    def _create_incident_row(self, id, title, severity, status, assigned, updated):
        """Create an incident table row"""
        severity_colors = {
            "Critical": "danger",
            "High": "warning",
            "Medium": "info",
            "Low": "success"
        }
        status_colors = {
            "Active": "danger",
            "Investigating": "warning",
            "Contained": "info",
            "Resolved": "success"
        }
        return html.Tr([
            html.Td(id),
            html.Td(title),
            html.Td(dbc.Badge(severity, color=severity_colors.get(severity, "primary"))),
            html.Td(dbc.Badge(status, color=status_colors.get(status, "primary"))),
            html.Td(assigned),
            html.Td(updated),
            html.Td(
                dbc.ButtonGroup([
                    dbc.Button("View", color="primary", size="sm", className="mr-1"),
                    dbc.Button("Update", color="warning", size="sm", className="mr-1"),
                    dbc.Button("Close", color="danger", size="sm")
                ])
            )
        ])

    def _create_incident_metrics(self):
        """Create incident metrics visualization"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=self._create_incident_severity_chart(),
                        config={'displayModeBar': False}
                    )
                ], md=6),
                dbc.Col([
                    dcc.Graph(
                        figure=self._create_incident_status_chart(),
                        config={'displayModeBar': False}
                    )
                ], md=6)
            ], className="mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure=self._create_incident_trend_chart(),
                        config={'displayModeBar': False}
                    )
                ], md=12)
            ])
        ])

    def _create_incident_severity_chart(self):
        """Create incident severity distribution chart"""
        labels = ['Critical', 'High', 'Medium', 'Low']
        values = [5, 12, 25, 8]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=['#e74c3c', '#f39c12', '#3498db', '#2ecc71'])
        )])
        
        fig.update_layout(
            title='Incident Severity Distribution',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        
        return fig

    def _create_incident_status_chart(self):
        """Create incident status distribution chart"""
        x = ['Active', 'Investigating', 'Contained', 'Resolved']
        y = [8, 15, 10, 20]
        
        fig = go.Figure(data=[go.Bar(
            x=x,
            y=y,
            marker_color=['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
        )])
        
        fig.update_layout(
            title='Incident Status Distribution',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        return fig

    def _create_incident_trend_chart(self):
        """Create incident trend chart"""
        dates = pd.date_range(start='2024-01-01', periods=14)
        incidents = np.random.randint(5, 20, size=14)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=incidents,
            mode='lines+markers',
            line=dict(color='#3498db', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title='Incident Trend (Last 14 Days)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            xaxis_title='Date',
            yaxis_title='Number of Incidents'
        )
        
        return fig

    def _create_incident_actions(self):
        """Create incident actions panel"""
        return dbc.Card([
            dbc.CardHeader("Response Actions"),
            dbc.CardBody([
                dbc.ButtonGroup([
                    dbc.Button([
                        html.I(className="fas fa-shield-alt mr-2"),
                        "Isolate System"
                    ], color="warning", className="mb-2 w-100"),
                    dbc.Button([
                        html.I(className="fas fa-ban mr-2"),
                        "Block IOCs"
                    ], color="danger", className="mb-2 w-100"),
                    dbc.Button([
                        html.I(className="fas fa-envelope mr-2"),
                        "Send Alert"
                    ], color="info", className="mb-2 w-100")
                ], vertical=True),
                html.Hr(),
                html.H6("Playbook Steps", className="mb-3"),
                dbc.ListGroup([
                    self._create_playbook_step(
                        "1. Initial Response",
                        "Isolate affected systems",
                        "Completed"
                    ),
                    self._create_playbook_step(
                        "2. Investigation",
                        "Collect and analyze evidence",
                        "In Progress"
                    ),
                    self._create_playbook_step(
                        "3. Containment",
                        "Implement containment measures",
                        "Pending"
                    ),
                    self._create_playbook_step(
                        "4. Eradication",
                        "Remove threat from systems",
                        "Pending"
                    )
                ], flush=True)
            ])
        ])

    def _create_playbook_step(self, title, description, status):
        """Create a playbook step item"""
        status_colors = {
            "Completed": "success",
            "In Progress": "warning",
            "Pending": "secondary",
            "Failed": "danger"
        }
        return dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.H6(title, className="mb-1"),
                    html.Small(description, className="text-muted")
                ]),
                dbc.Badge(status, color=status_colors.get(status, "primary"))
            ], className="d-flex justify-content-between align-items-center")
        ])

    def _create_training_page(self):
        """Create training page with enhanced functionality"""
        return dbc.Container([
            self._create_header("SOC Training"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Training Modules"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    self._create_training_card(
                                        "Incident Response",
                                        "Learn effective incident response procedures",
                                        ["IR Process", "Evidence Collection", "Documentation"],
                                        "4 hours",
                                        "Beginner"
                                    )
                                ], md=6),
                                dbc.Col([
                                    self._create_training_card(
                                        "Threat Hunting",
                                        "Advanced threat hunting techniques",
                                        ["IOC Analysis", "YARA Rules", "Memory Forensics"],
                                        "8 hours",
                                        "Advanced"
                                    )
                                ], md=6)
                            ], className="mb-4"),
                            dbc.Row([
                                dbc.Col([
                                    self._create_training_card(
                                        "Malware Analysis",
                                        "Learn malware analysis fundamentals",
                                        ["Static Analysis", "Dynamic Analysis", "Reverse Engineering"],
                                        "12 hours",
                                        "Intermediate"
                                    )
                                ], md=6),
                                dbc.Col([
                                    self._create_training_card(
                                        "Digital Forensics",
                                        "Master digital forensics techniques",
                                        ["Disk Forensics", "Network Forensics", "Memory Analysis"],
                                        "16 hours",
                                        "Advanced"
                                    )
                                ], md=6)
                            ])
                        ])
                    ], className="mb-4")
                ], md=12)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Training Progress"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.H5("Overall Progress", className="mb-3"),
                                    dbc.Progress([
                                        dbc.Progress(value=40, color="success", bar=True),
                                        dbc.Progress(value=35, color="warning", bar=True),
                                        dbc.Progress(value=25, color="danger", bar=True)
                                    ], className="mb-3", style={"height": "2rem"}),
                                    html.Div([
                                        dbc.Badge("Completed (40%)", color="success", className="mr-2"),
                                        dbc.Badge("In Progress (35%)", color="warning", className="mr-2"),
                                        dbc.Badge("Not Started (25%)", color="danger")
                                    ], className="mb-4")
                                ])
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        figure=self._create_training_metrics(),
                                        config={'displayModeBar': False}
                                    )
                                ])
                            ])
                        ])
                    ])
                ], md=8),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Upcoming Sessions"),
                        dbc.CardBody([
                            dbc.ListGroup([
                                self._create_session_item(
                                    "Incident Response Workshop",
                                    "Jan 15, 2024 10:00 AM",
                                    "John Doe",
                                    15
                                ),
                                self._create_session_item(
                                    "Threat Hunting Lab",
                                    "Jan 16, 2024 2:00 PM",
                                    "Jane Smith",
                                    8
                                ),
                                self._create_session_item(
                                    "Malware Analysis Demo",
                                    "Jan 17, 2024 11:00 AM",
                                    "Mike Johnson",
                                    12
                                )
                            ])
                        ])
                    ])
                ], md=4)
            ])
        ], fluid=True)

    def _create_session_item(self, title, time, instructor, spots):
        """Create a training session item"""
        return dbc.ListGroupItem([
            html.Div([
                html.H6(title, className="mb-1"),
                html.Small([
                    html.I(className="fas fa-clock mr-1"),
                    time
                ], className="text-muted d-block"),
                html.Small([
                    html.I(className="fas fa-user mr-1"),
                    f"Instructor: {instructor}"
                ], className="text-muted d-block"),
                html.Small([
                    html.I(className="fas fa-users mr-1"),
                    f"Available Spots: {spots}"
                ], className="text-muted d-block")
            ], className="mb-2"),
            dbc.Button("Register", color="primary", size="sm")
        ])

    def _create_training_metrics(self):
        """Create training metrics visualization"""
        categories = ['Completed', 'In Progress', 'Scheduled', 'Available']
        values = [12, 8, 5, 15]
        
        fig = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            marker_color=['#2ecc71', '#f1c40f', '#3498db', '#95a5a6']
        )])
        
        fig.update_layout(
            title='Training Module Status',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        return fig

    def _create_settings_page(self):
        """Create settings page with enhanced functionality"""
        try:
            notification_settings = dbc.Card([
                dbc.CardHeader("Notification Settings", className="bg-dark text-light"),
                dbc.CardBody([
                    html.H5("Alert Notifications", className="mb-3 text-light"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Critical Alerts", className="text-light"),
                            dbc.Checklist(
                                id="critical-alerts",
                                options=[
                                    {"label": "Email", "value": "email"},
                                    {"label": "SMS", "value": "sms"},
                                    {"label": "Slack", "value": "slack"},
                                    {"label": "Teams", "value": "teams"}
                                ],
                                value=["email", "sms", "slack"],
                                switch=True,
                                className="text-light"
                            ),
                        ], width=12, className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("High Priority Alerts", className="text-light"),
                            dbc.Checklist(
                                id="high-alerts",
                                options=[
                                    {"label": "Email", "value": "email"},
                                    {"label": "SMS", "value": "sms"},
                                    {"label": "Slack", "value": "slack"},
                                    {"label": "Teams", "value": "teams"}
                                ],
                                value=["email", "slack"],
                                switch=True,
                                className="text-light"
                            ),
                        ], width=12, className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Medium Priority Alerts", className="text-light"),
                            dbc.Checklist(
                                id="medium-alerts",
                                options=[
                                    {"label": "Email", "value": "email"},
                                    {"label": "Slack", "value": "slack"},
                                    {"label": "Teams", "value": "teams"}
                                ],
                                value=["email"],
                                switch=True,
                                className="text-light"
                            ),
                        ], width=12, className="mb-3"),
                    ]),
                ], className="bg-dark")
            ], className="mb-4 border-0")

            return dbc.Container([
                self._create_header("System Settings"),
                dbc.Row([
                    dbc.Col(notification_settings, md=6),
                    dbc.Col(self._create_integration_settings(), md=6)
                ]),
                dbc.Row([
                    dbc.Col(self._create_user_management(), md=12)
                ])
            ], fluid=True)
        except Exception as e:
            logger.error(f"Error creating settings page: {str(e)}")
            return html.Div([
                html.H4("Error Loading Settings Page", className="text-light text-center mb-3"),
                html.P(f"An error occurred: {str(e)}", className="text-light text-center"),
                dbc.Button("Refresh Page", color="primary", className="d-block mx-auto", id="refresh-settings")
            ], className="p-5")

    def _create_integration_settings(self):
        """Create integration settings card"""
        return dbc.Card([
            dbc.CardHeader("Integration Settings", className="bg-dark text-light"),
            dbc.CardBody([
                html.H5("External Integrations", className="mb-3 text-light"),
                dbc.ListGroup([
                    self._create_integration_item(
                        "SIEM Integration",
                        "Connected to Splunk Enterprise",
                        "Connected",
                        "success"
                    ),
                    self._create_integration_item(
                        "Threat Intel Platform",
                        "Connected to AlienVault OTX",
                        "Connected",
                        "success"
                    ),
                    self._create_integration_item(
                        "Ticketing System",
                        "Connected to ServiceNow",
                        "Connected",
                        "success"
                    ),
                    self._create_integration_item(
                        "Email Security",
                        "Connection Failed",
                        "Error",
                        "danger"
                    )
                ], flush=True, className="bg-dark")
            ], className="bg-dark")
        ], className="mb-4 border-0")

    def _create_user_management(self):
        """Create user management card"""
        return dbc.Card([
            dbc.CardHeader("User Management", className="bg-dark text-light"),
            dbc.CardBody([
                html.H5("Active Users", className="mb-3 text-light"),
                dbc.Table([
                    html.Thead([
                        html.Tr([
                            html.Th("User", className="text-light"),
                            html.Th("Role", className="text-light"),
                            html.Th("Status", className="text-light"),
                            html.Th("Last Active", className="text-light"),
                            html.Th("Actions", className="text-light")
                        ], className="bg-dark")
                    ]),
                    html.Tbody([
                        self._create_user_row(
                            "John Doe",
                            "Admin",
                            "Active",
                            "5 min ago"
                        ),
                        self._create_user_row(
                            "Jane Smith",
                            "Analyst",
                            "Active",
                            "10 min ago"
                        ),
                        self._create_user_row(
                            "Mike Johnson",
                            "Analyst",
                            "Inactive",
                            "1 hour ago"
                        )
                    ])
                ], bordered=True, hover=True, responsive=True, striped=True, 
                className="text-light bg-dark table-dark")
            ], className="bg-dark")
        ], className="border-0")

    def _create_integration_item(self, title, description, status, status_color):
        """Create an integration list item"""
        return dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.H6(title, className="mb-1 text-light"),
                    html.Small(description, className="text-muted")
                ]),
                html.Div([
                    dbc.Badge(status, color=status_color, className="mr-2"),
                    dbc.Button("Configure", color="primary", size="sm")
                ])
            ], className="d-flex justify-content-between align-items-center")
        ], className="bg-dark")

    def _create_user_row(self, name, role, status, last_active):
        """Create a user table row"""
        status_colors = {
            "Active": "success",
            "Inactive": "secondary"
        }
        return html.Tr([
            html.Td([
                html.I(className="fas fa-user-circle mr-2"),
                name
            ], className="text-light"),
            html.Td(role, className="text-light"),
            html.Td(dbc.Badge(status, color=status_colors[status])),
            html.Td(last_active, className="text-light"),
            html.Td([
                dbc.ButtonGroup([
                    dbc.Button("Edit", color="primary", size="sm", className="mr-1"),
                    dbc.Button("Disable", color="danger", size="sm")
                ])
            ])
        ])

    def _create_alert_section(self):
        """Create alert section with real-time alerts"""
        return dbc.Row([
            dbc.Col(
                dbc.Alert([
                    html.I(className="fas fa-exclamation-triangle mr-2"),
                    "Active Threats Detected",
                    html.Span("3 High Risk", className="ml-2 badge bg-danger")
                ],
                color="warning",
                className="alert-pulse mb-4"),
            )
        ])

    def _create_summary_cards(self):
        """Create summary cards with key metrics"""
        return dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-exclamation-circle fa-2x text-danger mb-2"),
                            html.H2(id="active-threats-count", className="stat-value"),
                            html.P("Active Threats", className="stat-label")
                        ], className="text-center")
                    ])
                ], className="mb-4"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x text-warning mb-2"),
                            html.H2(id="risk-level", className="stat-value"),
                            html.P("Risk Level", className="stat-label")
                        ], className="text-center")
                    ])
                ], className="mb-4"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-shield-alt fa-2x text-success mb-2"),
                            html.H2(id="mitigated-count", className="stat-value"),
                            html.P("Threats Mitigated", className="stat-label")
                        ], className="text-center")
                    ])
                ], className="mb-4"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className="fas fa-bell fa-2x text-info mb-2"),
                            html.H2(id="alerts-count", className="stat-value"),
                            html.P("Active Alerts", className="stat-label")
                        ], className="text-center")
                    ])
                ], className="mb-4"),
                md=3
            )
        ])

    def _create_threat_map(self):
        """Create threat map visualization"""
        return dbc.Card([
            dbc.CardHeader([
                html.H3("Global Threat Distribution", className="mb-0"),
                html.Small("Real-time geographic threat monitoring", className="text-muted")
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id="threat-map",
                    config={'displayModeBar': False}
                )
            ])
        ], className="mb-4")

    def _create_trend_analysis(self):
        """Create trend analysis visualization"""
        return dbc.Card([
            dbc.CardHeader([
                html.H3("Threat Trend Analysis", className="mb-0"),
                html.Small("24-hour threat activity pattern", className="text-muted")
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id="trend-analysis",
                    config={'displayModeBar': False}
                )
            ])
        ])

    def _create_threat_distribution(self):
        """Create threat distribution visualization"""
        return dbc.Card([
            dbc.CardHeader([
                html.H3("Threat Categories", className="mb-0"),
                html.Small("Distribution by type", className="text-muted")
            ]),
            dbc.CardBody([
                dcc.Graph(
                    id="threat-distribution",
                    config={'displayModeBar': False}
                )
            ])
        ], className="mb-4")

    def _create_recent_alerts(self):
        """Create recent alerts panel"""
        return dbc.Card([
            dbc.CardHeader([
                html.H3("Recent Alerts", className="mb-0"),
                html.Small("Last 5 security alerts", className="text-muted")
            ]),
            dbc.CardBody([
                html.Div(id="recent-alerts-content")
            ])
        ])

    def _create_threat_table(self):
        """Create threat table"""
        return dbc.Card([
            dbc.CardHeader([
                html.H3("Detailed Threat Analysis", className="mb-0"),
                html.Small("Comprehensive threat information", className="text-muted")
            ]),
            dbc.CardBody([
                html.Div(id="threat-table-content")
            ])
        ])

    def _create_threat_intel_visualization(self, df):
        """Create threat intelligence visualization"""
        try:
            # Create bubble chart for threat types and sources
            source_type_counts = df.groupby(['source', 'type']).size().reset_index(name='count')
            
            fig = px.scatter(source_type_counts,
                           x='source',
                           y='type',
                           size='count',
                           color='count',
                           color_continuous_scale='Viridis',
                           title='Threat Intelligence Overview')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating threat intel visualization: {e}")
            return go.Figure()

    def _create_attack_vector_visualization(self, df):
        """Create attack vector visualization"""
        try:
            # Create sunburst chart for attack vectors
            vector_severity = df.groupby(['vector', 'severity']).size().reset_index(name='count')
            
            fig = px.sunburst(vector_severity,
                            path=['vector', 'severity'],
                            values='count',
                            color='count',
                            color_continuous_scale='Viridis',
                            title='Attack Vector Distribution')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating attack vector visualization: {e}")
            return go.Figure()

    def _create_severity_visualization(self, df):
        """Create severity visualization"""
        try:
            # Create stacked bar chart for severity and status
            severity_status = df.groupby(['severity', 'status']).size().reset_index(name='count')
            
            fig = px.bar(severity_status,
                        x='severity',
                        y='count',
                        color='status',
                        title='Threat Severity Distribution',
                        barmode='stack')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating severity visualization: {e}")
            return go.Figure()

    def _create_detection_visualization(self, df):
        """Create detection methods visualization"""
        try:
            # Create scatter plot for detection methods
            detection_metrics = df.groupby('detection_method').agg({
                'confidence': 'mean',
                'id': 'count'
            }).reset_index()
            
            detection_metrics.columns = ['method', 'avg_confidence', 'count']
            
            fig = px.scatter(detection_metrics,
                           x='avg_confidence',
                           y='count',
                           text='method',
                           size='count',
                           color='avg_confidence',
                           title='Detection Methods Effectiveness')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating detection visualization: {e}")
            return go.Figure()

    def _create_timeline_visualization(self, df):
        """Create timeline visualization"""
        try:
            # Create line chart for threats over time
            df['time'] = pd.to_datetime(df['time'])
            timeline_data = df.groupby(['time', 'severity']).size().reset_index(name='count')
            
            fig = px.line(timeline_data,
                         x='time',
                         y='count',
                         color='severity',
                         title='Threat Activity Timeline')
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                showlegend=False,
                xaxis_title='Date',
                yaxis_title='Number of Threats'
            )
            
            return fig
        except Exception as e:
            logger.error(f"Error creating timeline visualization: {e}")
            return go.Figure()

    def _create_training_card(self, title, description, topics, duration, level):
        """Create a training module card"""
        level_colors = {
            "Beginner": "success",
            "Intermediate": "warning",
            "Advanced": "danger"
        }
        return dbc.Card([
            dbc.CardBody([
                html.H5(title, className="mb-2"),
                dbc.Badge(level, color=level_colors.get(level, "primary"), className="mb-2"),
                html.P(description, className="mb-3"),
                html.H6("Topics Covered:", className="mb-2"),
                html.Ul([html.Li(topic) for topic in topics], className="mb-3"),
                html.Div([
                    html.Small(f"Duration: {duration}", className="text-muted"),
                    dbc.Button("Start Training", color="primary", size="sm")
                ], className="d-flex justify-content-between align-items-center")
            ])
        ], className="mb-4")

    def _create_incident_timeline(self):
        """Create incident timeline visualization"""
        events = [
            {
                "title": "Initial Detection",
                "time": "2024-01-14 15:30:00",
                "description": "Suspicious activity detected in network logs",
                "type": "detection"
            },
            {
                "title": "Investigation Started",
                "time": "2024-01-14 15:35:00",
                "description": "SOC team began initial investigation",
                "type": "investigation"
            },
            {
                "title": "Containment Measures",
                "time": "2024-01-14 15:40:00",
                "description": "Implemented network isolation for affected systems",
                "type": "containment"
            },
            {
                "title": "Root Cause Analysis",
                "time": "2024-01-14 15:45:00",
                "description": "Identified compromised credentials as entry point",
                "type": "analysis"
            }
        ]
        
        return dbc.Card([
            dbc.CardHeader("Incident Timeline"),
            dbc.CardBody([
                dbc.ListGroup([
                    self._create_timeline_event(**event) for event in events
                ], flush=True)
            ])
        ], className="mb-4")

    def _create_timeline_event(self, title, time, description, type):
        """Create a timeline event item"""
        type_icons = {
            "detection": "fas fa-exclamation-circle text-danger",
            "investigation": "fas fa-search text-info",
            "containment": "fas fa-shield-alt text-warning",
            "analysis": "fas fa-microscope text-success"
        }
        return dbc.ListGroupItem([
            html.Div([
                html.Div([
                    html.I(className=type_icons.get(type, "fas fa-circle"), style={"width": "20px"}),
                    html.Div([
                        html.H6(title, className="mb-1"),
                        html.Small(time, className="text-muted d-block"),
                        html.P(description, className="mb-0 mt-2")
                    ], className="ml-3")
                ], className="d-flex")
            ], className="p-2")
        ])

    def _create_incident_details(self):
        """Create incident details interface"""
        return dbc.Card([
            dbc.CardHeader("Incident Details"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5("Current Incident", className="mb-3"),
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.H4("INC-2024-001", className="mb-2"),
                                    dbc.Badge("Critical", color="danger", className="mb-3"),
                                    html.P("Ransomware Attack Attempt", className="mb-2"),
                                    html.Small("Detected: 2024-01-14 15:30:00", className="text-muted d-block"),
                                    html.Small("Status: Active Investigation", className="text-muted d-block"),
                                    html.Hr(),
                                    html.H6("Affected Systems", className="mb-2"),
                                    dbc.ListGroup([
                                        dbc.ListGroupItem("WS-001 (192.168.1.100)"),
                                        dbc.ListGroupItem("WS-002 (192.168.1.101)"),
                                        dbc.ListGroupItem("SRV-001 (192.168.1.10)")
                                    ], flush=True)
                                ])
                            ])
                        ])
                    ], md=6),
                    dbc.Col([
                        html.H5("Impact Assessment", className="mb-3"),
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    self._create_impact_metric("Systems Affected", "3", "warning"),
                                    self._create_impact_metric("Data at Risk", "250GB", "danger"),
                                    self._create_impact_metric("Services Impacted", "2", "warning"),
                                    self._create_impact_metric("Users Affected", "15", "info")
                                ])
                            ])
                        ]),
                        html.H5("Risk Assessment", className="mb-3 mt-4"),
                        dbc.Progress(value=75, color="danger", className="mb-2",
                                   label="Business Impact"),
                        dbc.Progress(value=60, color="warning", className="mb-2",
                                   label="Data Loss Risk"),
                        dbc.Progress(value=40, color="info", className="mb-2",
                                   label="Spread Risk"),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([
                                html.H5("Technical Details", className="mb-3"),
                                dbc.Card([
                                    dbc.CardBody([
                                        html.Pre("""
Incident Type: Ransomware Attack Attempt
Initial Vector: Phishing Email
Malware Family: LockBit
C2 Servers: 
- 185.234.xxx.xxx
- 192.168.xxx.xxx
Encrypted Extensions: .locked, .encrypted
IOCs:
- Hash: d41d8cd98f00b204e9800998ecf8427e
- Domain: evil-domain.com
- IP: 192.168.1.100
                                        """, className="mb-0")
                                    ])
                                ])
                            ])
                        ])
                    ], md=6)
                ])
            ])
        ], className="mb-4")

    def _create_impact_metric(self, label, value, color):
        """Create an impact metric display"""
        return html.Div([
            html.H6(label, className="mb-1"),
            html.H4([
                value,
                dbc.Badge("", className=f"ml-2 bg-{color}", 
                         style={"width": "10px", "height": "10px", "border-radius": "50%"})
            ], className="mb-3")
        ]) 