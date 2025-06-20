#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Ejecuta migraciones de la base de datos
python manage.py migrate

# Recolecta archivos estáticos (importante para producción)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Inicia el servidor Gunicorn
gunicorn laundry_app.wsgi:application --bind 0.0.0.0:8000