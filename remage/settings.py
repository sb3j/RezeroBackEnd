"""
Django settings for remage project.
 
Generated by 'django-admin startproject' using Django 5.0.7.
 
For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/
 
 
For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
 
from datetime import timedelta
from pathlib import Path
 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-e0p0^s=l^$^7$#5@tfbdpv__34#l4h#t^=^#+60ghkh-@0a)b9"
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
ALLOWED_HOSTS = []
 
 
 
import os
 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 
 
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React 개발 서버 주소
]
# Application definition
 
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    'rest_framework',
    'rest_framework_simplejwt',
    'faq',
    'analyze',
    'django_filters',
    'order',
    'corsheaders',
    'drf_yasg',
]
 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'order.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
 
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]
 
ROOT_URLCONF = "remage.urls"
 
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
 
 
AUTH_USER_MODEL = 'users.CustomUser'
WSGI_APPLICATION = "remage.wsgi.application"
 
 
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rezero',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': 'localhost',   
        'PORT': '3307',
    }
}

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(seconds=5),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
} 
 
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
 
AUTH_PASSWORD_VALIDATORS = [
]
 
 
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
 
LANGUAGE_CODE = "en-us"
 
TIME_ZONE = "UTC"
 
USE_I18N = True
 
USE_TZ = True
 
 
 
STATIC_URL = "static/"
 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
 
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'analyze': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
# settings.py
 
# 세션 설정
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 세션을 데이터베이스에 저장
SESSION_COOKIE_NAME = 'sessionid'  # 기본 세션 쿠키 이름
SESSION_COOKIE_SECURE = False  # True로 설정하면 HTTPS에서만 세션 쿠키 전송
SESSION_COOKIE_HTTPONLY = True  # 클라이언트 측에서 세션 쿠키를 접근할 수 없도록 설정
SESSION_SAVE_EVERY_REQUEST = True  # 모든 요청에 대해 세션을 저장
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 브라우저가 닫힐 때 세션 만료
 
from decouple import config
OPENAI_API_KEY = config('OPENAI_API_KEY')

 
CORS_ORIGIN_WHITELIST = [

    'http://localhost:3000',  # React 개발 서버

]
 
 
CORS_EXPOSE_HEADERS = ['Authorization', 'Refresh-Token']

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'refresh-token',
]