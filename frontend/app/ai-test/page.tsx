'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Brain, Sun, Droplets, Zap, RefreshCw } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AITestPage() {
  const [solarPrediction, setSolarPrediction] = useState<any>(null);
  const [pumpAnalysis, setPumpAnalysis] = useState<any>(null);
  const [irrigationOptimization, setIrrigationOptimization] = useState<any>(null);
  const [loading, setLoading] = useState<{ [key: string]: boolean }>({});

  // Test data
  const [weatherData, setWeatherData] = useState({
    ambient_temperature: 28,
    module_temperature: 40,
    irradiation: 750,
    humidity: 45,
    wind_speed: 3
  });

  const [pumpData, setPumpData] = useState({
    flow_rate: 45,
    pressure: 3.2,
    power_consumption: 5.5,
    vibration_level: 0.15,
    temperature: 48
  });

  const testSolarPrediction = async () => {
    setLoading(prev => ({ ...prev, solar: true }));
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/solar/predict-power`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(weatherData)
      });
      
      if (response.ok) {
        const result = await response.json();
        setSolarPrediction(result);
      } else {
        console.error('Solar prediction failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(prev => ({ ...prev, solar: false }));
    }
  };

  const testPumpAnalysis = async () => {
    setLoading(prev => ({ ...prev, pump: true }));
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/pump/analyze-operational`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pumpData)
      });
      
      if (response.ok) {
        const result = await response.json();
        setPumpAnalysis(result);
      } else {
        console.error('Pump analysis failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(prev => ({ ...prev, pump: false }));
    }
  };

  const testIrrigationOptimization = async () => {
    setLoading(prev => ({ ...prev, irrigation: true }));
    try {
      const farmData = {
        farm_type: 'cereales',
        soil_type: 'limoneux',
        growth_stage: 'mid',
        days_since_irrigation: 3,
        irrigation_efficiency: 0.85
      };

      const solarForecast = Array.from({ length: 6 }, (_, i) => ({
        ambient_temperature: 25 + i * 2,
        irradiation: 600 + i * 50,
        humidity: 50,
        wind_speed: 2
      }));

      const response = await fetch(`${API_BASE_URL}/api/v1/ai/irrigation/optimize-schedule`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          environmental_data: weatherData,
          farm_data: farmData,
          solar_forecast: solarForecast
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        setIrrigationOptimization(result);
      } else {
        console.error('Irrigation optimization failed');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(prev => ({ ...prev, irrigation: false }));
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4 flex items-center justify-center gap-3">
            <Brain className="h-10 w-10 text-blue-600" />
            SREMS-TN AI Test Dashboard
          </h1>
          <p className="text-xl text-gray-600">
            Test des prédictions IA en temps réel
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Solar Prediction Test */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sun className="h-5 w-5 text-yellow-600" />
                Prédiction Solaire
              </CardTitle>
              <CardDescription>
                Test de prédiction de production solaire
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <Label htmlFor="temp">Température (°C)</Label>
                  <Input
                    id="temp"
                    type="number"
                    value={weatherData.ambient_temperature}
                    onChange={(e) => setWeatherData(prev => ({
                      ...prev,
                      ambient_temperature: parseFloat(e.target.value)
                    }))}
                  />
                </div>
                <div>
                  <Label htmlFor="irradiation">Irradiation (W/m²)</Label>
                  <Input
                    id="irradiation"
                    type="number"
                    value={weatherData.irradiation}
                    onChange={(e) => setWeatherData(prev => ({
                      ...prev,
                      irradiation: parseFloat(e.target.value)
                    }))}
                  />
                </div>
              </div>
              
              <Button 
                onClick={testSolarPrediction}
                disabled={loading.solar}
                className="w-full"
              >
                {loading.solar ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Prédiction...
                  </>
                ) : (
                  'Tester Prédiction Solaire'
                )}
              </Button>

              {solarPrediction && (
                <div className="mt-4 p-4 bg-yellow-50 rounded-lg border">
                  <h4 className="font-semibold text-yellow-800 mb-2">Résultat IA:</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Puissance prédite:</span>
                      <span className="font-medium">{solarPrediction.predicted_power_kw?.toFixed(2)} kW</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Confiance:</span>
                      <span className="font-medium">{(solarPrediction.confidence_score * 100)?.toFixed(0)}%</span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Pump Analysis Test */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-blue-600" />
                Analyse Pompe
              </CardTitle>
              <CardDescription>
                Test d'analyse de santé de la pompe
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <Label htmlFor="flow">Débit (L/min)</Label>
                  <Input
                    id="flow"
                    type="number"
                    value={pumpData.flow_rate}
                    onChange={(e) => setPumpData(prev => ({
                      ...prev,
                      flow_rate: parseFloat(e.target.value)
                    }))}
                  />
                </div>
                <div>
                  <Label htmlFor="pressure">Pression (bar)</Label>
                  <Input
                    id="pressure"
                    type="number"
                    step="0.1"
                    value={pumpData.pressure}
                    onChange={(e) => setPumpData(prev => ({
                      ...prev,
                      pressure: parseFloat(e.target.value)
                    }))}
                  />
                </div>
              </div>
              
              <Button 
                onClick={testPumpAnalysis}
                disabled={loading.pump}
                className="w-full"
              >
                {loading.pump ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Analyse...
                  </>
                ) : (
                  'Tester Analyse Pompe'
                )}
              </Button>

              {pumpAnalysis && (
                <div className="mt-4 p-4 bg-blue-50 rounded-lg border">
                  <h4 className="font-semibold text-blue-800 mb-2">Résultat IA:</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Score santé:</span>
                      <span className="font-medium">{(pumpAnalysis.operational_health_score * 100)?.toFixed(0)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>État:</span>
                      <Badge variant={pumpAnalysis.status === 'normal' ? 'secondary' : 'destructive'}>
                        {pumpAnalysis.status}
                      </Badge>
                    </div>
                    <div className="flex justify-between">
                      <span>Anomalie:</span>
                      <span className="font-medium">{pumpAnalysis.is_anomaly_detected ? 'Oui' : 'Non'}</span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Irrigation Optimization Test */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Droplets className="h-5 w-5 text-green-600" />
                Optimisation Irrigation
              </CardTitle>
              <CardDescription>
                Test d'optimisation intelligente de l'irrigation
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-sm text-gray-600">
                <p>Culture: Céréales</p>
                <p>Sol: Limoneux</p>
                <p>Stade: Développement moyen</p>
                <p>Dernière irrigation: Il y a 3 jours</p>
              </div>
              
              <Button 
                onClick={testIrrigationOptimization}
                disabled={loading.irrigation}
                className="w-full"
              >
                {loading.irrigation ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Optimisation...
                  </>
                ) : (
                  'Tester Optimisation'
                )}
              </Button>

              {irrigationOptimization && (
                <div className="mt-4 p-4 bg-green-50 rounded-lg border">
                  <h4 className="font-semibold text-green-800 mb-2">Résultat IA:</h4>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span>Humidité sol:</span>
                      <span className="font-medium">
                        {irrigationOptimization.current_soil_moisture?.predicted_soil_moisture_percent?.toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>État:</span>
                      <Badge variant="secondary">
                        {irrigationOptimization.current_soil_moisture?.moisture_status}
                      </Badge>
                    </div>
                    <div className="mt-2">
                      <span className="text-xs text-green-700">
                        Recommandation: {irrigationOptimization.irrigation_recommendations?.[0]?.message}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* API Health Check */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>État des Services IA</CardTitle>
          </CardHeader>
          <CardContent>
            <Button 
              onClick={async () => {
                try {
                  const response = await fetch(`${API_BASE_URL}/api/v1/ai/health`);
                  const health = await response.json();
                  alert(`Services IA: ${JSON.stringify(health, null, 2)}`);
                } catch (error) {
                  alert('Erreur de connexion aux services IA');
                }
              }}
              variant="outline"
            >
              Vérifier État des Services IA
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}