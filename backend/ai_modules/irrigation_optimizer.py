"""
Smart Irrigation Optimization Module
AI-powered irrigation scheduling and water management
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import joblib
import os

class IrrigationOptimizer:
    """
    AI-powered irrigation optimization system for SREMS-TN
    
    Features:
    - Weather-based irrigation scheduling
    - Soil moisture prediction
    - Crop water requirement calculation
    - Energy-efficient scheduling
    - Water conservation optimization
    """
    
    def __init__(self, model_path: Optional[str] = None):
        self.soil_moisture_model = None
        self.water_demand_model = None
        self.scaler = None
        
        # Crop coefficients (Kc) for different growth stages
        self.crop_coefficients = {
            'cereales': {'initial': 0.4, 'development': 0.7, 'mid': 1.15, 'late': 0.4},
            'legumes': {'initial': 0.6, 'development': 1.0, 'mid': 1.15, 'late': 0.8},
            'fruits': {'initial': 0.45, 'development': 0.75, 'mid': 1.05, 'late': 0.65},
            'olives': {'initial': 0.5, 'development': 0.65, 'mid': 0.8, 'late': 0.6},
            'agrumes': {'initial': 0.7, 'development': 0.8, 'mid': 0.85, 'late': 0.75}
        }
        
        if model_path and os.path.exists(model_path):
            self.load_models(model_path)
        else:
            self._initialize_default_models()
    
    def _initialize_default_models(self):
        """Initialize with default models for demo purposes"""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        
        self.soil_moisture_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=8,
            random_state=42
        )
        
        self.water_demand_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.scaler = StandardScaler()
        
        # Train with synthetic data for demo
        self._train_with_synthetic_data()
    
    def _train_with_synthetic_data(self):
        """Train models with synthetic data for demonstration"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic environmental data
        data = {
            'temperature': np.random.normal(28, 8, n_samples),
            'humidity': np.random.normal(60, 20, n_samples),
            'wind_speed': np.random.exponential(2, n_samples),
            'solar_radiation': np.random.exponential(20, n_samples),
            'rainfall': np.random.exponential(5, n_samples),
            'days_since_irrigation': np.random.randint(0, 7, n_samples),
            'crop_stage': np.random.choice([0, 1, 2, 3], n_samples),  # growth stages
            'soil_type': np.random.choice([0, 1, 2, 3, 4], n_samples)  # soil types
        }
        
        df = pd.DataFrame(data)
        
        # Generate synthetic soil moisture (0-100%)
        soil_moisture = (
            50 +  # Base moisture
            df['rainfall'] * 2 -  # Rainfall increases moisture
            df['temperature'] * 0.5 -  # Heat decreases moisture
            df['days_since_irrigation'] * 5 +  # Time decreases moisture
            df['humidity'] * 0.2 +  # Humidity helps retain moisture
            np.random.normal(0, 5, n_samples)  # Noise
        )
        soil_moisture = np.clip(soil_moisture, 0, 100)
        
        # Generate synthetic water demand (L/m²/day)
        water_demand = (
            2 +  # Base demand
            df['temperature'] * 0.1 +  # Heat increases demand
            df['solar_radiation'] * 0.05 +  # Solar radiation increases demand
            df['crop_stage'] * 0.5 -  # Growth stage affects demand
            df['humidity'] * 0.02 -  # Humidity reduces demand
            df['rainfall'] * 0.1 +  # Recent rain reduces demand
            np.random.normal(0, 0.5, n_samples)  # Noise
        )
        water_demand = np.maximum(0, water_demand)
        
        # Prepare features
        features = df[['temperature', 'humidity', 'wind_speed', 'solar_radiation', 
                      'rainfall', 'days_since_irrigation', 'crop_stage', 'soil_type']]
        
        # Train models
        X_scaled = self.scaler.fit_transform(features)
        self.soil_moisture_model.fit(X_scaled, soil_moisture)
        self.water_demand_model.fit(X_scaled, water_demand)
    
    def predict_soil_moisture(self, environmental_data: Dict, farm_data: Dict) -> Dict:
        """
        Predict soil moisture based on environmental conditions
        
        Args:
            environmental_data: Weather and environmental parameters
            farm_data: Farm-specific data (crop type, soil type, etc.)
            
        Returns:
            Soil moisture prediction
        """
        try:
            # Prepare features
            features = self._prepare_environmental_features(environmental_data, farm_data)
            
            # Scale features
            features_scaled = self.scaler.transform([features])
            
            # Make prediction
            moisture_prediction = self.soil_moisture_model.predict(features_scaled)[0]
            moisture_prediction = max(0, min(100, moisture_prediction))
            
            # Determine moisture status
            status = self._get_moisture_status(moisture_prediction)
            
            return {
                'predicted_soil_moisture_percent': moisture_prediction,
                'moisture_status': status,
                'timestamp': datetime.now().isoformat(),
                'confidence_score': self._calculate_moisture_confidence(features)
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'predicted_soil_moisture_percent': 50,
                'moisture_status': 'unknown'
            }
    
    def calculate_water_demand(self, environmental_data: Dict, farm_data: Dict) -> Dict:
        """
        Calculate crop water demand (evapotranspiration)
        
        Args:
            environmental_data: Weather data
            farm_data: Farm and crop data
            
        Returns:
            Water demand calculation
        """
        try:
            # Calculate reference evapotranspiration (ET0) - simplified Penman equation
            et0 = self._calculate_reference_et(environmental_data)
            
            # Get crop coefficient
            crop_type = farm_data.get('farm_type', 'cereales')
            growth_stage = farm_data.get('growth_stage', 'mid')
            kc = self.crop_coefficients.get(crop_type, {}).get(growth_stage, 1.0)
            
            # Calculate crop evapotranspiration (ETc)
            etc = et0 * kc
            
            # Adjust for soil type and irrigation efficiency
            soil_factor = self._get_soil_factor(farm_data.get('soil_type', 'limoneux'))
            irrigation_efficiency = farm_data.get('irrigation_efficiency', 0.85)
            
            # Calculate total water requirement
            water_requirement = (etc * soil_factor) / irrigation_efficiency
            
            return {
                'reference_et_mm_day': et0,
                'crop_coefficient': kc,
                'crop_et_mm_day': etc,
                'water_requirement_mm_day': water_requirement,
                'water_requirement_l_m2_day': water_requirement,  # 1mm = 1L/m²
                'soil_factor': soil_factor,
                'irrigation_efficiency': irrigation_efficiency,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'water_requirement_l_m2_day': 3.0  # Default value
            }
    
    def optimize_irrigation_schedule(self, environmental_data: Dict, farm_data: Dict, 
                                   solar_forecast: List[Dict]) -> Dict:
        """
        Generate optimized irrigation schedule
        
        Args:
            environmental_data: Current weather conditions
            farm_data: Farm configuration and crop data
            solar_forecast: Solar power forecast for scheduling
            
        Returns:
            Optimized irrigation schedule
        """
        # Get current soil moisture and water demand
        moisture_prediction = self.predict_soil_moisture(environmental_data, farm_data)
        water_demand = self.calculate_water_demand(environmental_data, farm_data)
        
        # Analyze solar power availability
        solar_analysis = self._analyze_solar_availability(solar_forecast)
        
        # Generate irrigation recommendations
        recommendations = self._generate_irrigation_recommendations(
            moisture_prediction, water_demand, solar_analysis, farm_data
        )
        
        # Create detailed schedule
        schedule = self._create_irrigation_schedule(recommendations, solar_analysis)
        
        return {
            'current_soil_moisture': moisture_prediction,
            'water_demand_analysis': water_demand,
            'solar_availability': solar_analysis,
            'irrigation_recommendations': recommendations,
            'detailed_schedule': schedule,
            'optimization_score': self._calculate_optimization_score(schedule),
            'timestamp': datetime.now().isoformat()
        }
    
    def _prepare_environmental_features(self, environmental_data: Dict, farm_data: Dict) -> List[float]:
        """Prepare feature vector from environmental and farm data"""
        # Map soil types to numeric values
        soil_type_map = {'argileux': 0, 'sableux': 1, 'limoneux': 2, 'calcaire': 3, 'mixte': 4}
        
        # Map growth stages
        growth_stage_map = {'initial': 0, 'development': 1, 'mid': 2, 'late': 3}
        
        features = [
            environmental_data.get('temperature', 28),
            environmental_data.get('humidity', 60),
            environmental_data.get('wind_speed', 2),
            environmental_data.get('solar_radiation', 20),
            environmental_data.get('rainfall_24h', 0),
            farm_data.get('days_since_irrigation', 2),
            growth_stage_map.get(farm_data.get('growth_stage', 'mid'), 2),
            soil_type_map.get(farm_data.get('soil_type', 'limoneux'), 2)
        ]
        
        return features
    
    def _calculate_reference_et(self, environmental_data: Dict) -> float:
        """Calculate reference evapotranspiration using simplified Penman equation"""
        temp = environmental_data.get('temperature', 28)
        humidity = environmental_data.get('humidity', 60)
        wind_speed = environmental_data.get('wind_speed', 2)
        solar_radiation = environmental_data.get('solar_radiation', 20)
        
        # Simplified ET0 calculation (mm/day)
        et0 = (
            0.0023 * (temp + 17.8) * np.sqrt(abs(temp - humidity)) * 
            (solar_radiation * 0.408) + 
            0.0001 * wind_speed * (temp - humidity)
        )
        
        return max(0, et0)
    
    def _get_soil_factor(self, soil_type: str) -> float:
        """Get soil-specific adjustment factor"""
        soil_factors = {
            'argileux': 1.2,    # Clay holds more water
            'sableux': 0.8,     # Sand drains quickly
            'limoneux': 1.0,    # Loam is ideal
            'calcaire': 0.9,    # Limestone drains moderately
            'mixte': 1.0        # Mixed soil
        }
        return soil_factors.get(soil_type, 1.0)
    
    def _get_moisture_status(self, moisture_percent: float) -> str:
        """Determine moisture status from percentage"""
        if moisture_percent >= 70:
            return 'optimal'
        elif moisture_percent >= 50:
            return 'adequate'
        elif moisture_percent >= 30:
            return 'low'
        else:
            return 'critical'
    
    def _calculate_moisture_confidence(self, features: List[float]) -> float:
        """Calculate confidence score for moisture prediction"""
        # Simplified confidence based on data quality
        base_confidence = 0.8
        
        # Adjust based on recent rainfall data availability
        if features[4] > 0:  # rainfall data available
            confidence_adj = 0.1
        else:
            confidence_adj = -0.05
        
        return min(1.0, max(0.0, base_confidence + confidence_adj))
    
    def _analyze_solar_availability(self, solar_forecast: List[Dict]) -> Dict:
        """Analyze solar power availability for irrigation scheduling"""
        if not solar_forecast:
            return {'peak_hours': [], 'total_available_kwh': 0, 'optimal_windows': []}
        
        # Find peak solar hours (simplified)
        peak_hours = []
        total_kwh = 0
        
        for i, forecast in enumerate(solar_forecast[:24]):  # Next 24 hours
            power = forecast.get('predicted_power_kw', 0)
            total_kwh += power
            
            if power > 4:  # High solar output threshold
                peak_hours.append({
                    'hour': i,
                    'power_kw': power,
                    'timestamp': (datetime.now() + timedelta(hours=i)).isoformat()
                })
        
        # Identify optimal irrigation windows (consecutive high-power hours)
        optimal_windows = self._find_optimal_windows(peak_hours)
        
        return {
            'peak_hours': peak_hours,
            'total_available_kwh': total_kwh,
            'optimal_windows': optimal_windows,
            'solar_efficiency_score': min(100, (total_kwh / 100) * 100)
        }
    
    def _find_optimal_windows(self, peak_hours: List[Dict]) -> List[Dict]:
        """Find consecutive hours with high solar output"""
        if not peak_hours:
            return []
        
        windows = []
        current_window = [peak_hours[0]]
        
        for i in range(1, len(peak_hours)):
            if peak_hours[i]['hour'] == peak_hours[i-1]['hour'] + 1:
                current_window.append(peak_hours[i])
            else:
                if len(current_window) >= 2:  # At least 2 consecutive hours
                    windows.append({
                        'start_hour': current_window[0]['hour'],
                        'end_hour': current_window[-1]['hour'],
                        'duration_hours': len(current_window),
                        'average_power': np.mean([h['power_kw'] for h in current_window])
                    })
                current_window = [peak_hours[i]]
        
        # Don't forget the last window
        if len(current_window) >= 2:
            windows.append({
                'start_hour': current_window[0]['hour'],
                'end_hour': current_window[-1]['hour'],
                'duration_hours': len(current_window),
                'average_power': np.mean([h['power_kw'] for h in current_window])
            })
        
        return windows
    
    def _generate_irrigation_recommendations(self, moisture_prediction: Dict, 
                                           water_demand: Dict, solar_analysis: Dict, 
                                           farm_data: Dict) -> List[Dict]:
        """Generate irrigation recommendations based on analysis"""
        recommendations = []
        
        moisture_status = moisture_prediction.get('moisture_status', 'unknown')
        water_requirement = water_demand.get('water_requirement_l_m2_day', 3.0)
        
        # Immediate irrigation needs
        if moisture_status == 'critical':
            recommendations.append({
                'priority': 'critical',
                'action': 'immediate_irrigation',
                'message': 'Critical soil moisture - irrigate immediately',
                'water_amount_l_m2': water_requirement * 1.5,
                'timing': 'immediate'
            })
        elif moisture_status == 'low':
            recommendations.append({
                'priority': 'high',
                'action': 'schedule_irrigation',
                'message': 'Low soil moisture - schedule irrigation within 6 hours',
                'water_amount_l_m2': water_requirement,
                'timing': 'within_6_hours'
            })
        
        # Solar-optimized scheduling
        optimal_windows = solar_analysis.get('optimal_windows', [])
        if optimal_windows and moisture_status in ['adequate', 'low']:
            best_window = max(optimal_windows, key=lambda x: x['average_power'])
            recommendations.append({
                'priority': 'medium',
                'action': 'solar_optimized_irrigation',
                'message': f'Optimal solar window: {best_window["start_hour"]}:00-{best_window["end_hour"]}:00',
                'water_amount_l_m2': water_requirement,
                'timing': f'hours_{best_window["start_hour"]}_to_{best_window["end_hour"]}'
            })
        
        # Preventive irrigation
        if moisture_status == 'optimal':
            recommendations.append({
                'priority': 'low',
                'action': 'monitor',
                'message': 'Soil moisture optimal - continue monitoring',
                'water_amount_l_m2': 0,
                'timing': 'none'
            })
        
        return recommendations
    
    def _create_irrigation_schedule(self, recommendations: List[Dict], 
                                  solar_analysis: Dict) -> List[Dict]:
        """Create detailed irrigation schedule"""
        schedule = []
        
        for rec in recommendations:
            if rec['action'] in ['immediate_irrigation', 'schedule_irrigation', 'solar_optimized_irrigation']:
                # Calculate irrigation duration based on pump capacity
                pump_capacity = 50  # L/min (example)
                area = 1000  # m² (example farm area)
                water_needed = rec['water_amount_l_m2'] * area
                duration_minutes = water_needed / pump_capacity
                
                # Determine start time
                if rec['timing'] == 'immediate':
                    start_time = datetime.now()
                elif 'hours_' in rec['timing']:
                    # Extract hour from timing string
                    hour = int(rec['timing'].split('_')[1])
                    start_time = datetime.now().replace(hour=hour, minute=0, second=0, microsecond=0)
                    if start_time < datetime.now():
                        start_time += timedelta(days=1)
                else:
                    start_time = datetime.now() + timedelta(hours=2)  # Default 2 hours
                
                schedule.append({
                    'start_time': start_time.isoformat(),
                    'end_time': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
                    'duration_minutes': duration_minutes,
                    'water_amount_liters': water_needed,
                    'priority': rec['priority'],
                    'reason': rec['message'],
                    'energy_source': 'solar' if 'solar' in rec['action'] else 'grid'
                })
        
        return sorted(schedule, key=lambda x: x['start_time'])
    
    def _calculate_optimization_score(self, schedule: List[Dict]) -> float:
        """Calculate optimization score for the irrigation schedule"""
        if not schedule:
            return 0.0
        
        score = 70  # Base score
        
        # Bonus for solar-powered irrigation
        solar_sessions = sum(1 for s in schedule if s['energy_source'] == 'solar')
        score += solar_sessions * 10
        
        # Bonus for efficient timing
        for session in schedule:
            start_hour = datetime.fromisoformat(session['start_time']).hour
            if 10 <= start_hour <= 16:  # Optimal daylight hours
                score += 5
        
        return min(100.0, score)
    
    def save_models(self, path: str):
        """Save trained models to disk"""
        model_data = {
            'soil_moisture_model': self.soil_moisture_model,
            'water_demand_model': self.water_demand_model,
            'scaler': self.scaler,
            'crop_coefficients': self.crop_coefficients
        }
        joblib.dump(model_data, path)
    
    def load_models(self, path: str):
        """Load trained models from disk"""
        model_data = joblib.load(path)
        self.soil_moisture_model = model_data['soil_moisture_model']
        self.water_demand_model = model_data['water_demand_model']
        self.scaler = model_data['scaler']
        self.crop_coefficients = model_data.get('crop_coefficients', self.crop_coefficients)


# Example usage and testing
if __name__ == "__main__":
    # Initialize optimizer
    optimizer = IrrigationOptimizer()
    
    # Test data
    environmental_data = {
        'temperature': 32,
        'humidity': 45,
        'wind_speed': 3,
        'solar_radiation': 25,
        'rainfall_24h': 0
    }
    
    farm_data = {
        'farm_type': 'cereales',
        'soil_type': 'limoneux',
        'growth_stage': 'mid',
        'days_since_irrigation': 3,
        'irrigation_efficiency': 0.85
    }
    
    solar_forecast = [
        {'predicted_power_kw': 2 + i * 0.5} for i in range(24)
    ]
    
    # Test optimization
    result = optimizer.optimize_irrigation_schedule(environmental_data, farm_data, solar_forecast)
    print("Irrigation Optimization Result:", result)