# apps/api/apps/accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta
import random
import string


class UserManager(BaseUserManager):
    """Custom user manager for phone-based authentication"""
    
    def create_user(self, phone, **extra_fields):
        if not phone:
            raise ValueError('Telefon nömrəsi mütləqdir')
        
        user = self.model(phone=phone, **extra_fields)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_phone_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(phone, **extra_fields)


class User(AbstractUser):
    """Custom User model with phone authentication"""
    
    GENDER_CHOICES = [
        ('M', 'Kişi'),
        ('F', 'Qadın'),
    ]
    
    username = None  # Username istifadə etmirik
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(unique=True, region='AZ')
    
    # User info
    first_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    
    # OTP fields
    is_phone_verified = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'gender', 'birth_date']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'users'
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['created_at']),
        ]
    
    def generate_otp(self):
        """Generate 6-digit OTP code"""
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.otp_attempts = 0
        self.save()
        return self.otp_code
    
    def verify_otp(self, code):
        """Verify OTP code"""
        if not self.otp_code or not self.otp_created_at:
            return False
        
        # Check expiry (5 minutes)
        if timezone.now() - self.otp_created_at > timedelta(minutes=5):
            return False
        
        # Check attempts
        if self.otp_attempts >= 3:
            return False
        
        if self.otp_code == code:
            self.is_phone_verified = True
            self.otp_code = None
            self.otp_created_at = None
            self.otp_attempts = 0
            self.save()
            return True
        
        # Increment attempts
        self.otp_attempts += 1
        self.save()
        return False
    
    @property
    def age(self):
        """Calculate age from birth date"""
        today = timezone.now().date()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def __str__(self):
        return f"{self.first_name} - {self.phone}"