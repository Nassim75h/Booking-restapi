from .common import *
import os 

SECRET_KEY=os.getenv("SECRET_KEY")
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKEN':True,
    'BLACKLIST_AFTER_ROTATION':True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

}

DATABASES={
    'default':{
        'ENGINE':'django.db.backends.postgresql',
        'NAME':os.getenv('DB_NAME'),
        'USER':os.getenv('DB_USER'),
        'PASSWORD':os.getenv('DB_PASSWORD'),
        'HOST':os.getenv('DB_HOST'),
        'PORT':os.getenv('DB_PORT'),
        
    }

}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['.herokuapp.com']




CORS_ALLOWED_ORIGINS=[
    'http://127.0.0.1:5500',
    "http://localhost:8080",
    "http://192.168.100.58:8080",
]
