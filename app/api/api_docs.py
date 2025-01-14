from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# API Models
class ThreatData(BaseModel):
    alert_id: str
    timestamp: datetime
    threat_type: str
    severity: str
    source_ip: str
    description: str
    indicators: List[str]
    confidence_score: float

class AnalysisResult(BaseModel):
    threat_class: str
    risk_score: float
    recommended_actions: List[str]
    is_anomaly: bool
    related_threats: List[str]

# API Documentation
api_description = """
# Cyber Threat Intelligence API

This API provides access to the threat intelligence platform's features and data.

## Features

* Real-time threat detection and analysis
* Historical threat data querying
* Threat intelligence reporting
* Alert management
* System health monitoring

## Authentication

All API endpoints require authentication using JWT tokens.
"""

tags_metadata = [
    {
        "name": "threats",
        "description": "Operations with threat data",
    },
    {
        "name": "analytics",
        "description": "Threat analysis operations",
    },
    {
        "name": "reports",
        "description": "Report generation and management",
    },
]

app = FastAPI(
    title="Cyber Threat Intelligence API",
    description=api_description,
    version="1.0.0",
    openapi_tags=tags_metadata
) 