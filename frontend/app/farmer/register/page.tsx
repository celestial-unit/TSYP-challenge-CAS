'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Loader2, Sprout, CheckCircle2, AlertCircle, ArrowLeft } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function FarmerRegisterPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [otpCode, setOtpCode] = useState('');
  const [step, setStep] = useState<'register' | 'verify'>('register');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showOtpDialog, setShowOtpDialog] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/role-auth/farmer/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name.trim(),
          phone: phone.trim(),
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Inscription échouée');
      }

      // Show OTP dialog
      setShowOtpDialog(true);
      setStep('verify');
    } catch (err: any) {
      setError(err.message || 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/role-auth/farmer/verify-otp`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ phone: phone.trim(), code: otpCode }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Vérification OTP échouée');
      }

      const data = await response.json();
      
      // Store auth data
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      
      setShowOtpDialog(false);
      
      // Redirect to profile completion
      router.push('/farmer/complete-profile?message=registration_success');
    } catch (err: any) {
      setError(err.message || 'Vérification échouée');
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setOtpCode('');
    setError('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/role-auth/farmer/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name.trim(),
          phone: phone.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error('Échec du renvoi du code');
      }
    } catch (err: any) {
      setError(err.message || 'Échec du renvoi');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50 px-4 py-8 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="shadow-lg">
          <CardHeader className="space-y-1">
            <div className="flex items-center gap-2">
              <Link href="/">
                <Button variant="ghost" size="icon" className="h-8 w-8">
                  <ArrowLeft className="h-4 w-4" />
                </Button>
              </Link>
              <div className="rounded-full bg-green-100 p-2 dark:bg-green-900/30">
                <Sprout className="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold text-green-800 dark:text-green-300">
              Inscription Agriculteur
            </CardTitle>
            <CardDescription>
              Créez votre compte en quelques secondes
            </CardDescription>
          </CardHeader>

          <CardContent>
            {error && !showOtpDialog && (
              <Alert variant="destructive" className="mb-4">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <form onSubmit={handleRegister} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">Prénom</Label>
                <Input
                  id="name"
                  type="text"
                  placeholder="Mohamed"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  disabled={loading || step === 'verify'}
                  minLength={2}
                  maxLength={100}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="phone">Numéro de téléphone</Label>
                <Input
                  id="phone"
                  type="tel"
                  placeholder="+216 98 765 432"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  required
                  disabled={loading || step === 'verify'}
                />
                <p className="text-xs text-muted-foreground">
                  Format Tunisie : +216 XX XXX XXX
                </p>
              </div>

              <Alert className="border-green-200 bg-green-50 text-green-800 dark:border-green-800 dark:bg-green-950 dark:text-green-200">
                <CheckCircle2 className="h-4 w-4" />
                <AlertDescription className="text-xs">
                  Connexion simplifiée : pas besoin de mot de passe !
                  Vous recevrez un code par SMS à chaque connexion.
                </AlertDescription>
              </Alert>

              <Button
                type="submit"
                className="w-full bg-green-600 hover:bg-green-700"
                disabled={loading || step === 'verify' || !name || !phone}
              >
                {loading && step === 'register' ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Inscription...
                  </>
                ) : (
                  'S\'inscrire'
                )}
              </Button>
            </form>

            <div className="mt-4 space-y-2 rounded-md border p-3 text-xs text-muted-foreground">
              <p className="font-medium">Après inscription :</p>
              <ul className="list-inside list-disc space-y-1">
                <li>Vous pourrez compléter votre profil (optionnel)</li>
                <li>Ajouter les détails de votre ferme et pompe</li>
                <li>Connecter vos équipements de mesure</li>
              </ul>
            </div>
          </CardContent>

          <CardFooter className="flex justify-center">
            <p className="text-sm text-muted-foreground">
              Déjà inscrit?{' '}
              <Link href="/farmer/login" className="font-medium text-green-600 hover:underline dark:text-green-400">
                Se connecter
              </Link>
            </p>
          </CardFooter>
        </Card>
      </motion.div>

      {/* OTP Verification Dialog */}
      <Dialog open={showOtpDialog} onOpenChange={setShowOtpDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Sprout className="h-5 w-5 text-green-600" />
              Vérification OTP
            </DialogTitle>
            <DialogDescription>
              Un code à 6 chiffres a été envoyé au {phone}
            </DialogDescription>
          </DialogHeader>

          {error && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="otp-dialog">Code OTP</Label>
              <Input
                id="otp-dialog"
                type="text"
                placeholder="123456"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                maxLength={6}
                disabled={loading}
                className="text-center text-2xl tracking-widest"
                autoFocus
              />
            </div>

            <Button
              variant="link"
              onClick={handleResendOTP}
              disabled={loading}
              className="w-full text-sm"
            >
              Renvoyer le code
            </Button>
          </div>

          <DialogFooter>
            <Button
              onClick={handleVerifyOTP}
              disabled={loading || otpCode.length !== 6}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Vérification...
                </>
              ) : (
                'Vérifier et continuer'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
