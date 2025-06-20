import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# IMPORTANTE: Manten esta clave SECRETA y usa una variable de entorno en producción
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your_default_secret_key_for_dev_if_not_set')

# En producción, DEBUG DEBE SER FALSE
DEBUG = False

# DOMINIOS E IPs permitidos en producción
# Se obtiene de la variable de entorno DJANGO_ALLOWED_HOSTS
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Tus aplicaciones
    'core',
    # Aplicaciones de terceros
    'django_select2', # Para los widgets mejorados
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Si tienes una carpeta 'templates' global
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


# Database
# Configuración de la base de datos PostgreSQL usando dj_database_url
# Obtiene la URL de la base de datos de la variable de entorno DATABASE_URL
# O construye una a partir de otras variables de entorno de POSTGRES
DATABASE_URL = os.environ.get('DATABASE_URL',
                              f"postgres://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@localhost:5432/{os.environ.get('POSTGRES_DB')}")

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600 # Opcional: tiempo de vida de la conexión
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-es' # Cambiado a español de España

TIME_ZONE = 'America/Lima' # Ajustado a tu zona horaria local

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static_cdn' # Ruta donde Nginx servirá los archivos estáticos

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_cdn' # Ruta donde Nginx servirá los archivos de medios (subidas de usuario)


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de redireccionamiento de autenticación
LOGIN_REDIRECT_URL = 'dashboard' # Redirige al dashboard después de iniciar sesión
LOGOUT_REDIRECT_URL = 'home' # Redirige a la página de inicio después de cerrar sesión

# Configuración para django-select2
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'select2': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'select2',
    }
}
SELECT2_CACHE_BACKEND = 'select2'

# Opcional: Configuración para SSL (HTTPS) - Descomentar cuando configures Certbot con Nginx
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True