"""
AI Endpoints for SREMS-TN
Provides AI-powered features for farmers
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
import sys
import os

# Add ai_modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ai_modules.solar_forecasting import SolarPowerForecaster
from ai_modules.pump_anomaly_detection import PumpAnomalyDetector
from ai_modules.irrigation_optimizer import IrrigationOptimizer

router = APIRouter(prefix="/ai", tags=["AI Services"])

# Initialize AI modules
solar_forecaster = SolarPowerForecaster()
pump_detector = PumpAnomalyDetector()
irrigation_optimizer = IrrigationOptimizer()


# Request/Response Models
class WeatherData(BaseModel):
    ambient_temperature: float = Field(..., description="Ambient temperature in Celsius")
    module_temperature: Optional[float] = Field(None, description="Solar module temperature")
    irradiation: float = Field(..., description="Solar irradiation in W/m²")
    humidity: Optional[float] = Field(None, description="Relative humidity %")
    wind_speed: Optional[float] = Field(None, description="Wind speed in m/s")
    rainfall_24h: Optional[float] = Field(0, description="Rainfall in last 24h (mm)")


class PumpOperationalData(BaseModel):
    flow_rate: float = Field(..., description="Pump flow rate in L/min")
    pressure: float = Field(..., description="System pressure in bar")
    power_consumption: float = Field(..., description="Power consumption in kW")
    vibration_level: float = Field(..., description="Vibration level")
    temperature: float = Field(..., description="Pump temperature in Celsius")


class FarmData(BaseModel):
    farm_type: str = Field(..., description="Type of crops")
    soil_type: str = Field(..., description="Soil type")
    growth_stage: Optional[str] = Field("mid", description="Crop growth stage")
    days_since_irrigation: Optional[int] = Field(2, description="Days since last irrigation")
    irrigation_efficiency: Optional[float] = Field(0.85, description="Irrigation system efficiency")
    farm_area_m2: Optional[float] = Field(1000, description="Farm area in square meters")


class AudioFeatures(BaseModel):
    mfcc_features: List[float] = Field(..., description="MFCC audio features")
    spectral_features: List[float] = Field(..., description="Spectral audio features")
    temporal_features: List[float] = Field(..., description="Temporal audio features")


# Solar Forecasting Endpoints
@router.post(
    "/solar/predict-power",
    summary="Predict Solar Power Output",
    description="Predict current solar power output based on weather conditions"
)
async def predict_solar_power(weather_data: WeatherData):
    """Predict solar power output based on current weather conditions"""
    try:
        weather_dict = weather_data.dict()
        prediction = solar_forecaster.predict_power_output(weather_dict)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Solar prediction failed: {str(e)}"
        )


@router.post(
    "/solar/daily-forecast",
    summary="Daily Solar Generation Forecast",
    description="Predict daily solar generation based on weather forecast"
)
async def daily_solar_forecast(weather_forecast: List[WeatherData]):
    """Generate daily solar power forecast"""
    try:
        forecast_data = [w.dict() for w in weather_forecast]
        prediction = solar_forecaster.predict_daily_generation(datetime.now(), forecast_data)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Daily forecast failed: {str(e)}"
        )


@router.post(
    "/solar/optimization-recommendations",
    summary="Solar Optimization Recommendations",
    description="Get AI-powered recommendations for energy optimization"
)
async def solar_optimization_recommendations(
    current_weather: WeatherData,
    weather_forecast: List[WeatherData]
):
    """Get solar energy optimization recommendations"""
    try:
        current_dict = current_weather.dict()
        forecast_data = [w.dict() for w in weather_forecast]
        
        recommendations = solar_forecaster.get_optimization_recommendations(
            current_dict, forecast_data
        )
        return recommendations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization recommendations failed: {str(e)}"
        )


# Pump Anomaly Detection Endpoints
@router.post(
    "/pump/analyze-operational",
    summary="Analyze Pump Operational Parameters",
    description="Analyze pump operational data for anomalies"
)
async def analyze_pump_operational(operational_data: PumpOperationalData):
    """Analyze pump operational parameters for anomalies"""
    try:
        data_dict = operational_data.dict()
        analysis = pump_detector.analyze_operational_parameters(data_dict)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pump operational analysis failed: {str(e)}"
        )


@router.post(
    "/pump/analyze-audio",
    summary="Analyze Pump Audio",
    description="Analyze pump audio for anomaly detection"
)
async def analyze_pump_audio(audio_features: AudioFeatures):
    """Analyze pump audio features for anomalies"""
    try:
        # Combine all audio features into single vector
        all_features = (
            audio_features.mfcc_features + 
            audio_features.spectral_features + 
            audio_features.temporal_features
        )
        
        analysis = pump_detector.analyze_pump_audio(all_features)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pump audio analysis failed: {str(e)}"
        )


@router.post(
    "/pump/comprehensive-health-check",
    summary="Comprehensive Pump Health Check",
    description="Perform comprehensive pump health analysis using both audio and operational data"
)
async def comprehensive_pump_health_check(
    operational_data: PumpOperationalData,
    audio_features: AudioFeatures
):
    """Perform comprehensive pump health analysis"""
    try:
        # Prepare data
        operational_dict = operational_data.dict()
        all_audio_features = (
            audio_features.mfcc_features + 
            audio_features.spectral_features + 
            audio_features.temporal_features
        )
        
        # Perform comprehensive analysis
        analysis = pump_detector.comprehensive_health_check(
            all_audio_features, operational_dict
        )
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive health check failed: {str(e)}"
        )


# Irrigation Optimization Endpoints
@router.post(
    "/irrigation/predict-soil-moisture",
    summary="Predict Soil Moisture",
    description="Predict soil moisture based on environmental conditions"
)
async def predict_soil_moisture(
    environmental_data: WeatherData,
    farm_data: FarmData
):
    """Predict soil moisture levels"""
    try:
        env_dict = environmental_data.dict()
        farm_dict = farm_data.dict()
        
        prediction = irrigation_optimizer.predict_soil_moisture(env_dict, farm_dict)
        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Soil moisture prediction failed: {str(e)}"
        )


@router.post(
    "/irrigation/calculate-water-demand",
    summary="Calculate Water Demand",
    description="Calculate crop water demand based on environmental conditions"
)
async def calculate_water_demand(
    environmental_data: WeatherData,
    farm_data: FarmData
):
    """Calculate crop water demand"""
    try:
        env_dict = environmental_data.dict()
        farm_dict = farm_data.dict()
        
        demand = irrigation_optimizer.calculate_water_demand(env_dict, farm_dict)
        return demand
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Water demand calculation failed: {str(e)}"
        )


@router.post(
    "/irrigation/optimize-schedule",
    summary="Optimize Irrigation Schedule",
    description="Generate AI-optimized irrigation schedule"
)
async def optimize_irrigation_schedule(
    environmental_data: WeatherData,
    farm_data: FarmData,
    solar_forecast: List[WeatherData]
):
    """Generate optimized irrigation schedule"""
    try:
        env_dict = environmental_data.dict()
        farm_dict = farm_data.dict()
        
        # Convert solar forecast to simple power predictions
        solar_data = []
        for weather in solar_forecast:
            power_prediction = solar_forecaster.predict_power_output(weather.dict())
            solar_data.append(power_prediction)
        
        optimization = irrigation_optimizer.optimize_irrigation_schedule(
            env_dict, farm_dict, solar_data
        )
        return optimization
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Irrigation optimization failed: {str(e)}"
        )


# Integrated AI Dashboard Endpoint
@router.post(
    "/dashboard/farmer-insights",
    summary="Farmer AI Dashboard",
    description="Get comprehensive AI insights for farmer dashboard"
)
async def farmer_ai_insights(
    current_weather: WeatherData,
    weather_forecast: List[WeatherData],
    farm_data: FarmData,
    pump_operational: Optional[PumpOperationalData] = None
):
    """Get comprehensive AI insights for farmer dashboard"""
    try:
        insights = {}
        
        # Solar insights
        current_dict = current_weather.dict()
        forecast_data = [w.dict() for w in weather_forecast]
        
        insights['solar'] = solar_forecaster.get_optimization_recommendations(
            current_dict, forecast_data
        )
        
        # Irrigation insights
        farm_dict = farm_data.dict()
        solar_predictions = [solar_forecaster.predict_power_output(w.dict()) for w in weather_forecast]
        
        insights['irrigation'] = irrigation_optimizer.optimize_irrigation_schedule(
            current_dict, farm_dict, solar_predictions
        )
        
        # Pump insights (if operational data provided)
        if pump_operational:
            pump_dict = pump_operational.dict()
            insights['pump'] = pump_detector.analyze_operational_parameters(pump_dict)
        
        # Overall recommendations
        insights['overall_recommendations'] = _generate_overall_recommendations(insights)
        
        return insights
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI insights generation failed: {str(e)}"
        )


def _generate_overall_recommendations(insights: Dict) -> List[Dict]:
    """Generate overall recommendations based on all AI insights"""
    recommendations = []
    
    # Solar recommendations
    solar_recs = insights.get('solar', {}).get('recommendations', [])
    for rec in solar_recs:
        recommendations.append({
            'category': 'energy',
            'priority': rec.get('priority', 'medium'),
            'message': rec.get('message', ''),
            'action': rec.get('action', '')
        })
    
    # Irrigation recommendations
    irrigation_recs = insights.get('irrigation', {}).get('irrigation_recommendations', [])
    for rec in irrigation_recs:
        recommendations.append({
            'category': 'irrigation',
            'priority': rec.get('priority', 'medium'),
            'message': rec.get('message', ''),
            'action': rec.get('action', '')
        })
    
    # Pump recommendations
    pump_analysis = insights.get('pump', {})
    if pump_analysis.get('is_anomaly_detected'):
        recommendations.append({
            'category': 'maintenance',
            'priority': 'high',
            'message': 'Pump anomaly detected - schedule inspection',
            'action': 'inspect_pump'
        })
    
    # Sort by priority
    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return recommendations


# Health check endpoint for AI services
@router.get(
    "/health",
    summary="AI Services Health Check",
    description="Check the health status of all AI services"
)
async def ai_health_check():
    """Check health status of AI services"""
    try:
        # Test each AI module
        health_status = {
            'solar_forecaster': 'healthy',
            'pump_detector': 'healthy',
            'irrigation_optimizer': 'healthy',
            'timestamp': datetime.now().isoformat()
        }
        
        # Quick test of each module
        test_weather = {
            'ambient_temperature': 25,
            'irradiation': 500,
            'humidity': 60
        }
        
        # Test solar forecaster
        try:
            solar_forecaster.predict_power_output(test_weather)
        except Exception:
            health_status['solar_forecaster'] = 'error'
        
        # Test pump detector
        try:
            test_operational = {
                'flow_rate': 50, 'pressure': 3.5, 'power_consumption': 5.2,
                'vibration_level': 0.1, 'temperature': 45
            }
            pump_detector.analyze_operational_parameters(test_operational)
        except Exception:
            health_status['pump_detector'] = 'error'
        
        # Test irrigation optimizer
        try:
            test_farm = {'farm_type': 'cereales', 'soil_type': 'limoneux'}
            irrigation_optimizer.predict_soil_moisture(test_weather, test_farm)
        except Exception:
            health_status['irrigation_optimizer'] = 'error'
        
        return health_status
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}"
        )