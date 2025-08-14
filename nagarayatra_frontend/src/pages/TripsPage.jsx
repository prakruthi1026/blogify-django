import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export default function TripsPage({ token }) {
  const [trips, setTrips] = useState([])

  useEffect(() => {
    load()
  }, [])

  const load = async () => {
    const res = await axios.get(`${API_BASE}/rides/trips/upcoming/`)
    setTrips(res.data)
  }

  return (
    <div>
      <h3>Upcoming Trips</h3>
      <ul>
        {trips.map(t => (
          <li key={t.id}>
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
  )
}