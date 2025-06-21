# settings.py - Versión Final para Producción con Docker y PostgreSQL

import os
from pathlib import Path
import dj_database_url # Importa la librería para leer la URL de la BD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- Configuración de Seguridad (leída desde el archivo .env) ---
# Se reemplazan los valores locales por variables de entorno para seguridad.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG se leerá como '0' desde .env, por lo que será False.
DEBUG = os.environ.get('DEBUG', '0') == '1'

# Lee la IP de tu servidor y el host 'web' desde .env
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')


# --- Aplicaciones Instaladas ---
# Se mantienen las de tu archivo local.
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

# --- Middleware, URLs, Templates ---
# Se mantienen los de tu archivo local, no necesitan cambios.
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

WSGI_APPLICATION = 'laundry_app.wsgi.application'


# --- Base de Datos (CAMBIO MÁS IMPORTANTE) ---
# Se reemplaza la base de datos local SQLite por la configuración
# que lee la URL de la base de datos PostgreSQL desde el archivo .env.
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=False)
}


# --- Validadores de Contraseña ---
# Se mantienen los de tu archivo local.
AUTH_PASSWORD_VALIDATORS = [ #
    # ... (tus validadores aquí) ...
]

# --- Internacionalización ---
LANGUAGE_CODE = 'es-es' #
TIME_ZONE = 'America/Lima' # Ajustado para Perú
USE_I18N = True
USE_TZ = True


# --- Archivos Estáticos y de Medios (Rutas para Producción) ---
# Estas rutas son cruciales para que Nginx sirva los archivos correctamente.
STATIC_URL = 'static/'
# Se añade STATIC_ROOT para que el comando `collectstatic` funcione.
STATIC_ROOT = BASE_DIR / 'static_cdn'

MEDIA_URL = '/media/' #
# Se ajusta MEDIA_ROOT para que coincida con el volumen de Docker.
MEDIA_ROOT = BASE_DIR / 'media_cdn'


# --- Configuraciones Varias ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
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