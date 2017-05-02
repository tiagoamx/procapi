# -*- coding: utf-8 -*-


"""
Django settings for procapi project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import os
import raven

from mongoengine import connect
from prettyconf import config

# Build paths inside the project like this: os.path.join(ROOT_DIR, ...)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APPS_DIR = os.path.join(ROOT_DIR, 'procapi')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=config.boolean)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=config.list)


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_celery_beat',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework_mongoengine',
]

LOCAL_APPS = [
    'procapi.processo.apps.ProcessoConfig',
    'procapi.taskapp.apps.TaskAppConfig'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APPS_DIR, 'templates')
        ],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

# mongodb config
MONGO_DBNAME = config('MONGO_DBNAME')
MONGO_HOSTNAME = config('MONGO_HOSTNAME')
MONGO_PORT = config('MONGO_PORT')
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')

MONGODB_DATABASE_HOST = 'mongodb://{}:{}@{}:{}/{}'.format(
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_HOSTNAME,
    MONGO_PORT,
    MONGO_DBNAME
)

mongo_conn = connect(db=MONGO_DBNAME, host=MONGO_HOSTNAME)

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Araguaina'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(ROOT_DIR, 'static_producao')

#STATICFILES_DIRS = (
#    os.path.join(APPS_DIR, 'static'),
#)

# Media files

MEDIA_ROOT = os.path.join(ROOT_DIR, 'media_producao')

MEDIA_URL = '/media/'

# Raven Config

RAVEN_DSN = config('RAVEN_DSN')
RAVEN_CONFIG = {
    'dsn': RAVEN_DSN,
    'release': raven.fetch_git_sha(ROOT_DIR),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'eproc': {
            'level': 'INFO',
            'handlers': ['sentry'],
            'propagate': False,
        },

    },
}

# E-Proc WSDL Config

EPROC_DEFAULT_USER = config('EPROC_DEFAULT_USER')
EPROC_DEFAULT_PASS = config('EPROC_DEFAULT_PASS')

EPROC_WSDL_PROCESSOS = config('EPROC_WSDL_PROCESSOS')
EPROC_WSDL_SERVICOS = config('EPROC_WSDL_SERVICOS')
EPROC_WSDL_TABELAS = config('EPROC_WSDL_TABELAS')

# DjangoRestFramework Config

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Celery Config

CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
