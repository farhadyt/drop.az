// src/app/auth/verify/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { otpFormSchema, OTPFormData } from '@/lib/validations';
import { authAPI } from '@/lib/api';
import { useAuth } from '@/store/auth-store';

export default function VerifyPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [isResending, setIsResending] = useState(false);
  const [countdown, setCountdown] = useState(60);
  const [phone, setPhone] = useState<string>('');
  const router = useRouter();
  const { setUser, setTokens, setError, clearError } = useAuth();

  const {
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
    setError: setFormError,
  } = useForm<OTPFormData>({
    resolver: zodResolver(otpFormSchema),
  });

  const otpValue = watch('otp') || '';

  // Get phone from sessionStorage
  useEffect(() => {
    const storedPhone = sessionStorage.getItem('auth_phone');
    if (!storedPhone) {
      router.push('/auth/phone');
      return;
    }
    setPhone(storedPhone);
  }, [router]);

  // Countdown timer
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  // Handle OTP input changes
  const handleOTPChange = (index: number, value: string) => {
    if (value.length > 1) return; // Prevent multiple characters
    
    const newOTP = otpValue.split('');
    newOTP[index] = value;
    const updatedOTP = newOTP.join('').slice(0, 6);
    
    setValue('otp', updatedOTP);

    // Auto-focus next input
    if (value && index < 5) {
      const nextInput = document.getElementById(`otp-${index + 1}`) as HTMLInputElement;
      nextInput?.focus();
    }
  };

  // Handle backspace
  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !otpValue[index] && index > 0) {
      const prevInput = document.getElementById(`otp-${index - 1}`) as HTMLInputElement;
      prevInput?.focus();
    }
  };

  const onSubmit = async (data: OTPFormData) => {
    setIsLoading(true);
    clearError();

    try {
      const response = await authAPI.verifyOTP(phone, data.otp);
      const { access, refresh, user } = response.data;

      // Store tokens and user data
      setTokens(access, refresh);
      setUser(user);

      // Clear stored phone
      sessionStorage.removeItem('auth_phone');

      // Navigate to dashboard
      router.push('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 
                          error.response?.data?.non_field_errors?.[0] ||
                          'OTP kodu yanlışdır. Yenidən cəhd edin.';
      
      setFormError('otp', { message: errorMessage });
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setIsResending(true);
    clearError();

    try {
      await authAPI.sendOTP(phone);
      setCountdown(60);
    } catch (error: any) {
      setError('OTP yenidən göndərilə bilmədi. Yenidən cəhd edin.');
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-xl shadow-lg p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            Təsdiq Kodu
          </h1>
          <p className="text-gray-600">
            {phone} nömrəsinə göndərilən 6 rəqəmli kodu daxil edin
          </p>
        </div>

        {/* OTP Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4 text-center">
              Təsdiq Kodu
            </label>
            
            {/* OTP Input Grid */}
            <div className="flex justify-center space-x-3 mb-4">
              {[...Array(6)].map((_, index) => (
                <input
                  key={index}
                  id={`otp-${index}`}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  maxLength={1}
                  value={otpValue[index] || ''}
                  onChange={(e) => handleOTPChange(index, e.target.value)}
                  onKeyDown={(e) => handleKeyDown(index, e)}
                  className={`
                    w-12 h-12 text-center text-xl font-semibold border-2 rounded-lg
                    focus:ring-2 focus:ring-blue-500 focus:border-transparent
                    ${errors.otp ? 'border-red-500' : 'border-gray-300'}
                  `}
                  disabled={isLoading}
                />
              ))}
            </div>

            {errors.otp && (
              <p className="text-sm text-red-600 text-center">
                {errors.otp.message}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading || otpValue.length !== 6}
            className={`
              w-full py-3 px-4 rounded-lg font-medium text-white transition-colors
              ${(isLoading || otpValue.length !== 6)
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
                Təsdiqlənir...
              </span>
            ) : (
              'Təsdiqlə'
            )}
          </button>
        </form>

        {/* Resend OTP */}
        <div className="mt-6 text-center">
          {countdown > 0 ? (
            <p className="text-sm text-gray-500">
              Yenidən göndərmək üçün {countdown} saniyə gözləyin
            </p>
          ) : (
            <button
              onClick={handleResendOTP}
              disabled={isResending}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              {isResending ? 'Göndərilir...' : 'Kodu yenidən göndər'}
            </button>
          )}
        </div>

        {/* Back button */}
        <div className="mt-4 text-center">
          <button
            onClick={() => router.push('/auth/phone')}
            className="text-sm text-gray-500 hover:text-gray-700"
          >
            ← Telefon nömrəsini dəyişdir
          </button>
        </div>
      </div>
    </div>
  );
}