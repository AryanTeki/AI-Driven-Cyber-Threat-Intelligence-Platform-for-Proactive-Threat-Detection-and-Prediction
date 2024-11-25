# app/modules/ml_classifier.py

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class ThreatClassifier:
    def __init__(self):
        self.model = LogisticRegression(random_state=42)
        self.scaler = StandardScaler()
        self._train_initial_model()
        
    def _train_initial_model(self):
        """Train the model with initial simulated data."""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        
        # Features: severity_score, confidence_score
        X = np.random.rand(n_samples, 2)
        X[:, 0] *= 10  # Scale severity score to 0-10
        
        # Generate labels based on severity and confidence
        y = np.where((X[:, 0] * X[:, 1]) > 5, 'Critical',
             np.where((X[:, 0] * X[:, 1]) > 3, 'High',
             np.where((X[:, 0] * X[:, 1]) > 1, 'Medium', 'Low')))
        
        # Fit scaler
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
    
    def predict_severity(self, severity_score, confidence_score):
        """Predict threat severity based on severity and confidence scores."""
        features = np.array([[severity_score, confidence_score]])
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        return {
            'prediction': prediction,
            'confidence': float(max(probabilities)),
            'probabilities': {
                label: float(prob)
                for label, prob in zip(self.model.classes_, probabilities)
            }
        }