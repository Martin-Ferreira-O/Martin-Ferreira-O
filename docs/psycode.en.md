[← Back to profile](../README.en.md) · [Versión en español](./psycode.md)

# Psycode

**University team project · Private repository**

Psycode combines a web interface, a central server, and an installable agent
to support the supervision of psychology sessions. It brings together session
management, audio capture, processing, and alert review with traceability.

## My contribution

I have contributed to the Django backend, the React interface, and the separation
of the capture agent from the central server. My work also includes automated
component boundary checks and features for users, alerts, and evaluations.

## Architecture decisions

- **Modular monolith:** the server organizes responsibilities into modules and
  layers. HTTP views delegate to application services; infrastructure adapters
  handle persistence and external communication.
- **Independent agent:** the capture application has its own installation and
  operational lifecycle. It communicates with the server through HTTP and
  WebSocket contracts, rather than being imported into the backend.
- **Background processing:** audio ingestion and processing have separate
  responsibilities. Persistent job state supports retries and recovery.
- **Purpose-specific storage:** SQL holds accounts, sessions, and operational
  state; MongoDB stores alerts and audit events.

## Quality and collaboration

The project includes authentication, permission checks, technical audit trails,
and integration tests. Component boundary and contract checks help detect
unintended dependencies between the agent and server. Integration tests can run
with synthetic data and without real credentials.

This work has helped me practice separating responsibilities, maintaining
component contracts, and collaborating on an evolving team codebase.

**Technologies:** Python, Django, Django REST Framework, React, SQL, MongoDB,
HTTP, WebSockets, and automated testing.

[Discuss the project →](mailto:martin.f8@icloud.com?subject=Psycode)
