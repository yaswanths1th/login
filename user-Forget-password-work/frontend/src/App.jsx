// Main App component
import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import ForgotPassword from './pages/ForgotPassword'
import VerifyOTP from './pages/VerifyOTP'
import Login from './pages/Login'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/forgot-password" replace />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/verify-otp" element={<VerifyOTP />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  )
}

export default App
