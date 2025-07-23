# apps/api/test_settings.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Python path-a əlavə et
sys.path.insert(0, str(BASE_DIR))

SECRET_KEY = 'test-key'
DEBUG = True

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'apps.accounts',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

AUTH_USER_MODEL = 'accounts.User'

print(f"✅ Test settings yükləndi")
print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"🐍 sys.path[0]: {sys.path[0]}")