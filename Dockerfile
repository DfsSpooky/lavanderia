# Usa una imagen base de Python oficial
FROM python:3.10-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requisitos y los instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# CREA EL ARCHIVO entrypoint.sh DIRECTAMENTE DENTRO DEL CONTENEDOR
# Esto evita cualquier problema de copia o saltos de línea desde el host
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'echo "Waiting for postgres..."' >> /app/entrypoint.sh && \
    echo 'while ! nc -z db 5432; do' >> /app/entrypoint.sh && \
    echo '  sleep 0.1' >> /app/entrypoint.sh && \
    echo 'done' >> /app/entrypoint.sh && \
    echo 'echo "PostgreSQL started"' >> /app/entrypoint.sh && \
    echo 'python manage.py migrate' >> /app/entrypoint.sh && \
    echo 'echo "Collecting static files..."' >> /app/entrypoint.sh && \
    echo 'python manage.py collectstatic --noinput' >> /app/entrypoint.sh && \
    echo 'gunicorn laundry_app.wsgi:application --bind 0.0.0.0:8000' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh # Asegura permisos de ejecución

# Opcional: Diagnóstico para verificar el archivo creado
RUN ls -l /app/entrypoint.sh
RUN cat /app/entrypoint.sh # Para ver el contenido dentro de la imagen

# Copia el resto del código de la aplicación
COPY . /app/

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Define el comando para iniciar Gunicorn (servidor de producción WSGI)
# Usaremos un script de entrada para esperar a la base de datos
ENTRYPOINT ["/app/entrypoint.sh"]