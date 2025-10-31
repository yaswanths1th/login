// Login Page
import React from 'react'
import { useLocation } from 'react-router-dom'

export default function Login() {
  const location = useLocation()
  const message = location?.state?.message || 'Please login'

  return (
    <div className="container">
      <div className="card">
        <h2>Dummy Login Page</h2>
        <p className="subtitle">{message}</p>
        <div style={{ marginTop: 20 }}>
          <button className="btn" onClick={() => alert('This is a dummy login page.')}>Ok</button>
        </div>
      </div>
    </div>
  )
}
