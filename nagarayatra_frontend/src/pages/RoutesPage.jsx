import { useEffect, useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export default function RoutesPage() {
  const [routes, setRoutes] = useState([])
  const [q, setQ] = useState('')

  useEffect(() => {
    load()
  }, [])

  const load = async () => {
    const res = await axios.get(`${API_BASE}/rides/routes/`)
    setRoutes(res.data)
  }

  const filtered = routes.filter(r =>
    [r.name, r.start_name, r.end_name].join(' ').toLowerCase().includes(q.toLowerCase())
  )

  return (
    <div>
      <h3>Routes</h3>
      <input placeholder="Search" value={q} onChange={e => setQ(e.target.value)} />
      <ul>
        {filtered.map(r => (
          <li key={r.id}>
            <strong>{r.name}</strong> — {r.start_name} → {r.end_name}
          </li>
        ))}
      </ul>
    </div>
  )
}