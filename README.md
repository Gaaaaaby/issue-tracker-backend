# Backend Issue Tracker

API FastAPI para la gestión de incidencias.

## Dependencias

Instaladas en `backend/venv`:
- fastapi
- uvicorn
- sqlalchemy
- passlib[bcrypt]
- python-jose[cryptography]
- pydantic

## Ejecutar

```bash
cd backend
./venv/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Probar con Swagger

Abre `http://localhost:8000/docs`, usa `POST /token` con `admin / Admin123!`, copia el token y pulsa `Authorize` para probar los endpoints seguros.

## App Engine

Incluye `app.yaml` para desplegar con `gcloud app deploy app.yaml`.

## Cloud Run

También hay un `Dockerfile` para crear una imagen Docker y desplegarla en Cloud Run.

## Usuarios preconfigurados

- admin / Admin123!
- user / User123!

## Endpoints

- `POST /token` - login y JWT.
- `GET /issues` - listar incidencias.
- `POST /issues` - crear incidencia.
- `PATCH /issues/{issue_id}` - actualizar estado/prioridad.
- `GET /summary` - resumen por estado.
