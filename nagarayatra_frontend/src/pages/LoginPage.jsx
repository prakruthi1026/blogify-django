import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

const API_BASE = 'http://localhost:8000/api'

export default function LoginPage({ setToken }) {
  const [username, setUsername] = useState('demo')
  const [password, setPassword] = useState('demo123')
  const [mode, setMode] = useState('login')
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    if (mode === 'register') {
      await axios.post(`${API_BASE}/rides/auth/register/`, { username, password })
    }
    const res = await axios.post(`${API_BASE}/auth/token/`, { username, password })
    setToken(res.data.token)
    navigate('/')
  }

  return (
    <div>
      <h3>{mode === 'login' ? 'Login' : 'Register'}</h3>
      <form onSubmit={submit}>
        <div>
          <input value={username} onChange={e => setUsername(e.target.value)} placeholder="username" />
        </div>
        <div>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="password" />
        </div>
        <button type="submit">Submit</button>
      </form>
      <button onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
        Switch to {mode === 'login' ? 'Register' : 'Login'}
      </button>
    </div>
  )
}