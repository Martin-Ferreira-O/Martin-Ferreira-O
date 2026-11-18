[← Volver al perfil](../README.md) · [English version](./psycode.en.md)

# Psycode

**Proyecto universitario en equipo · Repositorio privado**

Psycode integra una interfaz web, un servidor central y un agente instalable
para apoyar la supervisión de sesiones de psicología. Combina gestión de
sesiones, captura de audio, procesamiento y consulta de alertas con trazabilidad.

## Mi participación

He contribuido al backend Django, a la interfaz React y a la separación entre
el agente de captura y el servidor central. También he trabajado en comprobaciones
automáticas de los límites entre esos componentes, además de funcionalidades de
usuarios, alertas y evaluaciones.

## Decisiones de arquitectura

- **Monolito modular:** el servidor organiza sus responsabilidades por módulos y
  capas. Las vistas HTTP delegan en servicios de aplicación; los adaptadores de
  infraestructura resuelven persistencia y comunicación externa.
- **Agente independiente:** el programa de captura tiene su propio ciclo de
  instalación y operación. Se comunica con el servidor mediante contratos HTTP
  y WebSocket, sin importarse como parte del backend.
- **Trabajo en segundo plano:** la recepción de audio y su procesamiento tienen
  responsabilidades separadas. El estado persistente de los trabajos permite
  gestionar reintentos y recuperación.
- **Persistencia según responsabilidad:** SQL para cuentas, sesiones y estado
  operativo; MongoDB para alertas y bitácora.

## Calidad y colaboración

El proyecto incluye autenticación, control de permisos, trazabilidad técnica y
pruebas de integración. Las comprobaciones de límites y contratos ayudan a
detectar dependencias indebidas entre el agente y el servidor. Las pruebas de
integración pueden ejecutarse con datos sintéticos y sin credenciales reales.

Este trabajo me ha permitido practicar cómo dividir responsabilidades,
mantener contratos entre componentes y colaborar sobre una base de código que
evoluciona en equipo.

**Tecnologías:** Python, Django, Django REST Framework, React, SQL, MongoDB,
HTTP, WebSockets y pruebas automatizadas.

[Conversar sobre el proyecto →](mailto:martin.f8@icloud.com?subject=Psycode)
