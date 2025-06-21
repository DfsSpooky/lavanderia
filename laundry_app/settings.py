# settings.py - Modificado para Producción con Docker y PostgreSQL

import os
from pathlib import Path
import dj_database_url # Importa la librería para leer la URL de la BD

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuración de Seguridad ---
# Lee la clave secreta desde el archivo .env
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# DEBUG debe ser False en un entorno de producción
DEBUG = os.environ.get('DEBUG', '0') == '1' # Lee el valor de DEBUG desde .env (0 por defecto)

# Lee los hosts permitidos desde el archivo .env
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_select2',
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

ROOT_URLCONF = 'laundry_app.urls'

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

WSGI_APPLICATION = 'laundry_app.wsgi.application'


# --- Base de Datos (CAMBIO IMPORTANTE) ---
# Ahora Django leerá la variable DATABASE_URL del archivo .env
# para conectarse al contenedor de PostgreSQL.
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima' # Ajustado a tu zona horaria
USE_I18N = True
USE_TZ = True


# --- Archivos Estáticos y de Medios ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn' # Directorio para collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_cdn' # Directorio para subidas de usuarios


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Redirecciones de Autenticación ---
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# --- Configuración para django-select2 ---
CACHES = {
    'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', },
    'select2': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'select2', }
}
SELECT2_CACHE_BACKEND = 'select2'