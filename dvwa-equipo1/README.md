# DVWA (Damn Vulnerable Web Application)

Aplicación INTENCIONALMENTE VULNERABLE para practicar. Úsala solo en tu equipo local.

## Iniciar
    docker compose up -d
Acceso: http://localhost:8080
Usuario: admin  |  Contraseña: password

Primera vez: entra a "Setup / Reset DB" y pulsa "Create / Reset Database".
Luego puedes cambiar el nivel de dificultad en "DVWA Security" (low, medium, high, impossible).

## Detener y limpiar
    docker compose down

## Categorías OWASP que puedes practicar
- Inyección: SQL Injection, SQLi ciega, Command Injection
- Fallas de autenticación: fuerza bruta, sesiones débiles
- Diseño inseguro: CSRF, subida de archivos sin validación
- Configuración incorrecta: inclusión de archivos (File Inclusion)

## Seguridad
El puerto está enlazado a 127.0.0.1. No lo expongas a tu red ni a internet.
