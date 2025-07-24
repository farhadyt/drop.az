// src/types/auth.ts

export interface User {
  id: number;
  phone: string;
  first_name: string;
  last_name?: string;
  email?: string;
  gender: 'M' | 'F';
  birth_date?: string;
  age?: number;
  is_phone_verified: boolean;
  created_at: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: User;
}

export interface RegisterData {
  phone: string;
  first_name: string;
  gender: 'M' | 'F';
  birth_date?: string;
}

export interface OTPVerifyData {
  phone: string;
  otp_code: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface PhoneFormData {
  phone: string;
}

export interface OTPFormData {
  otp: string;
}

export interface ProfileFormData {
  first_name: string;
  gender: 'M' | 'F';
  birth_date?: string;
}