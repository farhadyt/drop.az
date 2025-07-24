// src/app/auth/phone/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { phoneFormSchema, PhoneFormData } from '@/lib/validations';
import { authAPI } from '@/lib/api';
import { useAuth } from '@/store/auth-store';

export default function PhonePage() {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { setError, clearError } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError: setFormError,
  } = useForm<PhoneFormData>({
    resolver: zodResolver(phoneFormSchema),
  });

  const onSubmit = async (data: PhoneFormData) => {
    setIsLoading(true);
    clearError();

    try {
      // First try to send OTP to existing user
      try {
        const response = await authAPI.sendOTP(data.phone);
        console.log('✅ Existing user OTP:', response.data);
      } catch (sendError: any) {
        // If user doesn't exist, create new user
        if (sendError.response?.status === 400) {
          console.log('📝 Creating new user...');
          const registerResponse = await authAPI.register({
            phone: data.phone,
            first_name: 'User', // Temporary name
            gender: 'M', // Temporary gender
          });
          console.log('✅ New user OTP:', registerResponse.data);
        } else {
          throw sendError;
        }
      }
      
      // Store phone in sessionStorage for next step
      sessionStorage.setItem('auth_phone', data.phone);
      
      // Navigate to OTP verification
      router.push('/auth/verify');
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.phone?.[0] || 
                          'Bir xəta baş verdi. Yenidən cəhd edin.';
      
      if (error.response?.status === 400 && error.response?.data?.phone) {
        setFormError('phone', { message: errorMessage });
      } else {
        setError(errorMessage);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            DROP.AZ
          </h1>
          <p className="text-gray-600">
            Dərmanları evə çatdırırıq
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
              Telefon nömrəsi
            </label>
            <input
              id="phone"
              type="tel"
              placeholder="+994 XX XXX XX XX"
              {...register('phone')}
              className={`
                w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent
                ${errors.phone ? 'border-red-500' : 'border-gray-300'}
              `}
              disabled={isLoading}
            />
            {errors.phone && (
              <p className="mt-2 text-sm text-red-600">
                {errors.phone.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`
              w-full py-3 px-4 rounded-lg font-medium text-white transition-colors
              ${isLoading 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-blue-500'
              }
            `}
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Göndərilir...
              </span>
            ) : (
              'OTP Kodu Göndər'
            )}
          </button>
        </form>

        {/* Info */}
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            Telefon nömrənizə SMS ilə 6 rəqəmli təsdiq kodu göndəriləcək
          </p>
        </div>
      </div>
    </div>
  );
}