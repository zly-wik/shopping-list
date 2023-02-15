import os
from .common import *

DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['SQL_DATABASE'],
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASSWORD'],
        'HOST': os.environ['SQL_HOST'],
        'PORT': os.environ['SQL_PORT'],
    },
}