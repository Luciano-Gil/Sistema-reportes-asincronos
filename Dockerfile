# Imagen base : Python 3.11  version slim (ligera, ahorra espacio )
FROM python:3.11-slim

# Variables de entorno: configuracion Python para el contenedor 
# evita que Python genere archivos de cache (.pyc) que ensucian el proyecto
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que los mensajes de error (logs) se muestren en tiempo real en la terminal 
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo: define  donde vivira el codigo dentro del contenedor 
WORKDIR /app

#Dependencias del sistema : prepara el sistema operativo Linux interno
# apt-get update &&:actualiza el índice de paquetes para conocer las últimas versiones disponibles
#  apt-get install -y :instala los paquetes siguientes confirmando "Sí" (-y) a todo automáticamente
# libpq-dev: librería fundamental para que Python pueda comunicarse con PostgreSQL
#gcc:Compilador de C necesario para instalar librerías de Python que requieren compilación
# && rm -rf /var/lib/apt/lists/*: Limpia los archivos temporales de la instalación para que el contenedor sea más liviano
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*
        
# Intalacion de librerias: se coopia los requerimientos y se instalan 
# se copia  primero el archivo para aprovechar la memoria cache de Docker
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia del codigo: se pasa todo el  proyecto local al contenedor 
# incluye la carpeta CODIGO_PYTHON y todos sus archivos
COPY . /app/