# Dockerfile — Imagen Ubuntu de laboratorio (Curso de Ciberseguridad)
# Construye un contenedor Ubuntu con herramientas básicas de red y diagnóstico.

FROM ubuntu:22.04

LABEL maintainer="Curso de Ciberseguridad"
LABEL description="Imagen Ubuntu con herramientas basicas de red para practicas de laboratorio"

# Evita que apt pida confirmaciones interactivas durante el build
ENV DEBIAN_FRONTEND=noninteractive

# Actualiza el sistema e instala herramientas básicas
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    python3 \
    python3-pip \
    python-is-python3 \
    curl \
    wget \
    vim \
    nano \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Crea un usuario sin privilegios de root para trabajar dentro del contenedor
RUN useradd -ms /bin/bash labuser && \
    echo "labuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


# A partir de aquí, todo corre como labuser (no como root)
USER labuser
WORKDIR /home/labuser

