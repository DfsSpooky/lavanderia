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

# Copia el resto del código de la aplicación
COPY . /app/

# ASEGÚRATE DE QUE entrypoint.sh TIENE PERMISOS DE EJECUCIÓN
RUN chmod +x /app/entrypoint.sh # <--- ¡Añade esta línea!

# Expone el puerto que usará Gunicorn
EXPOSE 8000

# Define el comando para iniciar Gunicorn (servidor de producción WSGI)
# Usaremos un script de entrada para esperar a la base de datos
ENTRYPOINT ["/app/entrypoint.sh"]