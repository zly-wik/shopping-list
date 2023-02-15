from .common import *
import os

DEBUG = True
SECRET_KEY = 'django-insecure-j!c@3#kk3^b#4j@lp7%q3ui9iw)364psywiahs65l*bmq=h%5j'

# Debug_toolbar with Docker
import socket 
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shoppinglist_db',
        'USER': 'dlugi',
        'PASSWORD': 'test_pass_123',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}

if os.environ.get('GITHUB_WORKFLOW') or not os.environ.get('PYTHONUNBUFFERED'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }