import { useEffect, useMemo, useState } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Polyline, Popup, useMap } from 'react-leaflet'

const API_BASE = 'http://localhost:8000/api'

function Recenter({ center }) {
  const map = useMap()
  useEffect(() => {
    if (center) map.setView(center, 13)
  }, [center])
  return null
}

export default function RoutesPage() {
  const [routes, setRoutes] = useState([])
  const [q, setQ] = useState('')
  const [center, setCenter] = useState([19.076, 72.8777])

  useEffect(() => { load() }, [])

  const load = async () => {
    const res = await axios.get(`${API_BASE}/rides/routes/`)
    setRoutes(res.data)
  }

  const filtered = routes.filter(r =>
    [r.name, r.start_name, r.end_name].join(' ').toLowerCase().includes(q.toLowerCase())
  )

  const firstStopCenter = (r) => {
    const s = (r.stops || [])[0]
    return s ? [s.lat, s.lng] : null
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      <div>
        <h3>Routes</h3>
        <input placeholder="Search" value={q} onChange={e => setQ(e.target.value)} />
        <ul>
          {filtered.map(r => (
            <li key={r.id} onClick={() => firstStopCenter(r) && setCenter(firstStopCenter(r))} style={{ cursor: 'pointer' }}>
              <strong>{r.name}</strong> — {r.start_name} → {r.end_name}
            </li>
          ))}
        </ul>
      </div>
      <div style={{ height: 480 }}>
        <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
          <Recenter center={center} />
          {filtered.map(r => {
            const pts = (r.stops || []).map(s => [s.lat, s.lng])
            return (
              <>
                {pts.length > 0 && <Polyline positions={pts} color="#1976d2" />}
                {(r.stops || []).map((s, idx) => (
                  <Marker key={`${r.id}-${idx}`} position={[s.lat, s.lng]}>
                    <Popup>
                      <div>
                        <div>{r.name}</div>
                        <div>Stop: {s.name}</div>
                      </div>
                    </Popup>
                  </Marker>
                ))}
              </>
            )
          })}
        </MapContainer>
      </div>
    </div>
  )
}