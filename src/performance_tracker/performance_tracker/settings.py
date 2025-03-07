"""
Django settings for performance_tracker project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Use database-backed sessions
SESSION_COOKIE_NAME = 'sessionid'  # Default Django session cookie name
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Sessions persist after browser close

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uxb9&z&)2zfo)v4w&p(x15+k=7z45gtt-00p+z7=!*9qyfx7$o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # third party
    'rest_framework', 
    "rest_framework.authtoken",
    'corsheaders',
    
    # own apps
    'users', 
    'pages',
    'students',
    'teachers', 
    'analytics', 
]

REST_AUTH = {
    "TOKEN_MODEL": None,  
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Ensure CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",  # Allow requests from frontend
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'performance_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'performance_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.User'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

REST_USE_JWT = False  # Ensure JWT is disabled if not configured
ACCOUNT_EMAIL_VERIFICATION = "none"  # Disable email verification
ACCOUNT_AUTHENTICATION_METHOD = "username"  # Use username for login
ACCOUNT_EMAIL_REQUIRED = False  # No email required

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer'
}


REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "dj_rest_auth.registration.serializers.RegisterSerializer"
}

REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "dj_rest_auth.serializers.LoginSerializer",
    "TOKEN_SERIALIZER": "dj_rest_auth.serializers.TokenSerializer",
    "PASSWORD_RESET_SERIALIZER": "dj_rest_auth.serializers.PasswordResetSerializer",
    "PASSWORD_RESET_CONFIRM_SERIALIZER": "dj_rest_auth.serializers.PasswordResetConfirmSerializer",
}

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False

LOGIN_REDIRECT_URL = "/pages/teacherdash/"  # Redirect after login
LOGOUT_REDIRECT_URL = "/pages/login/"  # Redirect after logout
LOGIN_URL = "/users/login/"  # Redirect unauthenticated users

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
