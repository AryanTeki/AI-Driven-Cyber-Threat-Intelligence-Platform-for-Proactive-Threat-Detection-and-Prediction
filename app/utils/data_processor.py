import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta

def preprocess_threat_data(df):
    """Preprocess threat data for analysis"""
    # Convert timestamps
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculate time-based features
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Encode categorical variables
    df = pd.get_dummies(df, columns=['threat_type', 'severity', 'attack_vector'])
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_cols = ['risk_score', 'confidence_score']
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    
    return df

def calculate_threat_metrics(df):
    """Calculate various threat metrics"""
    metrics = {
        'total_threats': len(df),
        'high_severity': len(df[df['severity'] == 'High']),
        'avg_risk_score': df['risk_score'].mean(),
        'threat_types': df['threat_type'].value_counts().to_dict(),
        'geographic_distribution': get_geographic_distribution(df)
    }
    return metrics

def get_geographic_distribution(df):
    """Calculate geographic distribution of threats"""
    return df.groupby(['latitude', 'longitude']).size().to_dict() 