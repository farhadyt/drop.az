# apps/api/apps/accounts/serializers.py
from rest_framework import serializers
from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    phone = PhoneNumberField(region='AZ')
    
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'gender', 'birth_date')
        
    def validate_birth_date(self, value):
        """Validate birth date - user must be at least 16 years old"""
        today = timezone.now().date()
        age = today.year - value.year - (
            (today.month, today.day) < (value.month, value.day)
        )
        
        if age < 16:
            raise serializers.ValidationError("Yaşınız minimum 16 olmalıdır")
        
        if age > 100:
            raise serializers.ValidationError("Doğum tarixi düzgün deyil")
        
        return value
    
    def create(self, validated_data):
        """Create user and generate OTP"""
        user = User.objects.create_user(**validated_data)
        user.generate_otp()
        return user


class SendOTPSerializer(serializers.Serializer):
    """Send OTP serializer"""
    phone = PhoneNumberField(region='AZ')
    
    def validate_phone(self, value):
        """Check if phone exists"""
        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Bu nömrə qeydiyyatdan keçməyib")
        return value


class VerifyOTPSerializer(serializers.Serializer):
    """Verify OTP serializer"""
    phone = PhoneNumberField(region='AZ')
    otp_code = serializers.CharField(max_length=6, min_length=6)
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        otp_code = attrs.get('otp_code')
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("İstifadəçi tapılmadı")
        
        if not user.verify_otp(otp_code):
            raise serializers.ValidationError("OTP kodu yanlışdır və ya müddəti bitib")
        
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """User detail serializer"""
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = (
            'id', 'phone', 'first_name', 'last_name', 
            'email', 'gender', 'birth_date', 'age',
            'is_phone_verified', 'created_at'
        )
        read_only_fields = ('phone', 'is_phone_verified', 'created_at')