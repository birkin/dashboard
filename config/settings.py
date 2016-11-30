# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Django settings for dashboard_project.

Environmental variables set in project's env/bin/activate, when using runserver,
  or env/bin/activate_this.py, when using apache via mod_wsgi or passenger.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import json, os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = unicode( os.path.dirname(os.path.dirname(__file__)) )

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = unicode( os.environ['DSHBRD__SECRET_KEY'] )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads( os.environ['DSHBRD__DEBUG_JSON'] )  # will be True or False

ALLOWED_HOSTS = json.loads( os.environ['DSHBRD__ALLOWED_HOSTS'] )  # list


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard_app',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = json.loads( os.environ['DSHBRD__TEMPLATES_JSON'] )  # list of dict(s)

WSGI_APPLICATION = 'config.passenger_wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = json.loads( os.environ['DSHBRD__DATABASES_JSON'] )


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = unicode( os.environ['DSHBRD__STATIC_URL'] )
STATIC_ROOT = unicode( os.environ['DSHBRD__STATIC_ROOT'] )  # needed for collectstatic command


# Email
EMAIL_HOST = unicode( os.environ['DSHBRD__EMAIL_HOST'] )
EMAIL_PORT = int( os.environ['DSHBRD__EMAIL_PORT'] )


# sessions

# <https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-SESSION_SAVE_EVERY_REQUEST>
# Thinking: not that many concurrent users, and no pages where session info isn't required, so overhead is reasonable.
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',  # note: configure server to use system's log-rotate to avoid permissions issues
            'filename': unicode( os.environ.get(u'DSHBRD__LOG_PATH') ),
            'formatter': 'standard',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'dashboard_app': {
            'handlers': ['logfile'],
            'level': unicode( os.environ.get(u'DSHBRD__LOG_LEVEL') ),
            'propogate': False
        },
    }
}


## app-level settings ##

EMAIL_GENERAL_HELP = unicode( os.environ['DSHBRD__EMAIL_GENERAL_HELP'] )


## EOF ##
