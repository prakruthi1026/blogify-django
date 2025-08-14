import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Polyline, Popup, useMap } from 'react-leaflet'

const API_BASE = 'http://localhost:8000/api'

function Recenter({ center }) {
  const map = useMap()
  useEffect(() => { if (center) map.setView(center, 13) }, [center])
  return null
}

export default function TripsPage({ token }) {
  const [trips, setTrips] = useState([])
  const [selected, setSelected] = useState(null)
  const [center, setCenter] = useState([19.076, 72.8777])

  useEffect(() => { load() }, [])

  const load = async () => {
    const res = await axios.get(`${API_BASE}/rides/trips/upcoming/`)
    setTrips(res.data)
  }

  const selectTrip = (t) => {
    setSelected(t)
    const firstStop = (t.route?.stops || [])[0]
    if (firstStop) setCenter([firstStop.lat, firstStop.lng])
  }

  const pts = (selected?.route?.stops || []).map(s => [s.lat, s.lng])

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      <div>
        <h3>Upcoming Trips</h3>
        <ul>
          {trips.map(t => (
            <li key={t.id} onClick={() => selectTrip(t)} style={{ cursor: 'pointer' }}>
              <div>
                <strong>{t.route?.name}</strong> — {t.departure_time?.replace('T',' ').slice(0,16)} — ₹{t.price}
                <div>Seats available: {t.seats_available}</div>
              </div>
              <div>
                <Link to={`/book/${t.id}`}>Book</Link>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div style={{ height: 480 }}>
        <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
          <Recenter center={center} />
          {pts.length > 0 && <Polyline positions={pts} color="#2e7d32" />}
          {(selected?.route?.stops || []).map((s, idx) => (
            <Marker key={`sel-${idx}`} position={[s.lat, s.lng]}>
              <Popup>
                <div>
                  <div>{selected?.route?.name}</div>
                  <div>Stop: {s.name}</div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}