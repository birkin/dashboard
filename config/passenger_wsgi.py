"""
WSGI config.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os, pprint, sys

import shellvars
from django.core.wsgi import get_wsgi_application


PROJECT_DIR_PATH = os.path.dirname( os.path.dirname(os.path.abspath(__file__)) )
ENV_SETTINGS_FILE = os.environ['DSHBRD__ENV_SETTINGS_PATH']  # set in `conf.d/passenger.conf`, and `env/bin/activate`

## update path
sys.path.append( PROJECT_DIR_PATH )

## reference django settings
os.environ[u'DJANGO_SETTINGS_MODULE'] = 'config.settings'  # so django can access its settings

## load up env vars
var_dct = shellvars.get_vars( ENV_SETTINGS_FILE )
for ( key, val ) in var_dct.items():
    os.environ[key.decode('utf-8')] = val.decode('utf-8')

## gogogo
application = get_wsgi_application()
