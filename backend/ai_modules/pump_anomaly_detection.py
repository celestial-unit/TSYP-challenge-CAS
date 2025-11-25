"""
Pump Anomaly Detection Module
Based on audio analysis and operational parameters
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import joblib
import os

class PumpAnomalyDetector:
    """
    AI-powered pump anomaly detection system for SREMS-TN
    
    Features:
    - Audio-based anomaly detection
    - Operational parameter monitoring
    - Predictive maintenance alerts
    - Performance degradation tracking
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.audio_model = None
        self.operational_model = None
        self.scaler = None
        self.threshold_normal = 0.7
        self.threshold_warning = 0.5
        self.threshold_critical = 0.3
        
        if model_path and os.path.exists(model_path):
            self.load_models(model_path)
        else:
            self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize with default models for demo purposes"""
        from sklearn.ensemble import IsolationForest
        from sklearn.preprocessing import StandardScaler
        
        # Audio-based anomaly detection (simplified)
        self.audio_model = IsolationForest(
            contamination=0.1,
            random_state=42
        )
        
        # Operational parameter anomaly detection
        self.operational_model = IsolationForest(
            contamination=0.15,
            random_state=42
        )
        
        self.scaler = StandardScaler()
        
        # Train with synthetic data for demo
        self._train_with_synthetic_data()
    
    def _train_with_synthetic_data(self):
        """Train models with synthetic data for demonstration"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic operational data
        normal_data = {
            'flow_rate': np.random.normal(50, 5, int(n_samples * 0.9)),
            'pressure': np.random.normal(3.5, 0.3, int(n_samples * 0.9)),
            'power_consumption': np.random.normal(5.2, 0.4, int(n_samples * 0.9)),
            'vibration_level': np.random.normal(0.1, 0.02, int(n_samples * 0.9)),
            'temperature': np.random.normal(45, 5, int(n_samples * 0.9))
        }
        
        # Add some anomalous data
        anomaly_data = {
            'flow_rate': np.random.normal(30, 10, int(n_samples * 0.1)),
            'pressure': np.random.normal(2.0, 0.8, int(n_samples * 0.1)),
            'power_consumption': np.random.normal(7.5, 1.0, int(n_samples * 0.1)),
            'vibration_level': np.random.normal(0.3, 0.1, int(n_samples * 0.1)),
            'temperature': np.random.normal(65, 10, int(n_samples * 0.1))
        }
        
        # Combine data
        all_data = {}
        for key in normal_data.keys():
            all_data[key] = np.concatenate([normal_data[key], anomaly_data[key]])
        
        df = pd.DataFrame(all_data)
        
        # Train operational model
        X_scaled = self.scaler.fit_transform(df)
        self.operational_model.fit(X_scaled)
        
        # Train audio model with synthetic audio features
        audio_features = np.random.normal(0, 1, (n_samples, 18))  # 18 features like in notebook
        self.audio_model.fit(audio_features)
    
    def analyze_pump_audio(self, audio_features: List[float]) -> Dict:
        """
        Analyze pump audio for anomalies
        
        Args:
            audio_features: Extracted audio features (MFCCs, spectral features, etc.)
            
        Returns:
            Audio analysis results
        """
        try:
            # Reshape for single prediction
            features = np.array(audio_features).reshape(1, -1)
            
            # Get anomaly score
            anomaly_score = float(self.audio_model.decision_function(features)[0])
            is_anomaly = bool(self.audio_model.predict(features)[0] == -1)
            
            # Normalize score to 0-1 range (higher = more normal)
            normalized_score = float(self._normalize_anomaly_score(anomaly_score))
            
            # Determine status
            status = self._get_status_from_score(normalized_score)
            
            return {
                'audio_health_score': normalized_score,
                'is_anomaly_detected': is_anomaly,
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'audio'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'audio_health_score': 0.5,
                'is_anomaly_detected': True,
                'status': 'unknown'
            }
    
    def analyze_operational_parameters(self, operational_data: Dict) -> Dict:
        """
        Analyze operational parameters for anomalies
        
        Args:
            operational_data: Dictionary containing operational parameters
            
        Returns:
            Operational analysis results
        """
        try:
            # Prepare features
            features = [
                operational_data.get('flow_rate', 50),
                operational_data.get('pressure', 3.5),
                operational_data.get('power_consumption', 5.2),
                operational_data.get('vibration_level', 0.1),
                operational_data.get('temperature', 45)
            ]
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Get anomaly score
            anomaly_score = float(self.operational_model.decision_function(features_scaled)[0])
            is_anomaly = bool(self.operational_model.predict(features_scaled)[0] == -1)
            
            # Normalize score
            normalized_score = self._normalize_anomaly_score(anomaly_score)
            
            # Determine status
            status = self._get_status_from_score(normalized_score)
            
            # Analyze individual parameters
            parameter_analysis = self._analyze_individual_parameters(operational_data)
            
            return {
                'operational_health_score': normalized_score,
                'is_anomaly_detected': is_anomaly,
                'status': status,
                'parameter_analysis': parameter_analysis,
                'timestamp': datetime.now().isoformat(),
                'analysis_type': 'operational'
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'operational_health_score': 0.5,
                'is_anomaly_detected': True,
                'status': 'unknown'
            }
    
    def comprehensive_health_check(self, audio_features: List[float], operational_data: Dict) -> Dict:
        """
        Perform comprehensive pump health analysis
        
        Args:
            audio_features: Audio feature vector
            operational_data: Operational parameters
            
        Returns:
            Comprehensive health assessment
        """
        # Get individual analyses
        audio_analysis = self.analyze_pump_audio(audio_features)
        operational_analysis = self.analyze_operational_parameters(operational_data)
        
        # Calculate overall health score (weighted average)
        audio_weight = 0.4
        operational_weight = 0.6
        
        overall_score = (
            audio_analysis['audio_health_score'] * audio_weight +
            operational_analysis['operational_health_score'] * operational_weight
        )
        
        # Determine overall status
        overall_status = self._get_status_from_score(overall_score)
        
        # Generate maintenance recommendations
        recommendations = self._generate_maintenance_recommendations(
            audio_analysis, operational_analysis, overall_score
        )
        
        return {
            'overall_health_score': overall_score,
            'overall_status': overall_status,
            'audio_analysis': audio_analysis,
            'operational_analysis': operational_analysis,
            'maintenance_recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _normalize_anomaly_score(self, score: float) -> float:
        """Normalize anomaly score to 0-1 range"""
        # Isolation Forest scores are typically between -0.5 and 0.5
        # Convert to 0-1 where 1 is normal, 0 is anomalous
        normalized = (score + 0.5) / 1.0
        return max(0.0, min(1.0, normalized))
    
    def _get_status_from_score(self, score: float) -> str:
        """Determine status from health score"""
        if score >= self.threshold_normal:
            return 'normal'
        elif score >= self.threshold_warning:
            return 'warning'
        elif score >= self.threshold_critical:
            return 'critical'
        else:
            return 'failure'
    
    def _analyze_individual_parameters(self, operational_data: Dict) -> Dict:
        """Analyze individual operational parameters"""
        analysis = {}
        
        # Flow rate analysis
        flow_rate = operational_data.get('flow_rate', 50)
        if flow_rate < 30:
            analysis['flow_rate'] = {'status': 'low', 'message': 'Flow rate below normal range'}
        elif flow_rate > 70:
            analysis['flow_rate'] = {'status': 'high', 'message': 'Flow rate above normal range'}
        else:
            analysis['flow_rate'] = {'status': 'normal', 'message': 'Flow rate within normal range'}
        
        # Pressure analysis
        pressure = operational_data.get('pressure', 3.5)
        if pressure < 2.5:
            analysis['pressure'] = {'status': 'low', 'message': 'Pressure below normal range'}
        elif pressure > 4.5:
            analysis['pressure'] = {'status': 'high', 'message': 'Pressure above normal range'}
        else:
            analysis['pressure'] = {'status': 'normal', 'message': 'Pressure within normal range'}
        
        # Power consumption analysis
        power = operational_data.get('power_consumption', 5.2)
        if power > 7.0:
            analysis['power_consumption'] = {'status': 'high', 'message': 'High power consumption detected'}
        elif power < 3.0:
            analysis['power_consumption'] = {'status': 'low', 'message': 'Unusually low power consumption'}
        else:
            analysis['power_consumption'] = {'status': 'normal', 'message': 'Power consumption normal'}
        
        # Temperature analysis
        temperature = operational_data.get('temperature', 45)
        if temperature > 60:
            analysis['temperature'] = {'status': 'high', 'message': 'High temperature - check cooling'}
        elif temperature < 30:
            analysis['temperature'] = {'status': 'low', 'message': 'Unusually low temperature'}
        else:
            analysis['temperature'] = {'status': 'normal', 'message': 'Temperature within normal range'}
        
        # Vibration analysis
        vibration = operational_data.get('vibration_level', 0.1)
        if vibration > 0.2:
            analysis['vibration_level'] = {'status': 'high', 'message': 'High vibration - check alignment'}
        else:
            analysis['vibration_level'] = {'status': 'normal', 'message': 'Vibration levels normal'}
        
        return analysis
    
    def _generate_maintenance_recommendations(self, audio_analysis: Dict, 
                                           operational_analysis: Dict, 
                                           overall_score: float) -> List[Dict]:
        """Generate maintenance recommendations based on analysis"""
        recommendations = []
        
        # Overall health recommendations
        if overall_score < self.threshold_critical:
            recommendations.append({
                'priority': 'critical',
                'action': 'immediate_inspection',
                'message': 'Pump requires immediate inspection - multiple anomalies detected',
                'estimated_downtime': '2-4 hours'
            })
        elif overall_score < self.threshold_warning:
            recommendations.append({
                'priority': 'high',
                'action': 'scheduled_maintenance',
                'message': 'Schedule maintenance within 24 hours',
                'estimated_downtime': '1-2 hours'
            })
        
        # Audio-based recommendations
        if audio_analysis.get('is_anomaly_detected'):
            recommendations.append({
                'priority': 'medium',
                'action': 'audio_inspection',
                'message': 'Unusual pump sounds detected - check for mechanical issues',
                'estimated_downtime': '30 minutes'
            })
        
        # Parameter-specific recommendations
        param_analysis = operational_analysis.get('parameter_analysis', {})
        
        if param_analysis.get('temperature', {}).get('status') == 'high':
            recommendations.append({
                'priority': 'high',
                'action': 'cooling_check',
                'message': 'Check cooling system and ventilation',
                'estimated_downtime': '1 hour'
            })
        
        if param_analysis.get('vibration_level', {}).get('status') == 'high':
            recommendations.append({
                'priority': 'medium',
                'action': 'alignment_check',
                'message': 'Check pump alignment and mounting',
                'estimated_downtime': '1-2 hours'
            })
        
        if param_analysis.get('flow_rate', {}).get('status') == 'low':
            recommendations.append({
                'priority': 'medium',
                'action': 'filter_check',
                'message': 'Check and clean intake filters',
                'estimated_downtime': '30 minutes'
            })
        
        # If no issues, recommend preventive maintenance
        if not recommendations:
            recommendations.append({
                'priority': 'low',
                'action': 'preventive_maintenance',
                'message': 'Pump operating normally - next scheduled maintenance in 30 days',
                'estimated_downtime': '0 minutes'
            })
        
        return recommendations
    
    def save_models(self, path: str):
        """Save trained models to disk"""
        model_data = {
            'audio_model': self.audio_model,
            'operational_model': self.operational_model,
            'scaler': self.scaler,
            'thresholds': {
                'normal': self.threshold_normal,
                'warning': self.threshold_warning,
                'critical': self.threshold_critical
            }
        }
        joblib.dump(model_data, path)
    
    def load_models(self, path: str):
        """Load trained models from disk"""
        model_data = joblib.load(path)
        self.audio_model = model_data['audio_model']
        self.operational_model = model_data['operational_model']
        self.scaler = model_data['scaler']
        
        thresholds = model_data.get('thresholds', {})
        self.threshold_normal = thresholds.get('normal', 0.7)
        self.threshold_warning = thresholds.get('warning', 0.5)
        self.threshold_critical = thresholds.get('critical', 0.3)


# Example usage and testing
if __name__ == "__main__":
    # Initialize detector
    detector = PumpAnomalyDetector()
    
    # Test operational analysis
    operational_data = {
        'flow_rate': 45,
        'pressure': 3.2,
        'power_consumption': 5.5,
        'vibration_level': 0.15,
        'temperature': 48
    }
    
    operational_result = detector.analyze_operational_parameters(operational_data)
    print("Operational Analysis:", operational_result)
    
    # Test audio analysis (synthetic features)
    audio_features = np.random.normal(0, 1, 18).tolist()
    audio_result = detector.analyze_pump_audio(audio_features)
    print("Audio Analysis:", audio_result)
    
    # Test comprehensive analysis
    comprehensive_result = detector.comprehensive_health_check(audio_features, operational_data)
    print("Comprehensive Analysis:", comprehensive_result)