# Entregable 5 — Agente RAG con Azure SQL + ACA + ACR + Azure DevOps

API FastAPI con arquitectura RAG que usa Azure SQL como base de conocimiento, se ejecuta en Docker y se despliega en Azure Container Apps mediante un pipeline de Azure DevOps.

## Recursos Azure previstos

| Recurso | Nombre |
|---|---|
| Resource Group | `rg-entregable5-rag` |
| Region | `francecentral` |
| Azure SQL Server | `sql-rag-ent5-pgar` |
| Azure SQL Database | `ragdb` |
| ACR | `acragent5pgar` |
| Container App | `cae-entregable5-rag` |
| Imagen | `rag-agent-api` |

## Estructura

```
rag-agent-entregable5/
├── api.py
├── agent.py
├── ai_provider.py
├── db.py
├── init_db.py
├── settings.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── azure-pipelines.yml
├── tests/
├── sql/
└── scripts/
```

## Endpoints

| Endpoint | Metodo | Descripcion |
|---|---|---|
| `/` | GET | Informacion basica de la API |
| `/health` | GET | Estado y conexion con Azure SQL |
| `/knowledge` | GET | Lista fragmentos de conocimiento |
| `/ask` | POST | Pregunta al agente RAG |
| `/ingest` | POST | Inserta conocimiento nuevo |

## Configuracion local

```powershell
copy .env.example .env
# Editar .env con la cadena ODBC real
python -m pip install -r requirements.txt
python -m pytest -q
```

## Docker local

```powershell
docker compose build
docker compose run --rm agent python init_db.py
docker compose up -d
```

Swagger: http://localhost:8000/docs

## Seguridad

- No subir `.env` al repositorio.
- No incluir passwords en Dockerfile, YAML ni README.
- En ACA usar `secretref` para `AZURE_SQL_CONNECTION_STRING`.
