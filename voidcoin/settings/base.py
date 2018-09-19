"""
Django settings for voidcoin project. https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import pygments.formatters
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages import constants as messages

from decouple import config, Csv

from chain.blockchain_client import Blockchain

BLOCKCHAIN = Blockchain()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
ROOT_URLCONF = 'voidcoin.urls'
SECRET_KEY = config('SECRET_KEY')

WSGI_APPLICATION = 'voidcoin.wsgi.application'
INTERNAL_IPS = ('127.0.0.1', 'localhost')

MESSAGE_LEVEL = 10  # DEBUG
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = 'voidcoin@outlook.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'voidcoin@outlook.com'

LOGIN_URL = reverse_lazy('personnel:login')
LOGOUT_URL = reverse_lazy('personnel:logout')
LOGOUT_REDIRECT_URL = reverse_lazy('personnel:login')

SITE_ID = 1
PASSWORD_RESET_TIMEOUT_DAYS = 1

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('siteuser:login')
LOGOUT_URL = reverse_lazy('siteuser:logout')

# SHELL_PLUS_PRINT_SQL = True
SHELL_PLUS_PYGMENTS_FORMATTER = pygments.formatters.TerminalFormatter
SHELL_PLUS_PYGMENTS_FORMATTER_KWARGS = {}
IPYTHON_KERNEL_DISPLAY_NAME = "Django Shell-Plus"
SHELL_PLUS_POST_IMPORTS = [
    ('fixtures', '*'),
    ('fixtures'),]

PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'chain',
    'siteuser',
]

THIRD_PARTY_APPS = [
    'django_extensions',
]

INSTALLED_APPS = PREREQ_APPS +  PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'siteuser.CustomUser'
