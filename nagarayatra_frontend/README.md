# NagaraYatra Frontend (React + Vite)

A minimal React UI for the NagaraYatra shuttle/tempo aggregator. Commuters can view routes and trips, book seats, pay (mock), and track live trips. Maps are rendered with Leaflet (OpenStreetMap tiles).

## Pages
- Home: high-level app info
- Routes: list of routes + map with polylines and stop markers
- Trips: upcoming trips list; selecting a trip shows its route on a map; book CTA
- Booking: confirm seats, then pay (mock) to confirm; side-by-side route map
- Tracking: live location map for a given trip ID
- Login: login/register for token-based API access

## Tech Stack
- React + Vite
- React Router
- Axios
- Leaflet + React Leaflet

## Prerequisites
- Node.js 18+

## Setup
```bash
cd /workspace/nagarayatra_frontend
npm install
```

## Configure API Base (if needed)
The frontend uses `http://localhost:8000/api` as the API base inside each page component (e.g. `src/pages/TripsPage.jsx`). If your backend runs elsewhere, change the `API_BASE` constant in those files or refactor into a single config.

## Run (dev)
```bash
npm run dev -- --host 0.0.0.0 --port 5173
```
Open `http://localhost:5173/`.

If running in a remote environment, expose/forward port 5173 to your machine.

## Build
```bash
npm run build
npm run preview
```
Then open the preview URL displayed in the terminal.

## Login
Use the seeded credentials (created by the backend `seed` command):
- User: `demo` / `demo123`
- Driver: `driver1` / `driver123` (not required for commuter flow)

## Typical Flow
1. Login on the Login page.
2. Go to Trips → select a trip → Book → Pay & Confirm.
3. Check Payments page to see recent payments.
4. For tracking, go to Tracking and enter the Trip ID to view live location updates.

## Maps
- Leaflet CSS is imported in `src/main.jsx`.
- Routes/Trips/Booking/Tracking pages embed OpenStreetMap tiles.
- If tiles do not load, check your network and ensure external requests to `tile.openstreetmap.org` are permitted.

## Notes
- Payments are mocked; the UI calls `/payments/initiate` then `/payments/{id}/confirm`.
- If you change backend ports or host, update `API_BASE` constants in the page components.
