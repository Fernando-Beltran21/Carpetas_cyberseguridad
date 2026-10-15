# OWASP WebGoat

Aplicación INTENCIONALMENTE VULNERABLE con lecciones guiadas. Úsala solo en tu equipo local.

## Iniciar
    docker compose up -d
Acceso: http://localhost:8081/WebGoat
Regístrate con un usuario nuevo la primera vez (es local).
Puerto 9090: WebWolf, herramienta complementaria para algunas lecciones.

## Detener y limpiar
    docker compose down

## Categorías OWASP que puedes practicar
- SSRF: lección específica
- Componentes vulnerables y desactualizados: librerías con CVEs
- Integridad de software y datos: deserialización insegura
- Fallas de registro y monitoreo: lecciones de logging
- Inyección, autenticación y control de acceso: varias lecciones

## Seguridad
Los puertos están enlazados a 127.0.0.1. No los expongas a tu red ni a internet.
