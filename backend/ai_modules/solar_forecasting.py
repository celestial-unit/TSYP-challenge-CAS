"""
Solar Power Forecasting Module
Based on weather data and historical generation patterns
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import joblib
import os

class SolarPowerForecaster:
    """
    AI-powered solar power forecasting system for SREMS-TN
    
    Features:
    - Weather-based power prediction
    - Historical pattern analysis
    - Seasonal adjustments
    - Real-time optimization
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.scaler = None
        self.feature_columns = [
            'ambient_temperature', 'module_temperature', 'irradiation',
            'hour', 'day_of_year', 'is_weekend'
        ]
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self._initialize_default_model()
    
    def _initialize_default_model(self):
        """Initialize with a simple regression model for demo purposes"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
        # Generate synthetic training data for demo
        self._train_with_synthetic_data()
    
    def _train_with_synthetic_data(self):
        """Train model with synthetic data for demonstration"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic weather data
        data = {
            'ambient_temperature': np.random.normal(25, 10, n_samples),
            'module_temperature': np.random.normal(35, 15, n_samples),
            'irradiation': np.random.exponential(500, n_samples),
            'hour': np.random.randint(0, 24, n_samples),
            'day_of_year': np.random.randint(1, 366, n_samples),
            'is_weekend': np.random.choice([0, 1], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Generate synthetic power output based on realistic relationships
        power_output = (
            df['irradiation'] * 0.01 +  # Base irradiation effect
            np.maximum(0, df['ambient_temperature'] - 10) * 0.5 +  # Temperature effect
            np.sin(df['hour'] * np.pi / 12) * 100 +  # Daily cycle
            np.sin(df['day_of_year'] * 2 * np.pi / 365) * 50 +  # Seasonal cycle
            np.random.normal(0, 20, n_samples)  # Noise
        )
        power_output = np.maximum(0, power_output)  # No negative power
        
        # Train the model
        X = df[self.feature_columns]
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, power_output)
    
    def predict_power_output(self, weather_data: Dict) -> Dict:
        """
        Predict solar power output based on weather conditions
        
        Args:
            weather_data: Dictionary containing weather parameters
            
        Returns:
            Dictionary with prediction results
        """
        try:
            # Prepare input features
            features = self._prepare_features(weather_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Make prediction
            prediction = self.model.predict(features_scaled)[0]
            
            # Calculate confidence interval (simplified)
            confidence = self._calculate_confidence(features)
            
            return {
                'predicted_power_kw': max(0, prediction),
                'confidence_score': confidence,
                'timestamp': datetime.now().isoformat(),
                'weather_conditions': weather_data
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'predicted_power_kw': 0,
                'confidence_score': 0
            }
    
    def predict_daily_generation(self, date: datetime, weather_forecast: List[Dict]) -> Dict:
        """
        Predict total daily power generation
        
        Args:
            date: Target date for prediction
            weather_forecast: Hourly weather forecast data
            
        Returns:
            Daily generation prediction
        """
        hourly_predictions = []
        total_generation = 0
        
        for hour_data in weather_forecast:
            prediction = self.predict_power_output(hour_data)
            hourly_predictions.append(prediction)
            total_generation += prediction.get('predicted_power_kw', 0)
        
        return {
            'date': date.isoformat(),
            'total_daily_kwh': total_generation,
            'hourly_predictions': hourly_predictions,
            'peak_hour': max(hourly_predictions, key=lambda x: x.get('predicted_power_kw', 0)),
            'average_confidence': np.mean([p.get('confidence_score', 0) for p in hourly_predictions])
        }
    
    def _prepare_features(self, weather_data: Dict) -> List[float]:
        """Prepare feature vector from weather data"""
        now = datetime.now()
        
        features = [
            weather_data.get('ambient_temperature', 25),
            weather_data.get('module_temperature', 35),
            weather_data.get('irradiation', 500),
            now.hour,
            now.timetuple().tm_yday,
            1 if now.weekday() >= 5 else 0  # Weekend flag
        ]
        
        return features
    
    def _calculate_confidence(self, features: List[float]) -> float:
        """Calculate prediction confidence score"""
        # Simplified confidence calculation
        # In practice, this would use model uncertainty estimation
        base_confidence = 0.8
        
        # Adjust based on irradiation (higher irradiation = higher confidence)
        irradiation = features[2]
        if irradiation > 800:
            confidence_adj = 0.1
        elif irradiation > 400:
            confidence_adj = 0.05
        else:
            confidence_adj = -0.1
        
        return min(1.0, max(0.0, base_confidence + confidence_adj))
    
    def get_optimization_recommendations(self, current_weather: Dict, forecast: List[Dict]) -> Dict:
        """
        Generate optimization recommendations based on predictions
        
        Args:
            current_weather: Current weather conditions
            forecast: Weather forecast for next 24 hours
            
        Returns:
            Optimization recommendations
        """
        current_prediction = self.predict_power_output(current_weather)
        daily_forecast = self.predict_daily_generation(datetime.now(), forecast)
        
        recommendations = []
        
        # Current power optimization
        current_power = current_prediction['predicted_power_kw']
        if current_power > 5:
            recommendations.append({
                'type': 'immediate',
                'action': 'optimal_pumping',
                'message': f'High solar output ({current_power:.1f} kW) - Optimal time for irrigation',
                'priority': 'high'
            })
        elif current_power < 2:
            recommendations.append({
                'type': 'immediate',
                'action': 'conserve_energy',
                'message': 'Low solar output - Consider postponing non-essential operations',
                'priority': 'medium'
            })
        
        # Daily planning
        peak_hour = daily_forecast['peak_hour']
        if peak_hour:
            peak_time = datetime.fromisoformat(peak_hour['timestamp']).hour
            recommendations.append({
                'type': 'planning',
                'action': 'schedule_irrigation',
                'message': f'Schedule main irrigation around {peak_time}:00 for maximum efficiency',
                'priority': 'high'
            })
        
        return {
            'current_conditions': current_prediction,
            'daily_forecast': daily_forecast,
            'recommendations': recommendations,
            'energy_efficiency_score': self._calculate_efficiency_score(daily_forecast)
        }
    
    def _calculate_efficiency_score(self, daily_forecast: Dict) -> float:
        """Calculate energy efficiency score for the day"""
        total_kwh = daily_forecast['total_daily_kwh']
        avg_confidence = daily_forecast['average_confidence']
        
        # Normalize to 0-100 scale
        efficiency_score = min(100, (total_kwh / 50) * 100 * avg_confidence)
        return round(efficiency_score, 1)
    
    def save_model(self, path: str):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns
        }
        joblib.dump(model_data, path)
    
    def load_model(self, path: str):
        """Load trained model from disk"""
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']


# Example usage and testing
if __name__ == "__main__":
    # Initialize forecaster
    forecaster = SolarPowerForecaster()
    
    # Test current prediction
    current_weather = {
        'ambient_temperature': 28,
        'module_temperature': 40,
        'irradiation': 750
    }
    
    prediction = forecaster.predict_power_output(current_weather)
    print("Current Power Prediction:", prediction)
    
    # Test optimization recommendations
    forecast_data = [
        {'ambient_temperature': 25 + i, 'module_temperature': 35 + i, 'irradiation': 600 + i*50}
        for i in range(24)
    ]
    
    recommendations = forecaster.get_optimization_recommendations(current_weather, forecast_data)
    print("Optimization Recommendations:", recommendations)