// src/lib/validations.ts
import { z } from 'zod';
import { parsePhoneNumber, isValidPhoneNumber } from 'libphonenumber-js';

// Phone number validation for Azerbaijan
export const phoneSchema = z
  .string()
  .min(1, 'Telefon nömrəsi mütləqdir')
  .refine((phone) => {
    try {
      // Try to parse as Azerbaijan number
      const phoneNumber = parsePhoneNumber(phone, 'AZ');
      return phoneNumber && phoneNumber.isValid();
    } catch {
      // Fallback validation
      return isValidPhoneNumber(phone, 'AZ');
    }
  }, 'Düzgün Azərbaycan telefon nömrəsi daxil edin (+994xxxxxxxxx)');

// OTP validation
export const otpSchema = z
  .string()
  .length(6, 'OTP kodu 6 rəqəm olmalıdır')
  .regex(/^\d+$/, 'OTP kodu yalnız rəqəmlərdən ibarət olmalıdır');

// Profile validation
export const profileSchema = z.object({
  first_name: z
    .string()
    .min(2, 'Ad minimum 2 hərf olmalıdır')
    .max(50, 'Ad maksimum 50 hərf ola bilər'),
  
  gender: z.enum(['M', 'F'], 'Cins seçilməlidir'),
  
  birth_date: z
    .string()
    .optional()
    .refine((date) => {
      if (!date) return true; // Optional field
      
      const birthDate = new Date(date);
      const today = new Date();
      const age = today.getFullYear() - birthDate.getFullYear();
      
      return age >= 16 && age <= 100;
    }, 'Yaş 16-100 arasında olmalıdır'),
});

// Combined schemas for forms
export const phoneFormSchema = z.object({
  phone: phoneSchema,
});

export const otpFormSchema = z.object({
  otp: otpSchema,
});

export const registerFormSchema = z.object({
  phone: phoneSchema,
  first_name: profileSchema.shape.first_name,
  gender: profileSchema.shape.gender,
  birth_date: profileSchema.shape.birth_date,
});

// Type inference
export type PhoneFormData = z.infer<typeof phoneFormSchema>;
export type OTPFormData = z.infer<typeof otpFormSchema>;
export type ProfileFormData = z.infer<typeof profileSchema>;
export type RegisterFormData = z.infer<typeof registerFormSchema>;