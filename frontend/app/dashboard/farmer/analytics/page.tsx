'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell,
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer 
} from 'recharts';
import { 
  Sun, 
  Droplets, 
  Zap, 
  TrendingUp, 
  Calendar,
  BarChart3,
  PieChart as PieChartIcon,
  Activity,
  Leaf,
  Battery,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';

// Demo data for charts
const solarProductionData = [
  { time: '06:00', production: 0, prediction: 0 },
  { time: '07:00', production: 0.5, prediction: 0.8 },
  { time: '08:00', production: 2.1, prediction: 2.3 },
  { time: '09:00', production: 4.2, prediction: 4.1 },
  { time: '10:00', production: 6.8, prediction: 6.5 },
  { time: '11:00', production: 8.5, prediction: 8.2 },
  { time: '12:00', production: 9.2, prediction: 9.0 },
  { time: '13:00', production: 8.8, prediction: 8.9 },
  { time: '14:00', production: 7.5, prediction: 7.8 },
  { time: '15:00', production: 5.9, prediction: 6.2 },
  { time: '16:00', production: 3.8, prediction: 4.0 },
  { time: '17:00', production: 1.5, prediction: 1.8 },
  { time: '18:00', production: 0.2, prediction: 0.3 },
  { time: '19:00', production: 0, prediction: 0 }
];

const weeklyEnergyData = [
  { day: 'Lun', solar: 45, grid: 12, irrigation: 28, house: 29 },
  { day: 'Mar', solar: 52, grid: 8, irrigation: 32, house: 28 },
  { day: 'Mer', solar: 38, grid: 18, irrigation: 25, house: 31 },
  { day: 'Jeu', solar: 48, grid: 10, irrigation: 30, house: 28 },
  { day: 'Ven', solar: 55, grid: 5, irrigation: 35, house: 25 },
  { day: 'Sam', solar: 42, grid: 15, irrigation: 22, house: 35 },
  { day: 'Dim', solar: 39, grid: 16, irrigation: 20, house: 35 }
];

const soilMoistureData = [
  { date: '20/11', moisture: 75, optimal: 70, critical: 30 },
  { date: '21/11', moisture: 68, optimal: 70, critical: 30 },
  { date: '22/11', moisture: 62, optimal: 70, critical: 30 },
  { date: '23/11', moisture: 45, optimal: 70, critical: 30 },
  { date: '24/11', moisture: 38, optimal: 70, critical: 30 },
  { date: '25/11', moisture: 65, optimal: 70, critical: 30 },
  { date: '26/11', moisture: 72, optimal: 70, critical: 30 }
];

const pumpHealthData = [
  { metric: 'Débit', value: 85, status: 'normal' },
  { metric: 'Pression', value: 92, status: 'normal' },
  { metric: 'Température', value: 78, status: 'warning' },
  { metric: 'Vibration', value: 88, status: 'normal' },
  { metric: 'Consommation', value: 82, status: 'normal' }
];

const cropYieldPrediction = [
  { month: 'Jan', predicted: 2.1, actual: 2.0, optimal: 2.5 },
  { month: 'Fév', predicted: 2.3, actual: 2.2, optimal: 2.5 },
  { month: 'Mar', predicted: 2.8, actual: 2.7, optimal: 2.5 },
  { month: 'Avr', predicted: 3.2, actual: 3.1, optimal: 2.5 },
  { month: 'Mai', predicted: 3.5, actual: null, optimal: 2.5 },
  { month: 'Jun', predicted: 3.8, actual: null, optimal: 2.5 }
];

const energyDistribution = [
  { name: 'Irrigation', value: 45, color: '#3B82F6' },
  { name: 'Maison', value: 30, color: '#10B981' },
  { name: 'Équipements', value: 15, color: '#F59E0B' },
  { name: 'Stockage', value: 10, color: '#8B5CF6' }
];

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6'];

export default function FarmerAnalytics() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      router.push('/farmer/login');
      return;
    }
    
    const parsedUser = JSON.parse(userData);
    if (parsedUser.role !== 'agriculteur') {
      router.push('/login');
      return;
    }
    
    setUser(parsedUser);
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-green-200 dark:bg-zinc-900/80 dark:border-zinc-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center gap-3">
              <Link href="/dashboard/farmer">
                <Button variant="ghost" size="icon">
                  <ArrowLeft className="h-5 w-5" />
                </Button>
              </Link>
              <div className="rounded-full bg-green-100 p-2 dark:bg-green-900/30">
                <BarChart3 className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-green-800 dark:text-green-300">
                  Analytics IA - {user.name}
                </h1>
                <p className="text-sm text-muted-foreground">
                  Analyse intelligente de votre exploitation
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Production Solaire</p>
                    <p className="text-2xl font-bold text-yellow-600">47.2 kWh</p>
                    <p className="text-xs text-green-600">+12% vs hier</p>
                  </div>
                  <Sun className="h-8 w-8 text-yellow-600" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Consommation Eau</p>
                    <p className="text-2xl font-bold text-blue-600">1,250 L</p>
                    <p className="text-xs text-green-600">-8% optimisé</p>
                  </div>
                  <Droplets className="h-8 w-8 text-blue-600" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Santé Pompe</p>
                    <p className="text-2xl font-bold text-green-600">85%</p>
                    <p className="text-xs text-green-600">Excellent</p>
                  </div>
                  <Zap className="h-8 w-8 text-green-600" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">Efficacité IA</p>
                    <p className="text-2xl font-bold text-purple-600">92%</p>
                    <p className="text-xs text-green-600">Optimisé</p>
                  </div>
                  <Activity className="h-8 w-8 text-purple-600" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Analytics Tabs */}
        <Tabs defaultValue="energy" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="energy" className="flex items-center gap-2">
              <Sun className="h-4 w-4" />
              Énergie
            </TabsTrigger>
            <TabsTrigger value="irrigation" className="flex items-center gap-2">
              <Droplets className="h-4 w-4" />
              Irrigation
            </TabsTrigger>
            <TabsTrigger value="equipment" className="flex items-center gap-2">
              <Zap className="h-4 w-4" />
              Équipements
            </TabsTrigger>
            <TabsTrigger value="crops" className="flex items-center gap-2">
              <Leaf className="h-4 w-4" />
              Cultures
            </TabsTrigger>
          </TabsList>

          {/* Energy Analytics */}
          <TabsContent value="energy" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Sun className="h-5 w-5 text-yellow-600" />
                    Production Solaire Journalière
                  </CardTitle>
                  <CardDescription>
                    Prédictions IA vs Production Réelle
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={solarProductionData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="production" 
                        stroke="#F59E0B" 
                        strokeWidth={2}
                        name="Production Réelle"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="prediction" 
                        stroke="#3B82F6" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Prédiction IA"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Battery className="h-5 w-5 text-green-600" />
                    Consommation Énergétique Hebdomadaire
                  </CardTitle>
                  <CardDescription>
                    Répartition par source et usage
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={weeklyEnergyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="solar" stackId="a" fill="#F59E0B" name="Solaire" />
                      <Bar dataKey="grid" stackId="a" fill="#EF4444" name="Réseau" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card className="lg:col-span-2">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <PieChartIcon className="h-5 w-5 text-purple-600" />
                    Répartition de la Consommation Énergétique
                  </CardTitle>
                  <CardDescription>
                    Distribution intelligente optimisée par IA
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center justify-center">
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={energyDistribution}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {energyDistribution.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Irrigation Analytics */}
          <TabsContent value="irrigation" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Droplets className="h-5 w-5 text-blue-600" />
                    Humidité du Sol - Prédictions IA
                  </CardTitle>
                  <CardDescription>
                    Surveillance intelligente et seuils optimaux
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={soilMoistureData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Area 
                        type="monotone" 
                        dataKey="moisture" 
                        stroke="#3B82F6" 
                        fill="#3B82F6" 
                        fillOpacity={0.3}
                        name="Humidité Actuelle"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="optimal" 
                        stroke="#10B981" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Seuil Optimal"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="critical" 
                        stroke="#EF4444" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Seuil Critique"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recommandations IA Irrigation</CardTitle>
                  <CardDescription>
                    Optimisation basée sur les prédictions météo
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2 mb-2">
                      <Droplets className="h-4 w-4 text-blue-600" />
                      <span className="font-semibold text-blue-800">Prochaine Irrigation</span>
                    </div>
                    <p className="text-sm text-blue-700">
                      Recommandée dans 4 heures (14:00) pour optimiser l'absorption
                    </p>
                    <div className="mt-2 flex items-center gap-2">
                      <Badge variant="secondary">Priorité: Moyenne</Badge>
                      <Badge variant="outline">Durée: 45 min</Badge>
                    </div>
                  </div>

                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-2 mb-2">
                      <Sun className="h-4 w-4 text-green-600" />
                      <span className="font-semibold text-green-800">Synchronisation Solaire</span>
                    </div>
                    <p className="text-sm text-green-700">
                      Pic de production solaire prévu à 13:30 - Irrigation optimale
                    </p>
                    <div className="mt-2">
                      <Badge className="bg-green-600">Économie: 35% d'énergie</Badge>
                    </div>
                  </div>

                  <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                    <div className="flex items-center gap-2 mb-2">
                      <Calendar className="h-4 w-4 text-yellow-600" />
                      <span className="font-semibold text-yellow-800">Prévisions Météo</span>
                    </div>
                    <p className="text-sm text-yellow-700">
                      Pluie prévue demain (15mm) - Reporter l'irrigation de 24h
                    </p>
                    <div className="mt-2">
                      <Badge variant="outline">Économie: 150L d'eau</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Equipment Analytics */}
          <TabsContent value="equipment" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="h-5 w-5 text-blue-600" />
                    Santé des Équipements - Analyse IA
                  </CardTitle>
                  <CardDescription>
                    Surveillance prédictive et maintenance
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={pumpHealthData} layout="horizontal">
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis type="number" />
                      <YAxis dataKey="metric" type="category" />
                      <Tooltip />
                      <Bar 
                        dataKey="value" 
                        fill={(entry) => entry.status === 'normal' ? '#10B981' : '#F59E0B'}
                        name="Score de Santé (%)"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Alertes de Maintenance Prédictive</CardTitle>
                  <CardDescription>
                    Recommandations basées sur l'analyse IA
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-green-800">Pompe Principale</span>
                      <Badge className="bg-green-600">Excellent</Badge>
                    </div>
                    <p className="text-sm text-green-700">
                      Fonctionnement optimal. Prochaine maintenance dans 45 jours.
                    </p>
                  </div>

                  <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-yellow-800">Capteur Température</span>
                      <Badge className="bg-yellow-600">Attention</Badge>
                    </div>
                    <p className="text-sm text-yellow-700">
                      Température légèrement élevée. Vérifier la ventilation.
                    </p>
                    <Button size="sm" className="mt-2">Programmer Inspection</Button>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold text-blue-800">Panneaux Solaires</span>
                      <Badge className="bg-blue-600">Optimal</Badge>
                    </div>
                    <p className="text-sm text-blue-700">
                      Rendement à 94%. Nettoyage recommandé dans 2 semaines.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Crops Analytics */}
          <TabsContent value="crops" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Leaf className="h-5 w-5 text-green-600" />
                    Prédictions de Rendement - IA Agricole
                  </CardTitle>
                  <CardDescription>
                    Analyse prédictive basée sur les conditions optimales
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={cropYieldPrediction}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Line 
                        type="monotone" 
                        dataKey="predicted" 
                        stroke="#10B981" 
                        strokeWidth={2}
                        name="Rendement Prédit (t/ha)"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="actual" 
                        stroke="#3B82F6" 
                        strokeWidth={2}
                        name="Rendement Réel (t/ha)"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="optimal" 
                        stroke="#F59E0B" 
                        strokeWidth={2}
                        strokeDasharray="5 5"
                        name="Objectif (t/ha)"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Optimisations IA pour les Cultures</CardTitle>
                  <CardDescription>
                    Recommandations personnalisées pour votre exploitation
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp className="h-4 w-4 text-green-600" />
                      <span className="font-semibold text-green-800">Rendement Optimisé</span>
                    </div>
                    <p className="text-sm text-green-700">
                      L'IA prédit une amélioration de 15% du rendement avec l'irrigation optimisée
                    </p>
                    <div className="mt-2">
                      <Badge className="bg-green-600">+0.4 t/ha prévues</Badge>
                    </div>
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2 mb-2">
                      <Droplets className="h-4 w-4 text-blue-600" />
                      <span className="font-semibold text-blue-800">Économie d'Eau</span>
                    </div>
                    <p className="text-sm text-blue-700">
                      Réduction de 28% de la consommation d'eau grâce à l'irrigation intelligente
                    </p>
                    <div className="mt-2">
                      <Badge className="bg-blue-600">-350L/jour économisés</Badge>
                    </div>
                  </div>

                  <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                    <div className="flex items-center gap-2 mb-2">
                      <Activity className="h-4 w-4 text-purple-600" />
                      <span className="font-semibold text-purple-800">Santé des Cultures</span>
                    </div>
                    <p className="text-sm text-purple-700">
                      Surveillance IA détecte des conditions optimales pour la croissance
                    </p>
                    <div className="mt-2">
                      <Badge className="bg-purple-600">Score: 92/100</Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}