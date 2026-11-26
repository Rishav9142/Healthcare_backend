# Healthcare Backend

A Django REST Framework backend for managing healthcare users, patients, doctors,
and patient-doctor assignments.

## Requirements

- Python 3.10+
- PostgreSQL

## Local setup

1. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a local environment file and configure it with your PostgreSQL
   credentials:

   ```powershell
   Copy-Item .env.example .env
   ```

   Set `DJANGO_SECRET_KEY` to a generated secret and update the `DB_*` values.
   The `.env` file is excluded from Git.

4. Apply migrations and start the development server:

   ```powershell
   python manage.py migrate
   python manage.py runserver
   ```

## Authentication

- `POST /api/auth/register/` — register with `name`, `email`, and `password`.
- `POST /api/auth/login/` — submit `email` and `password` to receive `access`
  and `refresh` JWTs.

Use the access token on protected API requests:

```http
Authorization: Bearer <access-token>
```

Run the authentication tests with the SQLite test settings (no local PostgreSQL
service is needed for these tests):

```powershell
python manage.py test accounts --settings=healthcare.test_settings
```
