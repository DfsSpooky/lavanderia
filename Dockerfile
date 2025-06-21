# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema operativo
# 'postgresql-client' es necesario para que psycopg2 se compile correctamente
RUN apt-get update && apt-get install -y gcc postgresql-client

# Copia el archivo de requerimientos y los instala
# Usamos un paso separado para aprovechar el cache de Docker
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el resto del código de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto 8000 para que Gunicorn pueda servir la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
# Inicia Gunicorn como servidor WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "laundry_app.wsgi:application"]