"""
Django settings for coew project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from dotenv import dotenv_values
from pathlib import Path

from core.dj_extensions import cors_headers, rest_framework, simple_jwt

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# locate .env.base file
BASE_ENV_PATH = BASE_DIR / '.env/base/.env'

# load the environment variables in .env/base/.env
base_env_config = dotenv_values(dotenv_path=BASE_ENV_PATH)

# if ENVIRONMENT is set to 'prod' in the .env.base file load the
# production environment variable ('.env/prod/.env') else
# load the development environment variables ('.env/dev/.env')

if base_env_config['ENVIRONMENT'] == 'prod':
    ENV_FILE_PATH = BASE_DIR / '.env/prod/.env'
else:
    ENV_FILE_PATH = BASE_DIR / '.env/dev/.env'

# load environment variables for the specified
# environment (either `.env/prod/.env` or `.env/dev/.env`)
env_config = dotenv_values(dotenv_path=ENV_FILE_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env_config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_config['DEBUG']

ALLOWED_HOSTS = env_config['ALLOWED_HOSTS'].split(',')
ALLOWED_ORIGINS = env_config['ALLOWED_ORIGINS']

API_PREFIX = env_config['API_PREFIX']
API_VERSIONS = env_config['API_VERSIONS']
APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'apis.base',
    'apis.scan_reports',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.routers.urls'

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

WSGI_APPLICATION = 'core.sgi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API Extensions Settings

# CORS Settings
cors_headers.CORS_CONFIG(ALLOWED_ORIGINS).settings()

# REST Framework Settings
REST_FRAMEWORK = rest_framework.REST_FRAMEWORK_CONFIG.settings()

# Simple JWT Settings
SIMPLE_JWT = simple_jwt.SIMPLE_JWT_CONFIG(SECRET_KEY).settings()
