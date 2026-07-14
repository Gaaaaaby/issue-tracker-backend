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

## Variables de entorno

Puedes usar un archivo `.env` local con estas variables:

```env
SECRET_KEY=change_this_secret_key_for_production
ACCESS_TOKEN_EXPIRE_MINUTES=60
DB_URL=sqlite:///./issues.db
BACKEND_CORS_ORIGINS=http://localhost:4200,https://localhost:4200
```

Railway y otros entornos pueden establecer `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DB_URL` y `BACKEND_CORS_ORIGINS` desde sus variables de entorno.

## Railway

Ya existe `railway.json` con:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
  }
}
```

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
