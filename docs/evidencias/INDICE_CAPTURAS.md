# Índice de capturas — Entregable 5

Carpeta: `docs/evidencias/`

## Fase 1 — Repositorio y estructura

| Archivo | Descripción | Sección informe |
|---|---|---|
| `fase1-01-repositorio-azure-devops-codigo.png` | Repositorio en Azure DevOps con código subido en `main` | Configuración y estructuración |

## Fase 2 — Azure SQL Database

| Archivo | Descripción | Sección informe |
|---|---|---|
| `fase2-01-sql-implementacion-completada.png` | Despliegue de `ragdb` completado | Azure SQL |
| `fase2-02-grupo-recursos-recursos.png` | Grupo `rg-entregable5-rag` con SQL Server y BD | Arquitectura Azure |
| `fase2-03-sql-database-ragdb-overview.png` | Overview de la base de datos `ragdb` | Azure SQL |
| `fase2-04-sql-configuracion-basica.png` | Configuración básica del asistente de creación | Azure SQL |
| `fase2-05-sql-cadena-odbc.png` | Cadena de conexión ODBC (sin contraseña real) | Configuración segura |
| `fase2-06-sql-firewall-redes.png` | Reglas de firewall del servidor SQL | Seguridad / redes |
| `fase2-07-sql-query-editor-chunks.png` | Query editor con 4 filas de `knowledge_chunks` | Azure SQL / validación |

## Fase 4 — Validación local (Swagger)

| Archivo | Descripción | Sección informe |
|---|---|---|
| `fase4-01-swagger-endpoint-ask.png` | Swagger UI con endpoint POST `/ask` | Validación local |
| `fase4-02-swagger-ask-respuesta-sources.png` | Respuesta de `/ask` con `answer` y `sources` | Agente RAG funcional |

## Fase 5 — Azure Container Registry

| Archivo | Descripción | Sección informe |
|---|---|---|
| `fase5-01-acr-overview.png` | Overview del ACR `acragent5pgar` | Registro en Azure |
| `fase5-02-acr-admin-user.png` | Admin user habilitado en Claves de acceso | Registro en Azure |
| `fase5-03-acr-repositorio-tags.png` | Repositorio `rag-agent-api` con tags `v1` y `latest` | Registro en Azure |

## Pendientes (añadir cuando las tengas)

| Archivo sugerido | Descripción |
|---|---|
| `fase4-03-swagger-health-local.png` | GET `/health` con `database: connected` |
| `fase4-04-docker-compose-build.png` | Terminal con `docker compose build` OK |
| `fase6-01-aca-running-fqdn.png` | Container App en estado Running |
| `fase7-01-pipeline-stages-verde.png` | Pipeline con stages en verde |
| `fase8-01-health-cloud.png` | `/health` en URL pública de ACA |
| `fase8-02-ask-cloud-sources.png` | `/ask` en cloud con sources |
| `fase8-03-aca-logs.png` | Logs de Azure Container Apps |
