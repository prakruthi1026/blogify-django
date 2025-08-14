import { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export default function PaymentsPage({ token }) {
  const [payments, setPayments] = useState([])

  useEffect(() => {
    if (token) load()
  }, [token])

  const load = async () => {
    const res = await axios.get(`${API_BASE}/payments/`, {
      headers: { Authorization: `Token ${token}` }
    })
    setPayments(res.data)
  }

  if (!token) return <div>Please login to view payments.</div>

  return (
    <div>
      <h3>Payments</h3>
      <ul>
        {payments.map(p => (
          <li key={p.id}>
            Booking {p.booking} — ₹{p.amount} — {p.status} — {p.transaction_id || '—'}
          </li>
        ))}
      </ul>
    </div>
  )
}