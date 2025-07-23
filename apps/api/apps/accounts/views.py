# apps/api/apps/accounts/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    RegisterSerializer, 
    SendOTPSerializer, 
    VerifyOTPSerializer,
    UserSerializer
)


@extend_schema(
    request=RegisterSerializer,
    responses={201: UserSerializer},
    description="Yeni istifadəçi qeydiyyatı"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Register new user and send OTP"""
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # TODO: Send SMS OTP here
        # sms_service.send_otp(user.phone, user.otp_code)
        
        return Response({
            'message': 'Qeydiyyat uğurlu oldu! OTP kodu göndərildi.',
            'phone': str(user.phone),
            'otp_code': user.otp_code if settings.DEBUG else None  # Only in DEBUG mode
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=SendOTPSerializer,
    responses={200: dict},
    description="OTP kodunu yenidən göndər"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp_view(request):
    """Resend OTP to existing user"""
    serializer = SendOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        phone = serializer.validated_data['phone']
        user = User.objects.get(phone=phone)
        
        # Check if can send new OTP
        if user.otp_created_at:
            time_passed = timezone.now() - user.otp_created_at
            if time_passed.seconds < 60:  # 1 minute cooldown
                return Response({
                    'error': f'Yeni kod {60 - time_passed.seconds} saniyə sonra göndərilə bilər'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        user.generate_otp()
        
        # TODO: Send SMS OTP here
        # sms_service.send_otp(user.phone, user.otp_code)
        
        return Response({
            'message': 'OTP kodu göndərildi',
            'otp_code': user.otp_code if settings.DEBUG else None  # Only in DEBUG mode
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=VerifyOTPSerializer,
    responses={200: dict},
    description="OTP kodu ilə giriş"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_view(request):
    """Verify OTP and login user"""
    serializer = VerifyOTPSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Update last login
        user.last_login = timezone.now()
        user.save()
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={200: UserSerializer},
    description="Cari istifadəçi məlumatları"
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Get current user profile"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    request=UserSerializer,
    responses={200: UserSerializer},
    description="Profil məlumatlarını yenilə"
)
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Update user profile"""
    serializer = UserSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Import settings for DEBUG check
from django.conf import settings
from django.utils import timezone