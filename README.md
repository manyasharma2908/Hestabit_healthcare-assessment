# Healthcare Backend (Django + DRF + JWT + PostgreSQL)

A clean starter that implements everything your assignment asks for.

## Tech
- Django, Django REST Framework
- JWT auth via `djangorestframework-simplejwt`
- PostgreSQL via `dj-database-url`
- Env vars via `python-dotenv`
- ORM models for Patient, Doctor, PatientDoctorMapping

## Quick Start

### 1) Clone & install
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure environment
Create a `.env` file from the example:
```
cp .env.example .env
```
Edit values as needed.

**.env**
```
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=*
# Format: postgres://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL=postgres://postgres:postgres@localhost:5432/healthcare_db
```

### 3) Database & migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4) Run
```bash
python manage.py runserver 0.0.0.0:8000
```

### 5) Auth & Endpoints

- Register: `POST /api/auth/register/` with `{ "name": "Alice", "email": "a@a.com", "username":"alice", "password":"StrongPass123" }`
- Login (JWT): `POST /api/auth/login/` with `{ "username": "alice", "password": "StrongPass123" }`
  - Response: `{ "access": "...", "refresh": "..." }`
  - Use header: `Authorization: Bearer <access>`

#### Patients (auth required; users see only their own patients)
- `POST /api/patients/`
- `GET /api/patients/`
- `GET /api/patients/<id>/`
- `PUT /api/patients/<id>/`
- `DELETE /api/patients/<id>/`

#### Doctors
- `GET /api/doctors/` (public)
- `POST /api/doctors/` (auth)
- `GET /api/doctors/<id>/`
- `PUT /api/doctors/<id>/` (auth)
- `DELETE /api/doctors/<id>/` (auth)

#### Patient–Doctor Mapping (auth; scoped to your patients)
- `POST /api/mappings/` with `{ "patient": <patient_id>, "doctor": <doctor_id> }`
- `GET /api/mappings/` – list your mappings
- `GET /api/mappings/<patient_id>/` – list doctors for a given patient you own
- `DELETE /api/mappings/<id>/`

### Notes
- Password validation is enabled (min length 8).
- Patients are tied to the creator via `created_by`.
- You can only assign doctors to your own patients.
- Default permissions: Auth required globally; Doctors allow read-only for anonymous.

### Testing quickly with cURL
```bash
# register
curl -X POST http://localhost:8000/api/auth/register/   -H "Content-Type: application/json"   -d '{"name":"Alice Doe","email":"alice@example.com","username":"alice","password":"StrongPass123!"}'

# login
ACCESS=$(curl -s -X POST http://localhost:8000/api/auth/login/   -H "Content-Type: application/json"   -d '{"username":"alice","password":"StrongPass123!"}' | python -c "import sys, json; print(json.load(sys.stdin)['access'])")

# create patient
curl -X POST http://localhost:8000/api/patients/   -H "Authorization: Bearer $ACCESS" -H "Content-Type: application/json"   -d '{"name":"John Smith","age":34,"gender":"M","address":"Bengaluru"}'

# list my patients
curl -H "Authorization: Bearer $ACCESS" http://localhost:8000/api/patients/
```

### Admin (optional)
```bash
python manage.py createsuperuser
```

Good luck! ✨
