import { useEffect, useState } from 'react'
import axios from 'axios'
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet'

const API_BASE = 'http://localhost:8000/api'

function Recenter({ center }) {
  const map = useMap()
  useEffect(() => { if (center) map.setView(center, 14) }, [center])
  return null
}

export default function TrackingPage() {
  const [tripId, setTripId] = useState('')
  const [location, setLocation] = useState(null)
  const [center, setCenter] = useState([19.076, 72.8777])

  useEffect(() => {
    let timer
    if (tripId) {
      timer = setInterval(load, 5000)
      load()
    }
    return () => timer && clearInterval(timer)
  }, [tripId])

  const load = async () => {
    try {
      const res = await axios.get(`${API_BASE}/tracking/locations/latest/?trip_id=${tripId}`)
      setLocation(res.data)
      setCenter([res.data.latitude, res.data.longitude])
    } catch (e) {
      setLocation(null)
    }
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 16 }}>
      <div>
        <h3>Live Tracking</h3>
        <div>
          <input placeholder="Trip ID" value={tripId} onChange={e => setTripId(e.target.value)} />
        </div>
        {location ? (
          <div>
            <div>Lat: {location.latitude} Lng: {location.longitude}</div>
            <div>Speed: {location.speed_kmph} km/h</div>
            <div>Time: {new Date(location.timestamp).toLocaleString()}</div>
          </div>
        ) : (
          <div>No data</div>
        )}
      </div>
      <div style={{ height: 480 }}>
        <MapContainer center={center} zoom={13} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" attribution="&copy; OpenStreetMap contributors" />
          <Recenter center={center} />
          {location && (
            <Marker position={[location.latitude, location.longitude]}>
              <Popup>
                <div>
                  Trip {tripId}
                  <div>{new Date(location.timestamp).toLocaleTimeString()}</div>
                </div>
              </Popup>
            </Marker>
          )}
        </MapContainer>
      </div>
    </div>
  )
}