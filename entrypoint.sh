#!/bin/sh

# Espera a que la base de datos esté disponible
# Reemplaza 'db' con el nombre del servicio de tu base de datos en docker-compose.yml
# Reemplaza '5432' con el puerto de tu base de datos
echo "Waiting for postgres..."

while ! nc -z db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# Ejecuta migraciones de la base de datos
python manage.py migrate

# Inicia el servidor Gunicorn
# Ajusta el número de workers según los núcleos de tu CPU (2*CPU + 1 es una buena regla general)
gunicorn laundry_app.wsgi:application --bind 0.0.0.0:8000