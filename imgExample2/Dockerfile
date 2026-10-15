# Dockerfile — Ejecuta cia_api.py (CIA Triad Demo API) con FastAPI + Uvicorn

FROM ubuntu:22.04

LABEL maintainer="Curso de Ciberseguridad"
LABEL description="Contenedor que corre la CIA Triad Demo API (FastAPI)"

ENV DEBIAN_FRONTEND=noninteractive

# Herramientas base + Python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python-is-python3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Usuario sin privilegios de root
RUN useradd -ms /bin/bash labuser
USER labuser
WORKDIR /home/labuser

# Ejecutables de "pip install --user" visibles en el PATH
ENV PATH="/home/labuser/.local/bin:${PATH}"

# Instala primero solo las dependencias (aprovecha la caché de Docker
# si luego solo cambias cia_api.py, no hace falta reinstalar todo)
COPY --chown=labuser:labuser requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copia la aplicación
COPY --chown=labuser:labuser cia_api.py .

EXPOSE 8000

# Arranca el servidor automáticamente al correr el contenedor
CMD ["uvicorn", "cia_api:app", "--host", "0.0.0.0", "--port", "8000"]
