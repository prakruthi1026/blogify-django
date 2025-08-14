import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export default function BookingPage({ token }) {
  const { tripId } = useParams()
  const [trip, setTrip] = useState(null)
  const [seats, setSeats] = useState(1)
  const [booking, setBooking] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    loadTrip()
  }, [tripId])

  const loadTrip = async () => {
    const res = await axios.get(`${API_BASE}/rides/trips/${tripId}/`)
    setTrip(res.data)
  }

  const createBooking = async () => {
    if (!token) {
      navigate('/login')
      return
    }
    const res = await axios.post(`${API_BASE}/rides/bookings/`, {
      trip_id: tripId,
      seats: seats,
    }, { headers: { Authorization: `Token ${token}` } })
    setBooking(res.data)
  }

  const initiatePayment = async () => {
    const res = await axios.post(`${API_BASE}/payments/initiate/`, {
      booking_id: booking.id,
      provider: 'mock'
    }, { headers: { Authorization: `Token ${token}` } })
    const payment = res.data
    const res2 = await axios.post(`${API_BASE}/payments/${payment.id}/confirm/`, {}, { headers: { Authorization: `Token ${token}` } })
    alert('Payment success! Booking confirmed.')
    navigate('/payments')
  }

  return (
    <div>
      <h3>Booking</h3>
      {!trip ? (
        <div>Loading...</div>
      ) : (
        <div>
          <div><strong>{trip.route?.name}</strong></div>
          <div>Departure: {trip.departure_time?.replace('T',' ').slice(0,16)}</div>
          <div>Seats available: {trip.seats_available}</div>
          <div>
            <label>Seats: </label>
            <input type="number" value={seats} min="1" max={trip.seats_available} onChange={e => setSeats(parseInt(e.target.value || '1'))} />
          </div>
          {!booking ? (
            <button onClick={createBooking}>Create Booking</button>
          ) : (
            <div>
              <div>Amount: ₹{booking.amount}</div>
              <button onClick={initiatePayment}>Pay & Confirm</button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}