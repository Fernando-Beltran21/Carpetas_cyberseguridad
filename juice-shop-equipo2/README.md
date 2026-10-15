# OWASP Juice Shop

Aplicación INTENCIONALMENTE VULNERABLE para practicar. Úsala solo en tu equipo local.

## Iniciar
    docker compose up -d
Acceso: http://localhost:3000

## Detener y limpiar
    docker compose down

## Categorías OWASP que puedes practicar
- Pérdida de control de acceso: IDOR en carritos y paneles de otros usuarios
- Fallas criptográficas: hashes débiles y datos sensibles expuestos
- Inyección: SQLi en login y búsqueda, XSS
- Diseño inseguro: flujos de negocio abusables
- Configuración incorrecta: rutas expuestas como /ftp
- Fallas de autenticación: contraseñas débiles, recuperación insegura
- Marcador de retos: http://localhost:3000/#/score-board

## Seguridad
El puerto está enlazado a 127.0.0.1. No lo expongas a tu red ni a internet.
