import { useEffect, useState } from 'react'
import { Link, Route, Routes, useNavigate } from 'react-router-dom'
import './App.css'
import Home from './pages/Home'
import RoutesPage from './pages/RoutesPage'
import TripsPage from './pages/TripsPage'
import BookingPage from './pages/BookingPage'
import PaymentsPage from './pages/PaymentsPage'
import TrackingPage from './pages/TrackingPage'
import LoginPage from './pages/LoginPage'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const navigate = useNavigate()

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  const logout = () => {
    setToken('')
    navigate('/login')
  }

  return (
    <div className="container">
      <nav className="nav">
        <Link to="/">NagaraYatra</Link>
        <div className="nav-links">
          <Link to="/routes">Routes</Link>
          <Link to="/trips">Trips</Link>
          <Link to="/tracking">Tracking</Link>
          <Link to="/payments">Payments</Link>
          {token ? (
            <button onClick={logout}>Logout</button>
          ) : (
            <Link to="/login">Login</Link>
          )}
        </div>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/routes" element={<RoutesPage />} />
          <Route path="/trips" element={<TripsPage token={token} />} />
          <Route path="/book/:tripId" element={<BookingPage token={token} />} />
          <Route path="/payments" element={<PaymentsPage token={token} />} />
          <Route path="/tracking" element={<TrackingPage />} />
          <Route path="/login" element={<LoginPage setToken={setToken} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
