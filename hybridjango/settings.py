"""
Django settings for hybridjango project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kxdw@f27f@c73b1064g%dtvm-=uke%2eqscww8k4k3@_ak&cit'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = [
    'vevsjef@hybrida.no',
]

# used in templates when an absolute url to a page is required
# (for example to tell facebokk what image to use when an event is shared)
SERVER_URL = 'https://hybrida.no'

SERVER_EMAIL = 'robot@hybrida.no'

# Application definition

AUTH_USER_MODEL = 'registration.Hybrid'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'widget_tweaks',
    'apps.kiltshop',
    'apps.bedkom',
    'apps.registration',
    'apps.quiz',
    'apps.events',
    'apps.jobannouncements',
    'apps.search',
    'apps.griffensorden',
    'apps.gitlab',
    'apps.staticpages',
    'apps.eventcalendar',
    'apps.rfid',
    'apps.evaluation',
    'apps.achievements',
    'tinymce',
    'apps.vevkom',
    'apps.merchandise',
    'hybridjango',
    'apps.update_k'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hybridjango.urls'

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

WSGI_APPLICATION = 'hybridjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        #        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #        'NAME': 'hybridjango',
        #        'USER': 'hybriduser',
        #        'PASSWORD': 'vevkom er 8',
        #        'HOST': 'localhost',
        #        'PORT': '',
        #    },
        #    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'nb-no'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = 'uploads/'
MEDIA_URL = '/uploads/'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Selfmade, used to list files, must be changed on deployment
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'robot@hybrida.no'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# If user has any local settings (local_settings.py), override the ones above
# Must be at the bottom of the file
# Used in production
try:
    from local_settings import *
except ImportError as e:
    print(e.msg)
    pass
