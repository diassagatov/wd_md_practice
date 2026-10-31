# Space Bounty Hunters API

Django REST Framework + PostgreSQL, run with Docker Compose.

## Run

```bash
cp .env.example .env
docker compose up --build
```

API: http://localhost:8000/api/ · Swagger: http://localhost:8000/swagger/

## Database

On start the container runs `python manage.py migrate`, which creates the tables and imports the seed data (5 criminals, 10 hunt logs) from `bounty/migrations/0002_seed_data.py`.

Reset to seed data: `docker compose down -v` and then `docker compose up --build`.

## Endpoints

| Method | URL |
|---|---|
| GET | `/api/criminals/?min_reward=&max_reward=&armed=&has_crew=&escape_master=&sort=reward\|-reward` |
| GET | `/api/criminals/{id}/` |
| GET | `/api/hunts/?criminal_id=` |
| GET | `/api/hunts/{id}/` |
| POST | `/api/hunts/` |
| PATCH | `/api/hunts/{id}/` |
| DELETE | `/api/hunts/{id}/` |

POST body:

```json
{ "criminal_id": 3, "success": false, "notes": "Target escaped through an asteroid field." }
```

`created_at` is set by the server.

## Postman

Import `postman/SpaceBountyHunters.postman_collection.json` and run it top to bottom on a fresh database.
