# Django settings
"""
Django settings for backend project.
"""

import os
from pathlib import Path
from datetime import timedelta

# load environment variables optionally (you can use python-dotenv)
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "django-insecure-dummy-secret-key")

DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party
    "rest_framework",
    "corsheaders",
    # Local
    "accounts",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # cors
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ],},
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database — PostgreSQL (dummy credentials — replace)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'otp_demo_db',
        'USER': 'postgres',
        'PASSWORD': 'root',  # Replace with your real password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation (not used for custom user model's make_password but keep defaults)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"

# Django REST Framework default
REST_FRAMEWORK = {}

# CORS settings - allow frontend origin
CORS_ALLOW_ALL_ORIGINS = True  # for dev. In production, set specific origins.

# Email settings - placeholder Gmail SMTP (replace for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'janamahi2010@gmail.com'
EMAIL_HOST_PASSWORD = 'vcwrnajhtthyjigf'  # not your Gmail password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# For local debugging you can set:
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# OTP expiry minutes
OTP_EXPIRY_MINUTES = int(os.getenv("OTP_EXPIRY_MINUTES", 5))
