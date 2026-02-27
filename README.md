# HRMS Lite – Backend (Django DRF + PostgreSQL)

REST API backend for the HRMS Lite frontend. Built with Django, Django REST Framework, and PostgreSQL.

## Features

- **Employees**: List all, create (with validation), delete by id
- **Attendance**: List by employee (query `?employeeId=...`), create (mark attendance)
- Validation: required fields, valid email format, duplicate Employee ID handling
- Proper HTTP status codes and JSON error messages for the frontend

## Tech stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- PostgreSQL (via psycopg)
- django-cors-headers
- python-dotenv

## Prerequisites

- Python 3.10+
- PostgreSQL server (create a database, e.g. `hrms_lite`)

## Setup

1. **Create virtual environment and install dependencies**

   ```bash
   cd hrms-lite-backend
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**

   Copy `.env.example` to `.env` and set the variables:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set at least:
   - `PG_DATABASE`, `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`

3. **Create PostgreSQL database**

   ```bash
   createdb hrms_lite
   # or in psql: CREATE DATABASE hrms_lite;
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional, for admin)**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**

   ```bash
   python manage.py runserver
   ```

   API base URL: `http://localhost:8000/api/`

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | List all employees |
| POST | `/api/employees` | Create employee (body: `employeeId`, `fullName`, `email`, `department`) |
| DELETE | `/api/employees/<uuid>` | Delete employee by id |
| GET | `/api/attendance?employeeId=EMP001` | List attendance for that employee |
| POST | `/api/attendance` | Mark attendance (body: `employeeId`, `date`, `status` where status is `Present` or `Absent`) |

Responses use camelCase for the frontend: `employeeId`, `fullName`, etc. Errors return `{ "message": "..." }` with appropriate status codes.

## Connect frontend

In the React frontend project root, create or edit `.env`:

```env
VITE_API_BASE=http://localhost:8000/api
VITE_USE_BACKEND=true
```

Then run the frontend (`npm run dev`). It will use this backend.

## Assumptions

- Single admin user; no authentication on the API.
- Employee ID is unique; duplicate is rejected with 400 and message.
- One attendance record per employee per day; re-POST for same employee/date updates the status.
