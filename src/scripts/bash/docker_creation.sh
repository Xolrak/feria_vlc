#!/bin/bash

# Cambia al directorio 'docker' (dos niveles arriba y luego 'docker')
cd ../../docker

# Verifica si existe el archivo .env en el directorio 'docker'
if [ ! -f .env ]; then
    echo "Error: No se encuentra el archivo .env en la carpeta 'docker'."
    echo "Crea el archivo .env antes de continuar."
    exit 1
fi

# Crea la red de Docker (ignora el error si ya existe)
docker network create bbdd-network || true

# Levanta los servicios definidos en el docker-compose
docker compose up -d
