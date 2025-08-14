import { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export default function TrackingPage() {
  const [tripId, setTripId] = useState('')
  const [location, setLocation] = useState(null)

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
    } catch (e) {
      setLocation(null)
    }
  }

  return (
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
  )
}