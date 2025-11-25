'use client';

import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Sprout, Users } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

export default function Home() {
  const router = useRouter();

  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.2,
        duration: 0.6,
        ease: [0.6, -0.05, 0.01, 0.99],
      },
    }),
    hover: {
      scale: 1.05,
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15)',
      transition: {
        duration: 0.3,
        ease: 'easeInOut',
      },
    },
    tap: {
      scale: 0.98,
    },
  };

  const iconVariants = {
    hover: {
      rotate: [0, -10, 10, -10, 0],
      scale: 1.2,
      transition: {
        duration: 0.5,
      },
    },
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 via-white to-green-50 px-4 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950">
      <div className="w-full max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-12 text-center"
        >
          <h1 className="mb-4 text-5xl font-bold text-zinc-900 dark:text-zinc-50">
            SREMS-TN
          </h1>
          <p className="text-xl text-muted-foreground">
            Smart Renewable Energy Management System
          </p>
          <p className="mt-2 text-lg text-muted-foreground">
            Choisissez votre type de compte pour continuer
          </p>
        </motion.div>

        <div className="grid gap-8 md:grid-cols-2">
          {/* Farmer Card */}
          <motion.div
            custom={0}
            initial="hidden"
            animate="visible"
            whileHover="hover"
            whileTap="tap"
            variants={cardVariants}
            onClick={() => router.push('/farmer/login')}
            className="cursor-pointer"
          >
            <Card className="h-full border-2 border-green-200 bg-gradient-to-br from-green-50 to-emerald-50 transition-all hover:border-green-400 dark:from-green-950/20 dark:to-emerald-950/20 dark:border-green-800">
              <CardHeader className="text-center">
                <motion.div
                  variants={iconVariants}
                  className="mb-4 flex justify-center"
                >
                  <div className="rounded-full bg-green-100 p-6 dark:bg-green-900/30">
                    <Sprout className="h-16 w-16 text-green-600 dark:text-green-400" />
                  </div>
                </motion.div>
                <CardTitle className="text-3xl font-bold text-green-800 dark:text-green-300">
                  Agriculteur
                </CardTitle>
                <CardDescription className="text-lg text-green-700 dark:text-green-400">
                  Gestion de pompage et irrigation solaire
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-center">
                <p className="text-sm text-muted-foreground">
                  Connexion simple avec numéro de téléphone et code OTP
                </p>
                <ul className="space-y-2 text-left text-sm text-muted-foreground">
                  <li>✓ Surveillance de votre pompe solaire</li>
                  <li>✓ Gestion de l'irrigation intelligente</li>
                  <li>✓ Optimisation de la consommation d'eau</li>
                  <li>✓ Statistiques de production agricole</li>
                </ul>
                <motion.div
                  whileHover={{ x: 10 }}
                  className="mt-4 flex items-center justify-center gap-2 font-semibold text-green-600 dark:text-green-400"
                >
                  <span>Continuer</span>
                  <span>→</span>
                </motion.div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Other Users Card */}
          <motion.div
            custom={1}
            initial="hidden"
            animate="visible"
            whileHover="hover"
            whileTap="tap"
            variants={cardVariants}
            onClick={() => router.push('/login')}
            className="cursor-pointer"
          >
            <Card className="h-full border-2 border-blue-200 bg-gradient-to-br from-blue-50 to-indigo-50 transition-all hover:border-blue-400 dark:from-blue-950/20 dark:to-indigo-950/20 dark:border-blue-800">
              <CardHeader className="text-center">
                <motion.div
                  variants={iconVariants}
                  className="mb-4 flex justify-center"
                >
                  <div className="rounded-full bg-blue-100 p-6 dark:bg-blue-900/30">
                    <Users className="h-16 w-16 text-blue-600 dark:text-blue-400" />
                  </div>
                </motion.div>
                <CardTitle className="text-3xl font-bold text-blue-800 dark:text-blue-300">
                  Autres Utilisateurs
                </CardTitle>
                <CardDescription className="text-lg text-blue-700 dark:text-blue-400">
                  Particuliers, Techniciens, Opérateurs
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3 text-center">
                <p className="text-sm text-muted-foreground">
                  Connexion sécurisée avec email et mot de passe
                </p>
                <ul className="space-y-2 text-left text-sm text-muted-foreground">
                  <li>✓ Suivi de votre installation photovoltaïque</li>
                  <li>✓ Maintenance et support technique</li>
                  <li>✓ Gestion administrative et monitoring</li>
                  <li>✓ Tableaux de bord personnalisés</li>
                </ul>
                <motion.div
                  whileHover={{ x: 10 }}
                  className="mt-4 flex items-center justify-center gap-2 font-semibold text-blue-600 dark:text-blue-400"
                >
                  <span>Continuer</span>
                  <span>→</span>
                </motion.div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.6 }}
          className="mt-12 text-center text-sm text-muted-foreground"
        >
          <p>Plateforme de gestion intelligente des énergies renouvelables en Tunisie</p>
        </motion.div>
      </div>
    </div>
  );
}
