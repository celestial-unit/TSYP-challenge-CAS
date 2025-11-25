'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Sprout, 
  Droplets, 
  Sun, 
  Battery, 
  TrendingUp, 
  Settings, 
  User,
  MapPin,
  Zap,
  Gauge,
  Calendar,
  AlertTriangle,
  RefreshCw,
  Brain
} from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function FarmerDashboard() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [aiInsights, setAiInsights] = useState<any>(null);
  const [loadingAI, setLoadingAI] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      router.push('/farmer/login');
      return;
    }
    
    const parsedUser = JSON.parse(userData);
    
    // Check if user is a farmer
    if (parsedUser.role !== 'agriculteur') {
      router.push('/login');
      return;
    }
    
    setUser(parsedUser);
    setLoading(false);
    
    // Load AI insights on component mount
    loadAIInsights();
  }, [router]);

  const loadAIInsights = async () => {
    setLoadingAI(true);
    try {
      // Sample data for AI predictions
      const currentWeather = {
        ambient_temperature: 28,
        module_temperature: 40,
        irradiation: 750,
        humidity: 45,
        wind_speed: 3,
        rainfall_24h: 0
      };

      const farmData = {
        farm_type: user?.farm_type || 'cereales',
        soil_type: user?.soil_type || 'limoneux',
        growth_stage: 'mid',
        days_since_irrigation: 2,
        irrigation_efficiency: 0.85,
        farm_area_m2: 1000
      };

      // Generate 24-hour weather forecast (simplified)
      const weatherForecast = Array.from({ length: 24 }, (_, i) => ({
        ambient_temperature: 25 + Math.sin(i * Math.PI / 12) * 8,
        module_temperature: 35 + Math.sin(i * Math.PI / 12) * 10,
        irradiation: Math.max(0, 800 * Math.sin(i * Math.PI / 12)),
        humidity: 50 + Math.random() * 20,
        wind_speed: 2 + Math.random() * 3
      }));

      // Call AI insights endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/ai/dashboard/farmer-insights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          current_weather: currentWeather,
          weather_forecast: weatherForecast,
          farm_data: farmData
        }),
      });

      if (response.ok) {
        const insights = await response.json();
        setAiInsights(insights);
      } else {
        console.error('Failed to load AI insights');
        // Set fallback data for demo
        setAiInsights({
          solar: {
            current_conditions: { predicted_power_kw: 4.2, confidence_score: 0.85 },
            recommendations: [
              { type: 'immediate', message: 'High solar output - Optimal time for irrigation', priority: 'high' }
            ]
          },
          irrigation: {
            current_soil_moisture: { predicted_soil_moisture_percent: 65, moisture_status: 'adequate' },
            irrigation_recommendations: [
              { priority: 'medium', message: 'Schedule irrigation in 4 hours for optimal efficiency' }
            ]
          }
        });
      }
    } catch (error) {
      console.error('Error loading AI insights:', error);
      // Set fallback data
      setAiInsights({
        solar: {
          current_conditions: { predicted_power_kw: 4.2, confidence_score: 0.85 },
          recommendations: [
            { type: 'immediate', message: 'High solar output - Optimal time for irrigation', priority: 'high' }
          ]
        },
        irrigation: {
          current_soil_moisture: { predicted_soil_moisture_percent: 65, moisture_status: 'adequate' },
          irrigation_recommendations: [
            { priority: 'medium', message: 'Schedule irrigation in 4 hours for optimal efficiency' }
          ]
        }
      });
    } finally {
      setLoadingAI(false);
    }
  };

  const handleCompleteProfile = () => {
    router.push('/farmer/complete-profile');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    router.push('/');
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const profileComplete = user.profile_completed;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-green-200 dark:bg-zinc-900/80 dark:border-zinc-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <div className="rounded-full bg-green-100 p-2 dark:bg-green-900/30">
                <Sprout className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-green-800 dark:text-green-300">
                  SREMS-TN Agriculteur
                </h1>
                <p className="text-sm text-muted-foreground">
                  Bienvenue, {user.name} {user.surname || ''}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" onClick={handleCompleteProfile}>
                <User className="h-4 w-4 mr-2" />
                Profil
              </Button>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                Déconnexion
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Profile Completion Alert */}
        {!profileComplete && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6"
          >
            <Card className="border-orange-200 bg-orange-50 dark:border-orange-800 dark:bg-orange-950/20">
              <CardContent className="flex items-center gap-4 pt-6">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <div className="flex-1">
                  <h3 className="font-semibold text-orange-800 dark:text-orange-300">
                    Profil incomplet
                  </h3>
                  <p className="text-sm text-orange-700 dark:text-orange-400">
                    Complétez votre profil pour accéder à toutes les fonctionnalités
                  </p>
                </div>
                <Button onClick={handleCompleteProfile} className="bg-orange-600 hover:bg-orange-700">
                  Compléter
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Farm Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MapPin className="h-5 w-5 text-green-600" />
                  Exploitation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground">Localisation</p>
                  <p className="font-medium">{user.farm_location || 'Non renseignée'}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Type de culture</p>
                  <p className="font-medium">{user.farm_type || 'Non renseigné'}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Méthode d'irrigation</p>
                  <p className="font-medium">{user.irrigation_method || 'Non renseignée'}</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* AI-Powered Solar System Status */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sun className="h-5 w-5 text-yellow-600" />
                  Système Solaire AI
                  <Brain className="h-4 w-4 text-blue-500" />
                </CardTitle>
                <CardDescription>
                  Prédictions en temps réel
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">État</span>
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    Opérationnel
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Production prédite (AI)</p>
                  <p className="text-2xl font-bold text-green-600">
                    {loadingAI ? '...' : `${aiInsights?.solar?.current_conditions?.predicted_power_kw?.toFixed(1) || '4.2'} kW`}
                  </p>
                  {aiInsights?.solar?.current_conditions?.confidence_score && (
                    <p className="text-xs text-muted-foreground">
                      Confiance: {(aiInsights.solar.current_conditions.confidence_score * 100).toFixed(0)}%
                    </p>
                  )}
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Recommandation AI</p>
                  <p className="font-medium text-sm">
                    {aiInsights?.solar?.recommendations?.[0]?.message || 'Conditions optimales pour l\'irrigation'}
                  </p>
                </div>
                <Button 
                  variant="outline" 
                  size="sm" 
                  onClick={loadAIInsights}
                  disabled={loadingAI}
                  className="w-full"
                >
                  {loadingAI ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Actualisation...
                    </>
                  ) : (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Actualiser AI
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </motion.div>

          {/* Pump Status */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-blue-600" />
                  Pompe
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-muted-foreground">État</span>
                  <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                    Arrêtée
                  </Badge>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Puissance</p>
                  <p className="font-medium">{user.pump_power_kw || 'N/A'} kW</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Dernière activation</p>
                  <p className="font-medium">Il y a 2h</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* AI-Powered Irrigation Insights */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Droplets className="h-5 w-5 text-blue-600" />
                  Irrigation Intelligente
                  <Brain className="h-4 w-4 text-blue-500" />
                </CardTitle>
                <CardDescription>
                  Analyse AI du sol et des besoins
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground">Humidité du sol (AI)</p>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{ 
                          width: `${aiInsights?.irrigation?.current_soil_moisture?.predicted_soil_moisture_percent || 65}%` 
                        }}
                      ></div>
                    </div>
                    <span className="text-sm font-medium">
                      {aiInsights?.irrigation?.current_soil_moisture?.predicted_soil_moisture_percent?.toFixed(0) || '65'}%
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">
                    État: {aiInsights?.irrigation?.current_soil_moisture?.moisture_status || 'adequate'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Recommandation AI</p>
                  <p className="font-medium text-sm">
                    {aiInsights?.irrigation?.irrigation_recommendations?.[0]?.message || 
                     'Irrigation recommandée dans 4 heures'}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Priorité</p>
                  <Badge 
                    variant={
                      aiInsights?.irrigation?.irrigation_recommendations?.[0]?.priority === 'high' ? 'destructive' :
                      aiInsights?.irrigation?.irrigation_recommendations?.[0]?.priority === 'medium' ? 'default' : 'secondary'
                    }
                  >
                    {aiInsights?.irrigation?.irrigation_recommendations?.[0]?.priority || 'medium'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Energy Statistics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-600" />
                  Statistiques
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm text-muted-foreground">Cette semaine</p>
                  <p className="text-xl font-bold text-green-600">185 kWh</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Ce mois</p>
                  <p className="font-medium">742 kWh</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Économies CO₂</p>
                  <p className="font-medium text-green-600">+125 kg</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5 text-gray-600" />
                  Actions rapides
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button variant="outline" className="w-full justify-start">
                  <Droplets className="h-4 w-4 mr-2" />
                  Démarrer irrigation
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => router.push('/dashboard/farmer/analytics')}
                >
                  <Gauge className="h-4 w-4 mr-2" />
                  Voir Analytics IA
                </Button>
                <Button variant="outline" className="w-full justify-start">
                  <Calendar className="h-4 w-4 mr-2" />
                  Programmer irrigation
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* AI Assistant Section - Live Predictions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          className="mt-8"
        >
          <Card className="border-2 border-green-300 bg-green-50/50 dark:border-green-700 dark:bg-green-950/20">
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-green-800 dark:text-green-300">
                <Brain className="h-5 w-5" />
                Assistant IA - Prédictions en Temps Réel
              </CardTitle>
              <CardDescription>
                Optimisation intelligente basée sur l'IA pour votre exploitation agricole
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loadingAI ? (
                <div className="text-center py-8">
                  <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-green-600" />
                  <p className="text-muted-foreground">Chargement des prédictions IA...</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Solar Predictions */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-green-800 dark:text-green-300 flex items-center gap-2">
                      <Sun className="h-4 w-4" />
                      Prédictions Solaires
                    </h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Production actuelle:</span>
                        <span className="font-medium">
                          {aiInsights?.solar?.current_conditions?.predicted_power_kw?.toFixed(1) || '4.2'} kW
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Confiance:</span>
                        <span className="font-medium">
                          {aiInsights?.solar?.current_conditions?.confidence_score ? 
                            `${(aiInsights.solar.current_conditions.confidence_score * 100).toFixed(0)}%` : '85%'}
                        </span>
                      </div>
                      <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                        <p className="text-sm text-yellow-800">
                          💡 {aiInsights?.solar?.recommendations?.[0]?.message || 
                              'Conditions optimales pour l\'irrigation solaire'}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Irrigation Predictions */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-green-800 dark:text-green-300 flex items-center gap-2">
                      <Droplets className="h-4 w-4" />
                      Prédictions Irrigation
                    </h4>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">Humidité du sol:</span>
                        <span className="font-medium">
                          {aiInsights?.irrigation?.current_soil_moisture?.predicted_soil_moisture_percent?.toFixed(0) || '65'}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm text-muted-foreground">État:</span>
                        <Badge variant="secondary">
                          {aiInsights?.irrigation?.current_soil_moisture?.moisture_status || 'adequate'}
                        </Badge>
                      </div>
                      <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <p className="text-sm text-blue-800">
                          💧 {aiInsights?.irrigation?.irrigation_recommendations?.[0]?.message || 
                              'Irrigation recommandée dans les prochaines heures'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div className="mt-6 flex gap-4">
                <Button 
                  onClick={loadAIInsights}
                  disabled={loadingAI}
                  className="bg-green-600 hover:bg-green-700"
                >
                  {loadingAI ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Actualisation...
                    </>
                  ) : (
                    <>
                      <Brain className="h-4 w-4 mr-2" />
                      Actualiser Prédictions IA
                    </>
                  )}
                </Button>
                <Button variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Paramètres IA
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </main>
    </div>
  );
}