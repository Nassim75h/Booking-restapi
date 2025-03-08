
from .common import *
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()


ALLOWED_HOSTS = ["*"]
DEBUG = True

STRIPE_KEY=os.getenv("STRIPE_KEY")

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLISHER_KEY')

SECRET_KEY = "django-insecure-lxhoqp8y=l(4u6iakgix*edo!s(6fe1@kk^j&g!%$6%)^_@$$w"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKEN':True,
    'BLACKLIST_AFTER_ROTATION':True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME":  'db',
        "HOST": 'localhost',
        'USER': 'root',
        'PASSWORD': ''
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DOMAIN = "localhost:8000"
SITE_NAME = "FastBook"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'noreply@fastbook.io'

AUTH_USER_MODEL='authapp.User'
CORS_ALLOWED_ORIGINS=[
    'http://127.0.0.1:5500',
    "http://localhost:8080",
    "http://192.168.100.58:8080",
]

CELERY_BROKER_URL = 'redis://localhost:6379/1'
