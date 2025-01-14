from typing import List, Dict, Union
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.svm import OneClassSVM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from datetime import datetime, timedelta
import re

class TextClassifier:
    """Simple text classifier using TF-IDF and Naive Bayes"""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = MultinomialNB()
        self.is_trained = False
        self._init_training_data()
    
    def _init_training_data(self):
        """Initialize with some basic training data"""
        self.training_texts = [
            "malware detected in system files",
            "suspicious executable downloaded",
            "ransomware encryption detected",
            "phishing email received",
            "credential theft attempt",
            "ddos attack detected",
            "high traffic volume",
            "port scanning detected"
        ]
        self.training_labels = [
            "malware",
            "malware",
            "ransomware",
            "phishing",
            "phishing",
            "ddos",
            "ddos",
            "reconnaissance"
        ]
        
        # Train initial model
        self._train_model()
    
    def _train_model(self):
        """Train the text classification model"""
        if not self.training_texts:
            return
        
        X = self.vectorizer.fit_transform(self.training_texts)
        self.classifier.fit(X, self.training_labels)
        self.is_trained = True
    
    def classify(self, text: str) -> Dict:
        """Classify text and return prediction with confidence"""
        if not self.is_trained:
            return {'label': 'unknown', 'confidence': 0.0}
        
        # Transform text
        X = self.vectorizer.transform([text])
        
        # Get prediction and probability
        label = self.classifier.predict(X)[0]
        probs = self.classifier.predict_proba(X)[0]
        confidence = max(probs)
        
        return {
            'label': label,
            'confidence': float(confidence)
        }
    
    def add_training_data(self, text: str, label: str):
        """Add new training data and retrain model"""
        self.training_texts.append(text)
        self.training_labels.append(label)
        self._train_model()

class AdvancedThreatDetector:
    """Advanced threat detection using ensemble methods"""
    def __init__(self):
        self.rf_classifier = RandomForestClassifier(n_estimators=100)
        self.threat_patterns = self._load_threat_patterns()
        self.threshold = 0.85
    
    def _load_threat_patterns(self) -> Dict:
        """Load known threat patterns and signatures"""
        return {
            'malware': [
                r'suspicious_exe_pattern',
                r'known_malware_signature',
                r'unusual_system_calls'
            ],
            'phishing': [
                r'suspicious_url_pattern',
                r'credential_theft_attempt',
                r'social_engineering_keywords'
            ],
            'ddos': [
                r'traffic_spike_pattern',
                r'connection_flood',
                r'bandwidth_exhaustion'
            ]
        }
    
    def analyze_behavior(self, data: Dict) -> Dict:
        """Analyze system behavior for threats"""
        results = {
            'anomaly_score': 0.0,
            'threat_indicators': [],
            'confidence': 0.0
        }
        
        # Analyze system calls
        if 'system_calls' in data:
            results['system_calls_score'] = self._analyze_system_calls(data['system_calls'])
        
        # Analyze network traffic
        if 'network_traffic' in data:
            results['network_score'] = self._analyze_network_traffic(data['network_traffic'])
        
        # Analyze file operations
        if 'file_operations' in data:
            results['file_ops_score'] = self._analyze_file_operations(data['file_operations'])
        
        # Calculate overall threat score
        results['threat_score'] = self._calculate_threat_score(results)
        
        return results
    
    def _analyze_system_calls(self, calls: List[str]) -> float:
        """Analyze system calls for suspicious patterns"""
        suspicious_patterns = [
            'create_remote_thread',
            'write_process_memory',
            'create_process',
            'reg_create_key'
        ]
        
        score = 0.0
        for call in calls:
            if any(pattern in call.lower() for pattern in suspicious_patterns):
                score += 0.1
        return min(score, 1.0)
    
    def _analyze_network_traffic(self, traffic: Dict) -> float:
        """Analyze network traffic for suspicious patterns"""
        score = 0.0
        
        # Check for unusual ports
        if traffic.get('unusual_ports', 0) > 5:
            score += 0.3
        
        # Check for high traffic volume
        if traffic.get('bytes_per_second', 0) > 1000000:  # 1 MB/s
            score += 0.3
        
        # Check for multiple failed connections
        if traffic.get('failed_connections', 0) > 10:
            score += 0.4
        
        return min(score, 1.0)
    
    def _analyze_file_operations(self, operations: List[Dict]) -> float:
        """Analyze file operations for suspicious activity"""
        suspicious_operations = {
            'encrypt': 0.4,
            'delete_multiple': 0.3,
            'modify_system': 0.4,
            'create_executable': 0.2
        }
        
        score = 0.0
        for op in operations:
            op_type = op.get('type', '').lower()
            if op_type in suspicious_operations:
                score += suspicious_operations[op_type]
        
        return min(score, 1.0)
    
    def _calculate_threat_score(self, results: Dict) -> float:
        """Calculate overall threat score"""
        weights = {
            'system_calls_score': 0.4,
            'network_score': 0.4,
            'file_ops_score': 0.2
        }
        
        score = 0.0
        for metric, weight in weights.items():
            if metric in results:
                score += results[metric] * weight
        
        return score

class MLAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self._init_models()
        self.advanced_detector = AdvancedThreatDetector()
        self.threat_memory = {}
        self.correlation_window = timedelta(hours=24)
    
    def _init_models(self):
        """Initialize ML models"""
        # Initialize text classifier
        self.text_classifier = TextClassifier()
        
        # Initialize anomaly detection models
        self.isolation_forest = IsolationForest(contamination=0.1)
        self.one_class_svm = OneClassSVM(kernel='rbf', nu=0.1)
        
        # Initialize clustering model
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
    
    def analyze_threat(self, data: Dict) -> Dict:
        """Comprehensive threat analysis"""
        results = {
            'timestamp': datetime.utcnow(),
            'basic_analysis': {},
            'advanced_analysis': {},
            'correlations': [],
            'risk_score': 0.0
        }
        
        # Basic threat detection
        if 'text' in data:
            try:
                results['basic_analysis']['classification'] = self.text_classifier.classify(data['text'])
            except Exception as e:
                print(f"Error in text classification: {e}")
                results['basic_analysis']['classification'] = {'label': 'unknown', 'confidence': 0.0}
        
        if 'features' in data:
            try:
                results['basic_analysis']['anomalies'] = self._detect_anomalies(data['features'])
                results['basic_analysis']['clusters'] = self._cluster_threats(data['features'])
            except Exception as e:
                print(f"Error in anomaly/cluster detection: {e}")
        
        # Advanced threat detection
        try:
            results['advanced_analysis'] = self.advanced_detector.analyze_behavior(data)
        except Exception as e:
            print(f"Error in advanced analysis: {e}")
        
        # Threat correlation
        try:
            results['correlations'] = self._correlate_threats(data)
        except Exception as e:
            print(f"Error in threat correlation: {e}")
        
        # Calculate final risk score
        results['risk_score'] = self._calculate_combined_risk_score(results)
        
        # Update threat memory
        self._update_threat_memory(data, results)
        
        return results
    
    def _detect_anomalies(self, features: np.ndarray) -> Dict:
        """Detect anomalies using multiple methods"""
        return {
            'isolation_forest': self.isolation_forest.fit_predict(features),
            'one_class_svm': self.one_class_svm.fit_predict(features)
        }
    
    def _cluster_threats(self, features: np.ndarray) -> np.ndarray:
        """Cluster similar threats"""
        return self.dbscan.fit_predict(features)
    
    def _correlate_threats(self, data: Dict) -> List[Dict]:
        """Correlate current threat with historical threats"""
        correlations = []
        current_time = datetime.utcnow()
        
        for threat_id, threat_data in self.threat_memory.items():
            if current_time - threat_data['timestamp'] <= self.correlation_window:
                correlation_score = self._calculate_correlation_score(data, threat_data)
                if correlation_score > 0.7:  # Correlation threshold
                    correlations.append({
                        'threat_id': threat_id,
                        'correlation_score': correlation_score,
                        'correlation_type': self._determine_correlation_type(data, threat_data)
                    })
        
        return correlations
    
    def _calculate_correlation_score(self, current: Dict, historical: Dict) -> float:
        """Calculate correlation score between two threats"""
        score = 0.0
        
        # Compare IP addresses
        if current.get('source_ip') == historical.get('source_ip'):
            score += 0.4
        
        # Compare threat types
        if current.get('type') == historical.get('type'):
            score += 0.3
        
        # Compare attack patterns
        if self._compare_patterns(current.get('pattern'), historical.get('pattern')):
            score += 0.3
        
        return score
    
    def _determine_correlation_type(self, current: Dict, historical: Dict) -> str:
        """Determine the type of correlation between threats"""
        if current.get('source_ip') == historical.get('source_ip'):
            return 'same_source'
        elif current.get('type') == historical.get('type'):
            return 'same_attack_type'
        elif self._compare_patterns(current.get('pattern'), historical.get('pattern')):
            return 'similar_pattern'
        return 'unknown'
    
    def _compare_patterns(self, pattern1: str, pattern2: str) -> bool:
        """Compare two attack patterns for similarity"""
        if not (pattern1 and pattern2):
            return False
        return pattern1.lower() == pattern2.lower()
    
    def _update_threat_memory(self, data: Dict, results: Dict):
        """Update threat memory with new threat data"""
        threat_id = f"threat_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self.threat_memory[threat_id] = {
            'timestamp': datetime.utcnow(),
            'data': data,
            'analysis_results': results
        }
        
        # Clean up old threats
        self._cleanup_threat_memory()
    
    def _cleanup_threat_memory(self):
        """Remove old threats from memory"""
        current_time = datetime.utcnow()
        self.threat_memory = {
            tid: data for tid, data in self.threat_memory.items()
            if current_time - data['timestamp'] <= self.correlation_window
        }
    
    def _calculate_combined_risk_score(self, results: Dict) -> float:
        """Calculate combined risk score from all analyses"""
        weights = {
            'basic_classification': 0.3,
            'anomaly_detection': 0.2,
            'advanced_analysis': 0.3,
            'correlation': 0.2
        }
        
        score = 0.0
        
        # Basic classification score
        if 'basic_analysis' in results and 'classification' in results['basic_analysis']:
            score += weights['basic_classification'] * results['basic_analysis']['classification'].get('confidence', 0)
        
        # Anomaly detection score
        if 'basic_analysis' in results and 'anomalies' in results['basic_analysis']:
            anomaly_scores = results['basic_analysis']['anomalies']
            score += weights['anomaly_detection'] * (
                1 if -1 in anomaly_scores.get('isolation_forest', []) else 0
            )
        
        # Advanced analysis score
        if 'advanced_analysis' in results:
            score += weights['advanced_analysis'] * results['advanced_analysis'].get('threat_score', 0)
        
        # Correlation score
        if results['correlations']:
            correlation_score = max(corr['correlation_score'] for corr in results['correlations'])
            score += weights['correlation'] * correlation_score
        
        return min(score * 10, 10)  # Scale to 0-10 