# laundry_app/settings.py - Versión Final para Producción

import os
from pathlib import Path
import dj_database_url # Importa la librería para leer la URL de la BD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Configuración de Seguridad (leída desde el archivo .env) ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG se leerá como '0' desde .env, por lo que será False.
DEBUG = os.environ.get('DEBUG', '0') == '1'

# Lee la IP de tu servidor desde .env
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition
# Tus apps originales, no necesitan cambios.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_select2',  # Añadido para Select2
]

MIDDLEWARE = [ #
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'laundry_app.urls' #

TEMPLATES = [ #
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #
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

WSGI_APPLICATION = 'laundry_app.wsgi.application' #


# --- Base de Datos (CAMBIO MÁS IMPORTANTE) ---
# En lugar de usar SQLite, ahora lee la variable DATABASE_URL del archivo .env
# para conectarse al contenedor de PostgreSQL.
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=False)
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [ #
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
LANGUAGE_CODE = 'es-es' #
TIME_ZONE = 'America/Lima' # Ajustado para Perú
USE_I18N = True
USE_TZ = True


# --- Archivos Estáticos y de Medios (Rutas para Producción) ---
# Nginx servirá los archivos desde estas carpetas dentro del contenedor.
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_cdn'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' #

# Redirecciones de Login/Logout
LOGIN_REDIRECT_URL = 'dashboard' #
LOGOUT_REDIRECT_URL = 'home' #


# Configuración para django-select2
CACHES = { #
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'select2',
    }
}
SELECT2_CACHE_BACKEND = 'select2' #