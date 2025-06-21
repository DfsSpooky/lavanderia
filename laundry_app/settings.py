# laundry_app/settings.py

import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configuración de Seguridad ---
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DEBUG', '0') == '1'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# --- Aplicaciones ---
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

# --- Middleware ---
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

# --- Templates ---
TEMPLATES = [
    # ... (tu configuración de templates aquí, no necesita cambios)
]

WSGI_APPLICATION = 'laundry_app.wsgi.application'

# --- Base de Datos ---
# Lee la configuración de la BD desde la variable DATABASE_URL en el archivo .env
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600)
}

# --- Validadores de Contraseña ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (tus validadores aquí, no necesita cambios)
]

# --- Internacionalización ---
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# --- Archivos Estáticos y de Medios ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn'  # Directorio para collectstatic

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_cdn'    # Directorio para subidas de usuarios

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# --- Configuración de Cache (para django-select2) ---
CACHES = {
    # ... (tu configuración de cache aquí, no necesita cambios)
}
SELECT2_CACHE_BACKEND = 'select2'