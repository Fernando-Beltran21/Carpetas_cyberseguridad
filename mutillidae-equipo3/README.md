# OWASP Mutillidae II

Aplicación INTENCIONALMENTE VULNERABLE para practicar. Úsala solo en tu equipo local.

## Iniciar
    docker compose up -d
Acceso: http://localhost:8082
Primera vez: si aparece un error de base de datos, abre
http://localhost:8082/set-up-database.php

## Detener y limpiar
    docker compose down

## Categorías OWASP que puedes practicar
- Configuración incorrecta: exposición de información, cabeceras débiles
- Pérdida de control de acceso: manipulación de parámetros y rutas
- Fallas criptográficas: datos transmitidos sin cifrar
- Inyección: SQLi, XSS, command injection
- SSRF: páginas dedicadas
- Tiene modo "hints" para ir de menos a más ayuda

## Seguridad
El puerto está enlazado a 127.0.0.1. No lo expongas a tu red ni a internet.
Nota: la imagen es antigua; si falla, revisa la versión oficial en
https://github.com/webpwnized/mutillidae-docker
