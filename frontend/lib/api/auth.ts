const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

export interface LoginCredentials {
  phone: string;
  password?: string;
  use_otp?: boolean;
}

export interface RegisterData {
  name: string;
  surname: string;
  phone: string;
  email?: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
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
  };
}

export interface MessageResponse {
  message: string;
  detail?: string;
}

class AuthAPI {
  private baseURL: string;

  constructor() {
    this.baseURL = `${API_BASE_URL}${API_VERSION}/auth`;
  }

  async login(credentials: LoginCredentials): Promise<AuthResponse | MessageResponse> {
    const response = await fetch(`${this.baseURL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Login failed');
    }

    return response.json();
  }

  async register(data: RegisterData): Promise<MessageResponse> {
    const response = await fetch(`${this.baseURL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Registration failed');
    }

    return response.json();
  }

  async verifyOTP(phone: string, code: string): Promise<AuthResponse> {
    const response = await fetch(`${this.baseURL}/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone, code }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'OTP verification failed');
    }

    return response.json();
  }

  async resetPassword(phone: string): Promise<MessageResponse> {
    const response = await fetch(`${this.baseURL}/reset-password`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Password reset request failed');
    }

    return response.json();
  }

  async confirmReset(phone: string, code: string, new_password: string): Promise<MessageResponse> {
    const response = await fetch(`${this.baseURL}/confirm-reset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phone, code, new_password }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Password reset confirmation failed');
    }

    return response.json();
  }
}

export const authAPI = new AuthAPI();
