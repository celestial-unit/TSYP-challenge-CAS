'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Loader2, Sprout, CheckCircle2, AlertCircle } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function CompleteProfilePage() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [user, setUser] = useState<any>(null);

    // Form data
    const [formData, setFormData] = useState({
        surname: '',
        email: '',
        farm_location: '',
        farm_type: '',
        pump_power_kw: '',
        water_tank_size: '',
        soil_type: '',
        irrigation_method: ''
    });

    useEffect(() => {
        // Check if user is logged in
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');

        if (!token || !userData) {
            router.push('/farmer/login');
            return;
        }

        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);

        // Pre-fill form with existing data
        setFormData({
            surname: parsedUser.surname || '',
            email: parsedUser.email || '',
            farm_location: parsedUser.farm_location || '',
            farm_type: parsedUser.farm_type || '',
            pump_power_kw: parsedUser.pump_power_kw?.toString() || '',
            water_tank_size: parsedUser.water_tank_size?.toString() || '',
            soil_type: parsedUser.soil_type || '',
            irrigation_method: parsedUser.irrigation_method || ''
        });
    }, [router]);

    const handleInputChange = (field: string, value: string) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const token = localStorage.getItem('token');

            const response = await fetch(`${API_BASE_URL}/api/v1/role-auth/farmer/complete-profile`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    ...formData,
                    pump_power_kw: formData.pump_power_kw ? parseFloat(formData.pump_power_kw) : null,
                    water_tank_size: formData.water_tank_size ? parseFloat(formData.water_tank_size) : null
                }),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to complete profile');
            }

            const data = await response.json();

            // Update stored user data
            localStorage.setItem('user', JSON.stringify(data.user));

            // Redirect to dashboard
            router.push('/dashboard/farmer');
        } catch (err: any) {
            setError(err.message || 'Une erreur est survenue');
        } finally {
            setLoading(false);
        }
    };

    const handleSkip = () => {
        // Skip profile completion and go to dashboard
        router.push('/dashboard/farmer');
    };

    if (!user) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin" />
            </div>
        );
    }

    return (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 px-4 py-8 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="w-full max-w-2xl"
            >
                <Card className="shadow-lg">
                    <CardHeader className="space-y-1">
                        <div className="flex items-center gap-2">
                            <div className="rounded-full bg-green-100 p-2 dark:bg-green-900/30">
                                <Sprout className="h-6 w-6 text-green-600 dark:text-green-400" />
                            </div>
                        </div>
                        <CardTitle className="text-2xl font-bold text-green-800 dark:text-green-300">
                            Compléter votre profil
                        </CardTitle>
                        <CardDescription>
                            Bienvenue {user.name}! Ajoutez les détails de votre exploitation pour une meilleure expérience.
                        </CardDescription>
                    </CardHeader>

                    <CardContent>
                        {error && (
                            <Alert variant="destructive" className="mb-4">
                                <AlertCircle className="h-4 w-4" />
                                <AlertDescription>{error}</AlertDescription>
                            </Alert>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-6">
                            {/* Personal Information */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-semibold text-green-800 dark:text-green-300">
                                    Informations personnelles
                                </h3>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="surname">Nom de famille (optionnel)</Label>
                                        <Input
                                            id="surname"
                                            type="text"
                                            placeholder="Ben Ahmed"
                                            value={formData.surname}
                                            onChange={(e) => handleInputChange('surname', e.target.value)}
                                            disabled={loading}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="email">Email (optionnel)</Label>
                                        <Input
                                            id="email"
                                            type="email"
                                            placeholder="farmer@example.tn"
                                            value={formData.email}
                                            onChange={(e) => handleInputChange('email', e.target.value)}
                                            disabled={loading}
                                        />
                                    </div>
                                </div>
                            </div>

                            {/* Farm Information */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-semibold text-green-800 dark:text-green-300">
                                    Informations sur l'exploitation
                                </h3>


                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="farm_location">Localisation de la ferme *</Label>
                                        <Input
                                            id="farm_location"
                                            type="text"
                                            placeholder="Kairouan, Tunisie"
                                            value={formData.farm_location}
                                            onChange={(e) => handleInputChange('farm_location', e.target.value)}
                                            required
                                            disabled={loading}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="farm_type">Type de culture *</Label>
                                        <Select
                                            value={formData.farm_type}
                                            onValueChange={(value) => handleInputChange('farm_type', value)}
                                            disabled={loading}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Sélectionner le type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="cereales">Céréales</SelectItem>
                                                <SelectItem value="legumes">Légumes</SelectItem>
                                                <SelectItem value="fruits">Fruits</SelectItem>
                                                <SelectItem value="olives">Olives</SelectItem>
                                                <SelectItem value="agrumes">Agrumes</SelectItem>
                                                <SelectItem value="fourrage">Fourrage</SelectItem>
                                                <SelectItem value="mixte">Mixte</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                            </div>

                            {/* Irrigation System */}
                            <div className="space-y-4">
                                <h3 className="text-lg font-semibold text-green-800 dark:text-green-300">
                                    Système d'irrigation
                                </h3>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="pump_power_kw">Puissance de la pompe (kW)</Label>
                                        <Input
                                            id="pump_power_kw"
                                            type="number"
                                            step="0.1"
                                            placeholder="5.5"
                                            value={formData.pump_power_kw}
                                            onChange={(e) => handleInputChange('pump_power_kw', e.target.value)}
                                            disabled={loading}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="water_tank_size">Capacité du réservoir (L)</Label>
                                        <Input
                                            id="water_tank_size"
                                            type="number"
                                            placeholder="10000"
                                            value={formData.water_tank_size}
                                            onChange={(e) => handleInputChange('water_tank_size', e.target.value)}
                                            disabled={loading}
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="soil_type">Type de sol</Label>
                                        <Select
                                            value={formData.soil_type}
                                            onValueChange={(value) => handleInputChange('soil_type', value)}
                                            disabled={loading}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Sélectionner le type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="argileux">Argileux</SelectItem>
                                                <SelectItem value="sableux">Sableux</SelectItem>
                                                <SelectItem value="limoneux">Limoneux</SelectItem>
                                                <SelectItem value="calcaire">Calcaire</SelectItem>
                                                <SelectItem value="mixte">Mixte</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>

                                    <div className="space-y-2">
                                        <Label htmlFor="irrigation_method">Méthode d'irrigation</Label>
                                        <Select
                                            value={formData.irrigation_method}
                                            onValueChange={(value) => handleInputChange('irrigation_method', value)}
                                            disabled={loading}
                                        >
                                            <SelectTrigger>
                                                <SelectValue placeholder="Sélectionner la méthode" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="goutte-a-goutte">Goutte à goutte</SelectItem>
                                                <SelectItem value="aspersion">Aspersion</SelectItem>
                                                <SelectItem value="gravitaire">Gravitaire</SelectItem>
                                                <SelectItem value="micro-aspersion">Micro-aspersion</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                            </div>

                            <div className="flex gap-4 pt-4">
                                <Button
                                    type="button"
                                    variant="outline"
                                    onClick={handleSkip}
                                    disabled={loading}
                                    className="flex-1"
                                >
                                    Passer pour l'instant
                                </Button>
                                <Button
                                    type="submit"
                                    className="flex-1 bg-green-600 hover:bg-green-700"
                                    disabled={loading || !formData.farm_location || !formData.farm_type}
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                            Enregistrement...
                                        </>
                                    ) : (
                                        <>
                                            <CheckCircle2 className="mr-2 h-4 w-4" />
                                            Compléter le profil
                                        </>
                                    )}
                                </Button>
                            </div>
                        </form>
                    </CardContent>
                </Card>
            </motion.div>
        </div>
    );
}