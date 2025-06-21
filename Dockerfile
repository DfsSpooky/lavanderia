# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# --- ¡CAMBIO IMPORTANTE AQUÍ! ---
# Instala las dependencias del sistema operativo ANTES de instalar las de Python.
# gcc y libpq-dev son necesarios para compilar psycopg2 y otras librerías.
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos y los instala.
# Ahora este paso debería funcionar sin problemas.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto donde correrá Gunicorn
EXPOSE 8000