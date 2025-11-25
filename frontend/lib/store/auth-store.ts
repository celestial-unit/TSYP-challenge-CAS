import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  _id: string;
  name: string;
  surname: string;
  phone: string;
  email?: string;
  role: string;
  is_verified: boolean;
  created_at: string;
  last_login?: string;
  devices: Array<{
    device_id: string;
    type: string;
  }>;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      setAuth: (user, token) =>
        set({
          user,
          token,
          isAuthenticated: true,
        }),

      logout: () =>
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        }),

      updateUser: (userData) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...userData } : null,
        })),
    }),
    {
      name: 'srems-auth-storage',
    }
  )
);

// Helper to get full name
export const getFullName = (user: User | null): string => {
  if (!user) return '';
  return `${user.name} ${user.surname}`.trim();
};

// Helper to format role
export const formatRole = (role: string): string => {
  const roleMap: Record<string, string> = {
    particulier: 'Particulier',
    agriculteur: 'Agriculteur',
    technician: 'Technician',
    operator: 'Operator',
  };
  return roleMap[role.toLowerCase()] || role;
};
