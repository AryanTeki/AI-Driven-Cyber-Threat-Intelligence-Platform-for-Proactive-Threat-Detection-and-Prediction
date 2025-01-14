from typing import Dict, List
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification

class ContinuousImprovement:
    def __init__(self, config: Dict):
        self.config = config
        self.feedback_data = []
        self.model_metrics = {}
        self._init_models()
    
    def _init_models(self):
        """Initialize models for continuous training"""
        self.tokenizer = AutoTokenizer.from_pretrained('security-bert-base-uncased')
        self.model = TFAutoModelForSequenceClassification.from_pretrained(
            'security-bert-base-uncased',
            num_labels=4  # malware, phishing, ddos, ransomware
        )
    
    def collect_feedback(self, feedback: Dict):
        """Collect user feedback for model improvement"""
        feedback['timestamp'] = datetime.utcnow()
        self.feedback_data.append(feedback)
        
        # If we have enough feedback, trigger model retraining
        if len(self.feedback_data) >= self.config.get('retraining_threshold', 100):
            self.retrain_models()
    
    def retrain_models(self):
        """Retrain models with new data"""
        if not self.feedback_data:
            return
        
        # Prepare training data
        df = pd.DataFrame(self.feedback_data)
        
        # Split data for training
        texts = df['text'].tolist()
        labels = df['label'].tolist()
        
        X_train, X_val, y_train, y_val = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )
        
        # Tokenize data
        train_encodings = self.tokenizer(
            X_train,
            truncation=True,
            padding=True,
            return_tensors='tf'
        )
        val_encodings = self.tokenizer(
            X_val,
            truncation=True,
            padding=True,
            return_tensors='tf'
        )
        
        # Convert labels to numpy arrays
        train_labels = np.array(y_train)
        val_labels = np.array(y_val)
        
        # Create TensorFlow datasets
        train_dataset = tf.data.Dataset.from_tensor_slices((
            dict(train_encodings),
            train_labels
        )).shuffle(1000).batch(16)
        
        val_dataset = tf.data.Dataset.from_tensor_slices((
            dict(val_encodings),
            val_labels
        )).batch(16)
        
        # Train the model
        history = self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=3
        )
        
        # Update metrics
        self._update_metrics(history, y_val, self.model.predict(val_dataset))
        
        # Save the model
        self._save_model()
        
        # Clear feedback data after training
        self.feedback_data = []
    
    def _update_metrics(self, history: tf.keras.callbacks.History,
                       y_true: np.ndarray, y_pred: np.ndarray):
        """Update model performance metrics"""
        self.model_metrics = {
            'timestamp': datetime.utcnow(),
            'training_loss': history.history['loss'][-1],
            'validation_loss': history.history['val_loss'][-1],
            'classification_report': classification_report(
                y_true,
                np.argmax(y_pred, axis=1),
                output_dict=True
            ),
            'confusion_matrix': confusion_matrix(
                y_true,
                np.argmax(y_pred, axis=1)
            ).tolist()
        }
    
    def _save_model(self):
        """Save the retrained model"""
        save_path = self.config.get('model_save_path', './models')
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        # Save model
        self.model.save_pretrained(f"{save_path}/model_{timestamp}")
        
        # Save tokenizer
        self.tokenizer.save_pretrained(f"{save_path}/tokenizer_{timestamp}")
        
        # Save metrics
        metrics_path = f"{save_path}/metrics_{timestamp}.json"
        with open(metrics_path, 'w') as f:
            json.dump(self.model_metrics, f)
    
    def get_model_performance(self) -> Dict:
        """Get current model performance metrics"""
        return self.model_metrics
    
    def analyze_feedback_trends(self) -> Dict:
        """Analyze trends in user feedback"""
        if not self.feedback_data:
            return {}
        
        df = pd.DataFrame(self.feedback_data)
        
        return {
            'total_feedback': len(df),
            'feedback_by_type': df['type'].value_counts().to_dict(),
            'average_confidence': df['confidence'].mean(),
            'feedback_trend': df.groupby(
                pd.Grouper(key='timestamp', freq='D')
            ).size().to_dict()
        }
    
    def generate_improvement_report(self) -> Dict:
        """Generate a report on model improvements and feedback analysis"""
        return {
            'timestamp': datetime.utcnow(),
            'model_metrics': self.get_model_performance(),
            'feedback_analysis': self.analyze_feedback_trends(),
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[Dict]:
        """Generate recommendations for model improvement"""
        recommendations = []
        
        # Analyze model performance
        if self.model_metrics:
            metrics = self.model_metrics['classification_report']
            
            # Check for classes with low performance
            for class_name, class_metrics in metrics.items():
                if isinstance(class_metrics, dict):
                    if class_metrics['f1-score'] < 0.8:
                        recommendations.append({
                            'type': 'model_performance',
                            'description': f'Improve model performance for {class_name} class',
                            'priority': 'High'
                        })
        
        # Analyze feedback trends
        feedback_trends = self.analyze_feedback_trends()
        if feedback_trends:
            if feedback_trends.get('average_confidence', 1.0) < 0.8:
                recommendations.append({
                    'type': 'confidence',
                    'description': 'Model confidence is low, consider collecting more training data',
                    'priority': 'Medium'
                })
        
        return recommendations 