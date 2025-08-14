# NagaraYatra Backend (Django + DRF)

NagaraYatra is a simple local shuttle/tempo aggregator backend that maps informal commute routes, lets commuters view timings, book seats, pay digitally (mock), and get trip updates. For drivers, it exposes demand clustering to help set optimal routes.

## Features

- Routes: define popular routes with named stops and coordinates; visualize on frontend
- Trips: scheduled trips per route with driver, pricing, seats
- Bookings: reserve seats with seat availability control
- Payments: mock digital payment flow (initiate + confirm/fail) tied to a booking
- Tracking: live vehicle locations, plus a "latest" location endpoint for each trip
- Demand Analytics: simple clustering of demand events by geobuckets
- Auth: token authentication, register, and current-user info

## Tech Stack

- Django 5 + Django REST Framework
- SQLite (dev)
- django-cors-headers, django-filter

## Quick Start

### Prerequisites
- Python 3.10+ (tested on 3.13)
- pip

### Install dependencies
```bash
cd /workspace/nagarayatra_backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install django djangorestframework django-cors-headers django-filter
```

If you are using the provided workspace, a virtualenv is already created at `/workspace/venv` with the required packages.

### Migrate and seed
```bash
cd /workspace/nagarayatra_backend
python manage.py migrate
python manage.py seed
```
This creates demo data:
- User: `demo` / `demo123`
- Driver: `driver1` / `driver123` (with a default `DriverProfile`)
- One sample route and a few upcoming trips

### Run
```bash
python manage.py runserver 0.0.0.0:8000
```
Visit `http://localhost:8000/` to check status.

If running in a remote dev environment, expose/forward port 8000 to your machine.

## Important Settings
- CORS allows `http://localhost:5173` for the React dev server
- Timezone set to `Asia/Kolkata`

## API Overview

Auth:
- POST `/api/auth/token/` → get token with `{"username","password"}`
- POST `/api/rides/auth/register/` → register `{"username","password"}`
- GET `/api/rides/auth/me` (Token) → current user and driver info

Routes:
- GET `/api/rides/routes/` → list routes

Trips:
- GET `/api/rides/trips/` → list all trips
- GET `/api/rides/trips/upcoming/` → list upcoming scheduled trips
- GET `/api/rides/trips/{id}/` → trip details
- POST `/api/rides/trips/` (Token; driver only) → create trip
  - Body: `{ "route_id": number, "departure_time": "2025-08-14T10:30:00Z", "price": 20 }`

Bookings (Token):
- POST `/api/rides/bookings/` → create booking `{ "trip_id": number, "seats": number }`
- POST `/api/rides/bookings/{id}/cancel/` → cancel booking (restores seats)

Payments (Token):
- GET `/api/payments/` → list user's payments
- POST `/api/payments/initiate/` → `{ "booking_id": number, "provider": "mock" }`
- POST `/api/payments/{id}/confirm/` → mark as success + confirm booking
- POST `/api/payments/{id}/fail/` → mark as failed

Tracking:
- POST `/api/tracking/locations/` → create location
  - Body: `{ "trip": number, "latitude": float, "longitude": float, "heading_degrees"?: float, "speed_kmph"?: float }`
- GET `/api/tracking/locations/?trip={id}` → list for a trip
- GET `/api/tracking/locations/latest/?trip_id={id}` → latest location

Demand events:
- POST `/api/rides/demand/` → `{ "latitude": float, "longitude": float, "event_type": "view|search|booking", "meta"?: {} }`
- GET `/api/rides/demand/clusters/` → top geobuckets (rounded lat/lng; naive clustering)

## Notes
- Payments are mocked for demo purposes. Replace with a real provider in production.
- The backend returns CORS headers for the frontend on port 5173.
- DEBUG is enabled. Disable DEBUG and set `ALLOWED_HOSTS` appropriately for production.