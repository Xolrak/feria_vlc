#!/bin/bash

# Cambia el directorio actual al subdirectorio 'docker' donde está el docker-compose
cd ../docker
# Crea una red de Docker
docker network create bbdd-network
# Levanta los servicios definidos en el docker-compose
docker-compose up -d